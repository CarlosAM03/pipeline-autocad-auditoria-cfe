import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from auditoriacfe.cad import literal, static_check
from auditoriacfe.cad_review import RUNTIME, compile_review
from auditoriacfe.util import PipelineError


class ReviewTableTests(unittest.TestCase):
    def test_reconciles_counts_preserves_coordinate_text_and_gates_final(self):
        with TemporaryDirectory() as root:
            stage = Path(root)
            source = stage/'02_DIAGNOSTICO_NO_VERIFICADO.csv'
            source.write_text(
                'elemento_id,tipo,longitud,latitud\n'
                'P,POSTE,-117.000100,32.5000000\nE,EXCEDENTE,-117.21,32.23\n',
                encoding='utf-8')
            shown = [{'elemento_id': 'P', 'tipo': 'POSTE'}]
            spec = dict(fecha='09/11/2026', elaboro='Ejemplo', reviso='Ejemplo')
            visibility = dict(radio_m=300, decisiones_por_id={
                'P': {'incluido': True}, 'E': {'incluido': False}})
            code = compile_review(stage, spec, shown, visibility, literal)
            self.assertTrue(static_check(code))
            self.assertTrue(static_check(RUNTIME.read_text(encoding='utf-8')))
            self.assertIn('("TOTAL" 2 1 1)', code)
            with (stage/'anexo_coordenadas_revision.csv').open(encoding='utf-8', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]['LONGITUD [°]'], '-117.000100')
            self.assertEqual(rows[0]['LATITUD [°]'], '32.5000000')
            self.assertEqual(rows[1]['representado'], 'NO')
            with self.assertRaisesRegex(PipelineError, 'solo admite'):
                compile_review(stage, spec | {'estado': 'FINAL'}, shown, visibility, literal)
            with self.assertRaisesRegex(PipelineError, 'no reconciliado'):
                compile_review(stage, spec, [], visibility, literal)
            with self.assertRaisesRegex(PipelineError, '300 m'):
                compile_review(stage, spec, shown, visibility | {'radio_m': 200}, literal)
