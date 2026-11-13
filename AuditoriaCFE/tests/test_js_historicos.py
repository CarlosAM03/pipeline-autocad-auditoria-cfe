import shutil
import unittest

from audit_js_support import FILES, inspect_js
from auditoriacfe.coordinates import parse
from auditoriacfe.util import PipelineError


@unittest.skipUnless(all(p.is_file() for p in FILES) and shutil.which("node"), "Faltan históricos exactos o Node.js; auditoría JS NO ejecutada")
class HistoricalJSTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = inspect_js()

    def test_533_965_points_match_txt_order_and_geometry(self):
        for name, count in (("STD-MIRADOR",533), ("STD-OTAY-FLORIDO",965)):
            info = self.audit["txt"][name]
            self.assertEqual(info["points"], count)
            self.assertEqual(info["text"], count)
            self.assertEqual(info["pline"], 0)
            self.assertTrue(info["same_cardinality"])
            self.assertEqual(info["max_sequence_error_m"], 0)

    def test_actual_branch_returns_and_shortcuts(self):
        libraries = self.audit["libraries"]
        self.assertEqual(libraries["ordenar"]["branch"], [0,1,2,1,3,1,0])
        self.assertEqual(libraries["trayectoria"]["branch"], [0,1,2,3])
        self.assertEqual(libraries["trayectoria"]["STD-MIRADOR.csv"]["non_edges"], 13)
        self.assertEqual(libraries["trayectoria"]["STD-OTAY-FLORIDO.csv"]["non_edges"], 15)
        self.assertEqual(libraries["ordenar"]["STD-MIRADOR.csv"]["non_edges"], 0)

    def test_historical_parser_flaws_not_reintroduced(self):
        for library in self.audit["libraries"].values():
            self.assertIsNone(library["parser"][0])
            self.assertEqual(library["parser"][1]["lat"], 432.46444)
            self.assertEqual(library["parser"][2]["lat"], 32)
            self.assertEqual(library["parser"][3]["lat"], 32.5)
            self.assertEqual(library["quoted_count"], 0)
        self.assertEqual(str(parse("32.5N117W")[0]), "32.5")
        for text in ("432.464440N 116.8W", "32..5N 117W", "junk32.5N 117Wtail"):
            with self.assertRaises(PipelineError):
                parse(text)

    def test_legacy_projection_error_is_measured_not_compensated(self):
        from pyproj import Transformer
        transformer = Transformer.from_crs(4326, 32611, always_xy=True)
        for library in self.audit["libraries"].values():
            sample = library["projection"][0]
            x, y = transformer.transform(sample["lon"], sample["lat"], errcheck=True)
            self.assertAlmostEqual(sample["x"] - x, 0, places=8)
            self.assertAlmostEqual(sample["y"] - y, 11.479314342141151, places=6)

    def test_filter_thresholds_are_strict_and_not_identity(self):
        for name in ("generar", "trayectoria"):
            case = self.audit["libraries"][name]["thresholds"]
            self.assertEqual(case["filter500"], 0)
            self.assertEqual(case["filter1000"], 2)
            self.assertEqual(case["colocated"], 2)
        self.assertEqual(self.audit["libraries"]["ordenar"]["thresholds"]["graph120"], 0)
        self.assertEqual(self.audit["libraries"]["generar"]["thresholds"]["classifySubstring"], "P")


if __name__ == "__main__":
    unittest.main()
