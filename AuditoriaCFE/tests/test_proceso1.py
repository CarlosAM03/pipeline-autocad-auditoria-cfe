import csv
import io
import json
import math
import os
import subprocess
import sys
import tracemalloc
import unittest
import zipfile
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from support import AuditFixture, GEO, HEADERS, PROJECT, record, xlsx
from auditoriacfe import config
from auditoriacfe.cli import main
from auditoriacfe.coordinates import parse, serialize
from auditoriacfe.dedup import consolidate, key
from auditoriacfe.pipeline import run
from auditoriacfe.quality import prepare
from auditoriacfe.projection import prepare_projection
from auditoriacfe.reporting import audit_lock, publish, recover, verify
from auditoriacfe.schemas import extract
from auditoriacfe.source_ooxml import MAX_META, Workbook
from auditoriacfe.util import PipelineError, digest, sha256


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.audit = AuditFixture()
        self.addCleanup(self.audit.close)

    def source(self, rows=None, family=3, name="a.xlsx", **kwargs):
        return xlsx(self.audit.path / "entrada" / name, family, rows, **kwargs)

    def execute(self, **changes):
        self.audit.save(**changes)
        return run(self.audit.path, emit=lambda *args: None)

    def csv(self, name):
        with (self.audit.path / "salida" / name).open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    def lineage(self):
        return [json.loads(line) for line in (self.audit.path / "salida/linaje_y_calidad.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_four_families_hidden_images_blank_sheet(self):
        for family in (1, 2, 3, 4):
            with self.subTest(family=family):
                path = self.source(family=family, images=True, rows=[(2, record(family), True), (3, {"J": "."}, False)])
                opened = []
                original = zipfile.ZipFile.open
                def monitored(book, name, *args, **kwargs):
                    opened.append(str(name))
                    self.assertNotIn("xl/media/", str(name))
                    self.assertNotIn("xl/drawings/", str(name))
                    return original(book, name, *args, **kwargs)
                with patch.object(zipfile.ZipFile, "open", monitored):
                    records, profiles, aux = extract(path, "a.xlsx", sha256(path))
                self.assertEqual(len(records), 1)
                self.assertTrue(records[0]["oculta"])
                self.assertTrue(records[0]["familia"].startswith(f"F{family}"))
                self.assertEqual(profiles[0]["medios_no_leidos"], 1)
                self.assertEqual(aux[0]["fila"], 3)
        self.source(empty=True)
        m = self.execute()
        self.assertEqual(m["conteos"]["ocurrencias"], 0)
        self.assertEqual(m["perfiles_hojas"][0]["familia"], "VACIA")

    def test_blank_d_requires_explicit_exception(self):
        self.source(blank_d=True)
        with self.assertRaisesRegex(PipelineError, "Cabecera D"):
            self.execute()
        m = self.execute(excepciones_cabecera={"a.xlsx": {"Datos": "F3_D_VACIA"}})
        self.assertEqual(m["conteos"]["POSTE"], 1)

    def test_shared_strings_formula_metadata_and_no_cache(self):
        cells = record(extras={"B": {"tipo": "s", "valor": 0},
                               "F": {"tipo": "str", "valor": "32.500000N", "formula": "LEFT(D2,10)", "attrs": {"t": "shared", "si": "0", "ref": "F2:F3"}},
                               "G": {"tipo": "str", "valor": "117.000000W", "formula": "", "attrs": {"t": "shared", "si": "0"}},
                               "H": {"tipo": "n", "valor": None, "formula": "1+2"}})
        self.source(rows=[(2, cells, False)], shared=["Conexión, ruta"])
        m = self.execute()
        r = self.lineage()[0]
        self.assertEqual(r["ruta_original"], "Conexión, ruta")
        self.assertEqual(r["celdas_originales"]["G"]["formula_atributos"]["si"], "0")
        self.assertTrue(r["celdas_originales"]["G"]["es_formula"])
        self.assertEqual(m["perfiles_hojas"][0]["formulas_sin_cache"], 1)

    def test_million_physical_rows_bounded_memory(self):
        self.source(dimension="A1:XFD1048576", physical_rows=1048576, images=True)
        tracemalloc.start()
        try:
            records, profiles, _ = extract(self.audit.path / "entrada/a.xlsx", "a.xlsx", "fixture")
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(profiles[0]["filas_xml"], 1048576)
        self.assertEqual(len(records), 1)
        self.assertLess(peak, 12 * 1024 * 1024, f"pico Python={peak}")
        print(f"\nMemoria lector millón filas: {peak} bytes Python (tracemalloc)")

    def test_sharedstrings_limit_explicit_failure(self):
        path = self.source()
        with zipfile.ZipFile(path, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr("xl/sharedStrings.xml", b" " * (MAX_META + 1))
        with self.assertRaisesRegex(PipelineError, "Metadatos OOXML"):
            with Workbook(path):
                pass

    def test_strict_coordinates_and_exact_precision(self):
        for text in ("32.5N 117.0W", "32.5N117.0W", "32.5N  117.0W", " 32.5 ° n 117.0 ° w "):
            self.assertEqual(parse(text), (Decimal("32.5"), Decimal("-117.0")))
        for text in ("No detectado", "32.5N 117", "32,5N 117W", "32.5B 117W", "432.464440N 116.8W", "32.5N 11702014028W", "-32.5N 117W", "32..5N 117W", "32.5N 1e2W"):
            with self.subTest(text=text), self.assertRaises(PipelineError):
                parse(text)
        pair = parse("32.123456789012345678901234567890123456N 117.123456789012345678901234567890123456W")
        self.assertEqual(serialize(*pair), "32.123456789012345678901234567890123456N 117.123456789012345678901234567890123456W")
        self.assertEqual(parse("32.5S 117.0E"), (Decimal("-32.5"), Decimal("117.0")))

    def test_recovery_auxiliary_and_conflicts(self):
        rows = [
            (2, record(coord="No detectado", extras={"F": "32.5N", "G": "117W", "H": "32.5", "I": "-117"}), False),
            (3, record(coord="32.5N 117", extras={"F": "32.5N", "G": "117W"}), False),
            (4, record(coord="No detectado", extras={"F": "32.5N", "G": "117W", "H": "32.6", "I": "-117"}), False),
            (5, record(coord="No detectado", extras={"H": "325", "I": "-117"}), False),
            (6, record(coord="32.5N 11702014028W", extras={"F": "32.5N", "G": "117W"}), False),
            (7, record(coord="No detectado", extras={"F": {"tipo": "str", "valor": "32.5N", "formula": "something"}, "G": "117W"}), False),
            (8, record(coord="32.6N MALO", extras={"F": "32.5N", "G": "117W"}), False),
            (9, record(extras={"H": "32500000", "I": "-117000000"}), False),
        ]
        self.source(rows=rows)
        self.execute()
        rs = self.lineage()
        self.assertEqual([r["estado"] for r in rs], ["VALIDO", "DUPLICADO", "RECHAZADO", "RECHAZADO", "RECHAZADO", "RECHAZADO", "RECHAZADO", "DUPLICADO"])
        self.assertIn("RECUPERADO_AUXILIAR", [i["codigo"] for i in rs[0]["incidencias"]])
        self.assertEqual(rs[0]["coordenada_original"], "No detectado")
        self.assertEqual(rs[-1]["coordenada_normalizada"], "32.500000N 117.000000W")

    def test_scope_unknown_remote_empty_route_and_missing_geography(self):
        self.source(rows=[(2, record(typ="Registro", coord="MALO"), False),
                          (3, record(typ="caja desconocida"), False),
                          (4, record(coord="2.52867353N 116.89829643W"), False),
                          (5, record(route=""), False),
                          (6, record(coord="32.5S 117E"), False)])
        m = self.execute()
        self.assertEqual([r["estado"] for r in self.lineage()], ["FUERA_ALCANCE"] + ["REVISAR"] * 4)
        self.assertEqual(m["conteos"]["POSTE"], 0)
        self.assertEqual([i["codigo"] for i in self.lineage()[0]["incidencias"]], ["REGISTRO_SUBTERRANEO"])
        self.source()
        self.execute(geografia_permitida=None)
        self.assertEqual(self.lineage()[0]["estado"], "REVISAR")
        self.assertEqual(self.csv("01_elementos_normalizados.csv"), [])

    def test_exact_dedup_precedence_routes_types_and_nearby(self):
        self.source(name="z.xlsx", rows=[(2, record(route="Prevalente"), False)])
        self.source(name="a.xlsx", rows=[(2, record(route="Otra", coord="32.5N 117W"), False),
                                           (3, record(typ="cajadedmpalme"), False),
                                           (4, record(coord="32.50000000000000000000000000000001N 117W"), False),
                                           (5, record(coord="32.50001N 117W"), False)])
        m = self.execute(fuentes_en_orden=["z.xlsx", "a.xlsx"], cercanos_m=10)
        rs = self.lineage()
        self.assertEqual(rs[1]["estado"], "DUPLICADO")
        self.assertEqual(rs[1]["prevalente_id"], rs[0]["ocurrencia_id"])
        self.assertEqual(m["conteos"]["unicos_exportables"], 4)
        self.assertEqual(self.csv("01_elementos_normalizados.csv")[0]["Ruta"], "Prevalente")
        self.assertEqual(len(self.csv("asociaciones_elemento_ruta.csv")), 5)
        self.assertGreater(len(self.csv("coordenadas_cercanas.csv")), 0)
        self.assertEqual(self.csv("topologia_propuesta.csv"), [])
        # Fechas físicas no alteran autoridad ni bytes.
        before = {p.name: p.read_bytes() for p in (self.audit.path / "salida").iterdir()}
        os.utime(self.audit.path / "entrada/a.xlsx", (1, 1))
        again = self.execute()
        self.assertEqual(m, again)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.audit.path / "salida").iterdir()})
        swapped = self.execute(fuentes_en_orden=["a.xlsx", "z.xlsx"])
        self.assertEqual(self.csv("01_elementos_normalizados.csv")[0]["Ruta"], "Otra")

    def test_trusted_ids_two_boxes_and_unassigned_occurrence(self):
        self.source(rows=[(i, record(typ="cajadedmpalme"), False) for i in range(2, 6)])
        ids = [dict(archivo="a.xlsx", hoja="Datos", fila=row, id=identity, evidencia="Fixture: foto de placa verificada") for row, identity in ((2, "A"), (3, "B"), (4, "A"))]
        m = self.execute(ids_confiables=ids)
        self.assertEqual(m["conteos"]["CAJA_EMP"], 2)
        rs = self.lineage()
        self.assertEqual([r["estado"] for r in rs], ["VALIDO", "VALIDO", "DUPLICADO", "REVISAR"])
        self.assertNotEqual(rs[0]["elemento_id"], rs[1]["elemento_id"])
        self.assertEqual(rs[0]["elemento_id"], rs[2]["elemento_id"])

    def test_conflicting_id_positions_to_review(self):
        self.source(rows=[(2, record(typ="cajadedmpalme"), False), (3, record(typ="cajadedmpalme", coord="32.6N 117W"), False)])
        ids = [dict(archivo="a.xlsx", hoja="Datos", fila=i, id="A", evidencia="Fixture") for i in (2, 3)]
        m = self.execute(ids_confiables=ids)
        self.assertEqual(m["conteos"]["REVISAR"], 2)

    def test_configuration_invalid_and_complete_inventory(self):
        self.source()
        for changes in (dict(fuentes_en_orden=[]), dict(fuentes_en_orden=["a.xlsx", "a.xlsx"]),
                        dict(fuentes_en_orden=["../a.xlsx"]), dict(fuentes_en_orden=["absent.xlsx"]),
                        dict(crs_validado="false"), dict(cercanos_m=float("nan")),
                        dict(geografia_permitida={**GEO, "lat_min": 40}), dict(extra_no_reconocido=True)):
            self.audit.cfg = dict(auditoria=self.audit.path.name, fuentes_en_orden=["a.xlsx"], geografia_permitida=GEO)
            self.audit.save(**changes)
            with self.subTest(changes=changes), self.assertRaises(PipelineError):
                run(self.audit.path, emit=lambda *args: None)

    def test_sheet_precedence_obligatory_and_empty_sheet_profile(self):
        self.source(sheets=[("B", [(1, HEADERS[3], False), (2, record(route="B"), False)]),
                            ("A", [(1, HEADERS[3], False), (2, record(route="A"), False)]), ("Vacia", [])])
        with self.assertRaisesRegex(PipelineError, "orden de todas"):
            self.execute()
        m = self.execute(hojas_por_fuente={"a.xlsx": ["A", "B", "Vacia"]})
        self.assertEqual(self.csv("01_elementos_normalizados.csv")[0]["Ruta"], "A")
        self.assertEqual(m["perfiles_hojas"][-1]["familia"], "VACIA")

    def test_master_and_baseline_are_independent_and_not_filter(self):
        self.source(rows=[(2, record(), False), (3, record(coord="32.6N 117W"), False)])
        master = xlsx(self.audit.path / "maestro.xlsx")
        baseline = self.audit.path / "base.csv"
        baseline.write_text("Ruta,Elemento de Red,Coordenadas\nOtra,POSTE,32.6N 117W\n", encoding="utf-8")
        spec_master = dict(archivo="maestro.xlsx", fecha="2026-01-01")
        self.execute(maestro_informativo=spec_master)
        summary = self.csv("summary.csv")
        self.assertEqual([r["novedad_vs_baseline"] for r in summary], ["NO_DETERMINADO"] * 2)
        self.assertEqual([r["coincide_maestro"] for r in summary], ["SI", "NO"])
        self.assertEqual(len(self.csv("01_elementos_normalizados.csv")), 2)
        self.execute(baseline_historica=dict(archivo="base.csv", fecha="2025-10-01", auditoria=self.audit.path.name))
        self.assertEqual([r["novedad_vs_baseline"] for r in self.csv("summary.csv")], ["NUEVO", "EXISTENTE"])

    def test_incomplete_baseline_cannot_prove_new(self):
        self.source()
        (self.audit.path / "base.csv").write_text("Ruta,Elemento de Red,Coordenadas\nR,POSTE,MALO\n", encoding="utf-8")
        self.execute(baseline_historica=dict(archivo="base.csv", fecha="2025-01-01", auditoria=self.audit.path.name))
        self.assertEqual(self.csv("summary.csv")[0]["novedad_vs_baseline"], "NO_DETERMINADO")

    def test_csv_escaping_contract_counts_hashes_and_manifest_location(self):
        route = 'Conexión, "ruta"\nSegunda línea '
        self.source(rows=[(2, record(route=route), False), (3, record(route=route), False),
                          (4, record(typ="Registro"), False), (5, record(coord="MALO"), False)])
        m = self.execute()
        content = (self.audit.path / "salida/01_elementos_normalizados.csv").read_bytes()
        self.assertTrue(content.startswith(b"Ruta,Elemento de Red,Coordenadas\r\n"))
        self.assertEqual(self.csv("01_elementos_normalizados.csv")[0]["Ruta"], route)
        c = m["conteos"]
        self.assertEqual(c["ocurrencias"], sum(c[s] for s in ("VALIDO", "DUPLICADO", "FUERA_ALCANCE", "RECHAZADO", "REVISAR")))
        self.assertEqual(len(self.csv("summary.csv")), 3)
        self.assertTrue((self.audit.path / "manifiestos" / (m["ejecucion_id"] + ".json")).exists())
        self.assertFalse((self.audit.path / "salida/manifiesto_ejecucion.json").exists())
        for name, meta in m["artefactos"].items():
            self.assertEqual(sha256(self.audit.path / "salida" / name), meta["sha256"])
        self.assertEqual(verify(self.audit.path), m)
        with (self.audit.path / "salida/summary.csv").open("a", encoding="utf-8") as f:
            f.write("alterado")
        with self.assertRaisesRegex(PipelineError, "Hash/tamaño"):
            verify(self.audit.path)

    def test_pending_geography_still_has_dedup_lineage_and_comparison(self):
        self.source(rows=[(2, record(), False), (3, record(), False)])
        m = self.execute(geografia_permitida=None)
        self.assertEqual(m["conteos"]["unicos_identificados"], 1)
        self.assertEqual(m["conteos"]["unicos_exportables"], 0)
        self.assertEqual([r["estado"] for r in self.lineage()], ["REVISAR", "DUPLICADO"])
        self.assertEqual(self.csv("summary.csv")[0]["ocurrencias"], "2")

    def test_missing_or_corrupt_reference_and_corrupt_workbook_fail_explicitly(self):
        self.source()
        with self.assertRaises(PipelineError):
            self.execute(maestro_informativo=dict(archivo="missing.xlsx", fecha="2026-01-01"))
        self.audit.cfg["maestro_informativo"] = None
        self.audit.save()
        (self.audit.path / "entrada/a.xlsx").write_bytes(b"CORRUPT")
        proc = subprocess.run([sys.executable, str(PROJECT / "preparar_auditoria.py"), "--auditoria", self.audit.path.name], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertTrue(list((self.audit.path / "manifiestos").glob("fallo_*.json")))

    def evidence(self, offset=0):
        # Controles analíticos: meridiano central UTM 11, ecuador y latitud 1°.
        (self.audit.path / "control.txt").write_text("FIXTURE; no evidencia CAD real", encoding="utf-8")
        return dict(archivo="control.txt", aprobado_por="TEST", fecha="2026-01-01", crs="EPSG:32611", unidades="m", tolerancia_m=0.01,
                    controles=[dict(id="C1", latitud=0, longitud=-117, este_m=500000, norte_m=offset),
                               dict(id="C2", latitud=1, longitud=-117, este_m=500000, norte_m=110530.15880237566 + offset)])

    def test_projection_gate_and_correct_always_xy(self):
        self.source()
        self.execute()
        self.assertFalse((self.audit.path / "salida/02_elementos_proyectados.csv").exists())
        m = self.execute(crs_validado=True, evidencia_crs=self.evidence())
        self.assertTrue(m["crs_validado"])
        self.assertEqual(len(self.csv("02_elementos_proyectados.csv")), 1)
        row = self.csv("02_elementos_proyectados.csv")[0]
        self.assertAlmostEqual(float(row["este_m"]), 500000, places=5)
        # Referencia independiente en meridiano central: integral de radio de
        # curvatura meridiano WGS84 por Simpson, k0=0.9996; no usa pyproj.
        phi = math.radians(32.5)
        n = 10000
        step = phi / n
        e2 = 0.0066943799901413165
        def meridian(t):
            return 6378137 * (1 - e2) / (1 - e2 * math.sin(t) ** 2) ** 1.5
        total = meridian(0) + meridian(phi)
        total += sum((4 if i % 2 else 2) * meridian(i * step) for i in range(1, n))
        expected_north = 0.9996 * step * total / 3
        self.assertAlmostEqual(float(row["norte_m"]), expected_north, places=4)
        # CRS bloqueado tras una corrida acreditada elimina el proyectado antiguo.
        self.execute(crs_validado=False)
        self.assertFalse((self.audit.path / "salida/02_elementos_proyectados.csv").exists())

    def test_bad_controls_and_missing_evidence_block_only_projection(self):
        self.source()
        for evidence in (None, "texto no acredita", self.evidence(11.5), {**self.evidence(), "controles": self.evidence()["controles"][:1]}, {**self.evidence(), "unidades": "ft"}):
            with self.subTest(evidence=evidence):
                m = self.execute(crs_validado=True, evidencia_crs=evidence)
                self.assertFalse(m["crs_validado"])
                self.assertEqual(m["conteos"]["POSTE"], 1)

    def test_dry_run_no_writes_and_cli_modes(self):
        self.source()
        self.audit.save()
        before = sorted(p.relative_to(self.audit.path).as_posix() for p in self.audit.path.rglob("*"))
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            code = main(["--auditoria", self.audit.path.name, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("XLSX detectados: 1", out.getvalue())
        self.assertEqual(before, sorted(p.relative_to(self.audit.path).as_posix() for p in self.audit.path.rglob("*")))
        # Aislar listado interactivo para no depender de auditorías del operador.
        with patch.object(config, "AUDITS", self.audit.path.parent), patch("builtins.input", return_value="1"), patch("pathlib.Path.iterdir", return_value=iter([self.audit.path])), patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(main(["--dry-run"]), 0)
        for name in ("..", "a/b", "a\\b", ""):
            with self.assertRaises(PipelineError):
                config.audit_path(name)
        proc = subprocess.run([sys.executable, str(PROJECT / "preparar_auditoria.py"), "--auditoria", self.audit.path.name], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_unknown_schema_failure_keeps_previous_output_and_manifest(self):
        self.source()
        self.execute()
        before = (self.audit.path / "salida/01_elementos_normalizados.csv").read_bytes()
        self.source(sheets=[("Datos", [(1, {"A": "DESCONOCIDO"}, False), (2, record(), False)])])
        with self.assertRaises(PipelineError):
            self.execute()
        self.assertEqual(before, (self.audit.path / "salida/01_elementos_normalizados.csv").read_bytes())
        self.assertTrue(list((self.audit.path / "manifiestos").glob("fallo_*.json")))

    def test_publication_rollback_and_crash_recovery(self):
        self.source()
        self.execute()
        original = os.replace
        def interrupt_stage(src, dst):
            if Path(src).name.startswith("proceso1_"):
                raise KeyboardInterrupt("fixture interrupción")
            return original(src, dst)
        before = {p.name: p.read_bytes() for p in (self.audit.path / "salida").iterdir()}
        with patch("auditoriacfe.reporting.os.replace", side_effect=interrupt_stage), self.assertRaises(KeyboardInterrupt):
            self.execute()
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.audit.path / "salida").iterdir()})
        prior = self.audit.path / "temporales/salida_anterior"
        os.replace(self.audit.path / "salida", prior)
        recover(self.audit.path)
        self.assertTrue((self.audit.path / "salida").is_dir())
        self.assertFalse(prior.exists())

    def test_source_changed_during_read_is_not_published(self):
        path = self.source()
        real_extract = extract
        def change_after(*args, **kwargs):
            result = real_extract(*args, **kwargs)
            with path.open("ab") as stream:
                stream.write(b"changed")
            return result
        with patch("auditoriacfe.pipeline.extract", side_effect=change_after), self.assertRaisesRegex(PipelineError, "cambió"):
            self.execute()
        self.assertFalse((self.audit.path / "salida").exists())

    def test_concurrent_audit_lock_rejected(self):
        with audit_lock(self.audit.path):
            with self.assertRaises(PipelineError):
                with audit_lock(self.audit.path):
                    pass


if __name__ == "__main__":
    unittest.main()
