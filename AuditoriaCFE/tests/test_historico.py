"""Regresión readonly de rutas EXACTAS declaradas en diagnóstico (sin búsquedas).

Si el repositorio se distribuye sin originales, se omite explícitamente esta
clase; jamás se simula aprobación. No ejecuta archivos históricos.
"""
import csv
import re
import unittest
from collections import Counter

from support import PROJECT
from auditoriacfe.coordinates import parse
from auditoriacfe.quality import TYPES
from auditoriacfe.schemas import extract
from auditoriacfe.util import PipelineError, decimal_key, sha256

HISTORY = PROJECT.parent / "Auditorias-20261104T035633Z-1-001"
RAW = HISTORY / "postes"
BASE = "CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/"
MIR = BASE + "Mirador/"
OTAY = BASE + "Otay - Florido/"
STD = MIR + "STD HACIA CNAL 12.xlsx"
CANAL = MIR + "Ruta canal 12 level antes 2014 Completo.xlsx"
COPY = MIR + "Copy of STD HACIA CNAL 12.xlsx"
VIA = OTAY + "ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx"
FLO = OTAY + "RUTA FLO-OTAY FO96 final.xlsx"
CIVIL = OTAY + "ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx"
SOURCES = {"CFE FLO-OTAY-BOMBEROS.xlsx": 494, "CFE Natura  - Datra/Natura  - Datra.xlsx": 507,
           COPY: 181, CANAL: 347, STD: 204, FLO: 622, CIVIL: 303, VIA: 44, "Postes_CFE.xlsx": 4341}
CSVS = {"STD-MIRADOR.csv": "46c62d0670e715dae2e0b9a4a306e591c2cbf98a066797f6b8d9aa0d5e583a17",
        "STD-OTAY-FLORIDO.csv": "aa509d2928f9a51133f6b8e25d683411067ba7a1d97ed0cfbfa4c7a08510cf56"}
AVAILABLE = all((RAW / n).is_file() for n in SOURCES) and all((HISTORY / "Auditorias" / n).is_file() for n in CSVS)


@unittest.skipUnless(AVAILABLE, "Originales históricos exactos no disponibles; regresión NO ejecutada")
class HistoricalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records, cls.profiles = {}, []
        cls.hashes = {}
        inventory = (PROJECT / "Codex/00_Diagnostico/01_Excel_Origen/01_inventario_xlsx.md").read_text(encoding="utf-8")
        expected = dict(re.findall(r"\| ([^|]+\.xlsx) \| `([0-9a-f]{64})`", inventory))
        for name in SOURCES:
            path = RAW / name
            before = sha256(path)
            if before != expected[name]:
                raise AssertionError(f"Hash histórico no coincide con diagnóstico: {name}")
            sheets = ["Sheet1", "Sheet2"] if name == COPY else None
            exceptions = {"Hoja1": "F3_D_VACIA"} if name == CANAL else None
            records, profiles, aux = extract(path, name, before, sheets, exceptions)
            cls.records[name] = records
            cls.profiles.extend(profiles)
            cls.hashes[name] = before
            if sha256(path) != before:
                raise AssertionError("Fuente histórica alterada")

    @classmethod
    def tearDownClass(cls):
        for name, before in cls.hashes.items():
            if sha256(RAW / name) != before:
                raise AssertionError("Fuente histórica alterada durante tests")

    def triples(self, names):
        return [(r["ruta_original"], r["tipo_original"], r["coordenada_original"]) for name in names for r in self.records[name]]

    def historical(self, name):
        path = HISTORY / "Auditorias" / name
        self.assertEqual(sha256(path), CSVS[name])
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = [tuple(row) for row in csv.reader(stream) if any(row)]
        if rows[0] == ("Ruta", "Elemento de Red", "Coordenadas"):
            rows.pop(0)
        return rows

    def test_nine_originals_four_families_and_7043_occurrences(self):
        self.assertEqual({name: len(rows) for name, rows in self.records.items()}, SOURCES)
        self.assertEqual(sum(len(r) for r in self.records.values()), 7043)
        self.assertEqual({p["familia"] for p in self.profiles}, {"F1_NOMBRE_ABC", "F2_RUTA_ABC_FOTO_D", "F3_NUMERO_BCD", "F4_DESPLAZADO_BCD", "VACIA"})
        self.assertEqual(sum(p["filas_xml"] for p in self.profiles), 1058886)
        self.assertEqual(sum(p["formulas"] for p in self.profiles), 6175)
        self.assertEqual(sum(r["oculta"] for r in self.records[COPY]), 44)
        self.assertEqual(len({r["ruta_original"] for r in self.records["CFE Natura  - Datra/Natura  - Datra.xlsx"]}), 14)

    def test_mirador_551_literal_and_56_repetitions(self):
        extracted = self.triples([STD, CANAL])
        historical = self.historical("STD-MIRADOR.csv")
        self.assertEqual(len(extracted), 551)
        self.assertEqual(extracted, historical)
        self.assertEqual(len(extracted) - len(set(extracted)), 56)

    def test_otay_969_one_spacing_difference_and_218_repetitions(self):
        extracted = self.triples([VIA, FLO, CIVIL])
        historical = self.historical("STD-OTAY-FLORIDO.csv")
        self.assertEqual(len(extracted), 969)
        differences = [i for i, pair in enumerate(zip(extracted, historical), 1) if pair[0] != pair[1]]
        self.assertEqual(differences, [731])
        normalize = lambda rs: [(a, b, " ".join(c.split())) for a, b, c in rs]
        self.assertEqual(normalize(extracted), normalize(historical))
        self.assertEqual(len(historical) - len(set(historical)), 218)

    def test_new_quality_does_not_approve_historical_errors(self):
        result = Counter()
        for rows in self.records.values():
            for r in rows:
                try:
                    parse(r["coordenada_original"])
                    result["mundo_interpretable"] += 1
                except PipelineError as exc:
                    result[str(exc)] += 1
        self.assertEqual(result, {"mundo_interpretable": 7020, "COORD_FUERA_RANGO": 10, "COORD_NO_INTERPRETABLE": 13})
        # Diagnóstico de identidad exacta, ANTES de admisión local: no equivale
        # a exportables ni acredita perímetro. No se redondea ni filtra por distancia.
        for names in ([STD, CANAL], [VIA, FLO, CIVIL]):
            counts, rejected, outside = Counter(), 0, 0
            for name in names:
                for r in self.records[name]:
                    if r["tipo_original"].casefold() == "registro":
                        outside += 1
                        continue
                    try:
                        lat, lon = parse(r["coordenada_original"])
                    except PipelineError:
                        rejected += 1
                        continue
                    counts[(TYPES[r["tipo_original"].casefold()], decimal_key(lat), decimal_key(lon))] += 1
            print(f"\nIdentidad sin aprobar ámbito {'Mirador' if names[0] == STD else 'Otay'}: únicos={len(counts)}, duplicados={sum(counts.values()) - len(counts)}, rechazados={rejected}, fuera_alcance={outside}")


if __name__ == "__main__":
    unittest.main()
