import csv
import json
import subprocess
import types
import unittest
from pathlib import Path

from support import AuditFixture, GEO, PROJECT, record, xlsx
from auditoriacfe import config, reporting
from auditoriacfe.dedup import consolidate, identified_groups
from auditoriacfe.pipeline import run
from auditoriacfe.quality import prepare
from auditoriacfe.schemas import extract
from auditoriacfe.util import PipelineError, sha256


class UnifiedTests(unittest.TestCase):
    def setUp(self):
        self.audit = AuditFixture()
        self.addCleanup(self.audit.close)

    def source(self, rows=None, name="a.xlsx", family=3):
        return xlsx(self.audit.path / "entrada" / name, family=family, rows=rows)

    def execute(self, **cfg):
        self.audit.save(**cfg)
        return run(self.audit.path, emit=lambda *args: None)

    def rows(self, name="00_elementos_unificados.csv"):
        with (self.audit.path / "salida" / name).open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def lineage(self):
        return [json.loads(l) for l in (self.audit.path / "salida/linaje_y_calidad.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_pending_p03_p06_identified_is_not_admitted(self):
        self.source(rows=[(2, record(), False), (3, record(route="Subruta B"), False)])
        m = self.execute(geografia_permitida=None, crs_validado=False)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["estado_preparacion"], "IDENTIFICADO")
        self.assertEqual(rows[0]["admision_geografica"], "PENDIENTE_P03")
        self.assertEqual(rows[0]["apto_csv_01"], "NO")
        self.assertEqual(rows[0]["ocurrencias"], "2")
        self.assertEqual(self.rows("01_elementos_normalizados.csv"), [])
        self.assertFalse((self.audit.path / "salida/02_elementos_proyectados.csv").exists())
        self.assertEqual(m["checkpoints"]["CP-01"]["estado"], "COMPLETADO")
        self.assertIn("00_elementos_unificados.csv", m["artefactos"])
        self.assertEqual(reporting.verify(self.audit.path), m)

    def test_exact_identity_precision_subroutes_and_prevalence(self):
        exact = "32.50000000000000000000000000000001N 117W"
        self.source(name="z.xlsx", rows=[(2, record(route='Ruta, "primera"'), False)])
        self.source(rows=[(2, record(coord="32.5N117W", route="B"), False),
                          (3, record(coord=exact), False), (4, record(typ="cajadedmpalme"), False)])
        self.execute(fuentes_en_orden=["z.xlsx", "a.xlsx"], geografia_permitida=None)
        rows = self.rows()
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["ruta_prevalente"], 'Ruta, "primera"')
        self.assertEqual(rows[0]["archivo_prevalente"], "z.xlsx")
        self.assertEqual(rows[0]["ocurrencias"], "2")
        self.assertEqual(rows[1]["coordenada_interpretada"], exact)
        self.assertEqual(len(self.rows("asociaciones_elemento_ruta.csv")), 4)
        lineage = self.lineage()
        self.assertEqual(lineage[1]["prevalente_id"], lineage[0]["ocurrencia_id"])

    def test_ids_and_unidentifiable_records_not_invented(self):
        self.source(rows=[(2, record(typ="cajadedmpalme"), False), (3, record(typ="cajadedmpalme"), False),
                          (4, record(typ="cajadedmpalme"), False), (5, record(coord="432N 117W"), False),
                          (6, record(typ="Registro", coord="MALO"), False), (7, record(typ="DESCONOCIDO"), False)])
        ids = [dict(archivo="a.xlsx", hoja="Datos", fila=i, id=identity, evidencia="FIXTURE") for i, identity in ((2,"A"),(3,"B"))]
        m = self.execute(ids_confiables=ids, geografia_permitida=None)
        self.assertEqual(len(self.rows()), 2)
        self.assertEqual(len({r["elemento_id"] for r in self.rows()}), 2)
        lineage = self.lineage()
        self.assertEqual([r["elemento_id"] for r in lineage[2:]], [None] * 4)
        self.assertEqual(len(lineage), 6)
        self.assertEqual(m["conteos"]["RECHAZADO"], 1)
        self.assertEqual(m["conteos"]["FUERA_ALCANCE"], 1)
        self.assertEqual(m["conteos"]["ocurrencias_revision_sin_identidad"], 2)
        self.assertIn("ID_EQUIPO_AMBIGUO", {i["codigo"] for i in self.rows("reporte_incidencias.csv")})

    def test_four_families_share_existing_etl(self):
        names = []
        for family in (1,2,3,4):
            name = f"f{family}.xlsx"
            names.append(name)
            self.source(name=name, family=family, rows=[(2, record(family=family, route=f"F{family}"), False)])
        self.execute(fuentes_en_orden=list(reversed(names)), geografia_permitida=None)
        self.assertEqual(len(self.rows()), 1)
        self.assertEqual(self.rows()[0]["ruta_prevalente"], "F4")
        self.assertEqual(self.rows()[0]["ocurrencias"], "4")

    def test_outside_approved_area_is_identified_but_not_admitted(self):
        self.source(rows=[(2, record(coord="2.5N 117W"), False)])
        m = self.execute()
        self.assertEqual(self.rows()[0]["admision_geografica"], "REVISAR_FUERA_AMBITO")
        self.assertEqual(self.rows()[0]["apto_csv_01"], "NO")
        self.assertEqual(m["conteos"]["filas_csv_00"], 1)
        self.assertEqual(m["conteos"]["filas_csv_01"], 0)

    def test_reproducible_all_bytes_hashes_and_stable_element_id(self):
        self.source()
        first = self.execute(geografia_permitida=None)
        before = {p.name:p.read_bytes() for p in (self.audit.path / "salida").iterdir()}
        second = self.execute()
        self.assertEqual(first, second)
        self.assertEqual(before, {p.name:p.read_bytes() for p in (self.audit.path / "salida").iterdir()})
        pending_id = self.rows()[0]["elemento_id"]
        self.execute(geografia_permitida=GEO)
        self.assertEqual(self.rows()[0]["elemento_id"], pending_id)
        self.assertEqual(self.rows()[0]["apto_csv_01"], "SI")

    def test_legacy_reporting_exact_bytes_except_additive_counts(self):
        # Oráculo independiente: reporting.py real del commit anterior, no una
        # reescritura del contrato actual. Solo se lee con git show.
        previous_source = subprocess.check_output(["git", "show", "7baa82c:AuditoriaCFE/src/auditoriacfe/reporting.py"], cwd=PROJECT.parent).decode("utf-8")
        legacy = types.ModuleType("auditoriacfe._legacy_reporting")
        legacy.__package__ = "auditoriacfe"
        exec(compile(previous_source, "reporting_7baa82c.py", "exec"), legacy.__dict__)
        path = self.source(rows=[(2, record(), False), (3, record(), False), (4, record(coord="MALO"), False)])
        self.audit.save()
        cfg = config.load(self.audit.path)
        records, profiles, auxiliary = extract(path, "a.xlsx", sha256(path))
        prepare(records, cfg)
        uniques = consolidate(records, self.audit.path.name)
        for projected in (None, [[r["elemento_id"], r["ruta_salida"], r["tipo_canonico"], r["latitud"], r["longitud"], 500000, 3595859, "EPSG:32611"] for r in uniques]):
            stages = [self.audit.path / "temporales" / n for n in ("old", "new")]
            for stage, module in zip(stages, (legacy, reporting)):
                stage.mkdir(parents=True, exist_ok=True)
                module.generate(stage, records, uniques, self.audit.path.name, None, None,
                                {"maestro":None,"baseline":None}, projected, [], profiles, auxiliary, [])
            old, new = stages
            for file in old.iterdir():
                if file.name != "resumen_conteos.csv":
                    self.assertEqual(file.read_bytes(), (new / file.name).read_bytes(), file.name)
            old_counts, new_counts = legacy.counts(records, uniques), reporting.counts(records, uniques, projected)
            self.assertTrue(all(new_counts[k] == v for k,v in old_counts.items()))
            self.assertEqual(new_counts["filas_csv_02"], len(projected or []))

    def test_isolated_elements_are_not_distance_filtered(self):
        self.source(rows=[(2, record(coord="32.1N 117W"), False), (3, record(coord="32.9N 117W"), False)])
        self.execute(geografia_permitida=None)
        self.assertEqual(len(self.rows()), 2)

    def test_count_invariants_reject_orphan_group(self):
        path = self.source()
        self.audit.save()
        records, _, _ = extract(path, "a.xlsx", sha256(path))
        prepare(records, config.load(self.audit.path))
        uniques = consolidate(records, self.audit.path.name)
        self.assertEqual(len(identified_groups(records)), 1)
        records[0]["prevalente_id"] = "NO_EXISTE"
        with self.assertRaises(PipelineError):
            reporting.counts(records, uniques)


if __name__ == "__main__":
    unittest.main()
