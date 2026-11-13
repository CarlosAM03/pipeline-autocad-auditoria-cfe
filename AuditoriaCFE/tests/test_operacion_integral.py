import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from support import AuditFixture, xlsx, record, PROJECT
from auditoriacfe.batch import batch
from auditoriacfe.cli import main
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import verify
from auditoriacfe.util import PipelineError

sys.path.insert(0,str(PROJECT/'herramientas'))
from verificar_publicacion import violations


class OperationIntegralTests(unittest.TestCase):
    def setUp(self):
        self.audit=AuditFixture();self.addCleanup(self.audit.close)
        xlsx(self.audit.path/'entrada/a.xlsx')
        self.audit.save(schema_02=2)

    def test_batch_independent_failure_and_dry_run_no_writes(self):
        with patch('auditoriacfe.batch.config.audit_path',side_effect=[self.audit.path,self.audit.path/'MISSING']):
            result=batch(['ONE','TWO'],dry_run=True,emit=lambda *a:None)
        self.assertEqual(result['estado'],'FALLIDO')
        self.assertEqual(result['auditorias'][0]['estado'],'DRY_RUN')
        self.assertFalse((self.audit.path/'salida').exists())
        self.assertFalse((self.audit.path/'.proceso1.lock').exists())

    def test_batch_matches_individual_and_verify(self):
        first=run(self.audit.path,emit=lambda *a:None)
        with patch('auditoriacfe.batch.config.audit_path',return_value=self.audit.path):
            result=batch([self.audit.path.name],emit=lambda *a:None,persist=False)
            checked=batch([self.audit.path.name],verify_only=True,emit=lambda *a:None)
        self.assertEqual(result['auditorias'][0]['ejecucion_id'],first['ejecucion_id'])
        self.assertEqual(checked['auditorias'],result['auditorias'])

    def test_cli_mutually_exclusive_and_portable_help(self):
        self.assertEqual(main(['--batch','--auditoria','X']),2)
        self.assertEqual(main(['--batch','--entrada-prueba','X']),2)
        with self.assertRaises(SystemExit) as captured:main(['--help'])
        self.assertEqual(captured.exception.code,0)

    def test_config_mutation_blocks_consumption_but_allows_new_run(self):
        run(self.audit.path,emit=lambda *a:None)
        self.audit.save(cercanos_m=1)
        with self.assertRaises(PipelineError):verify(self.audit.path)
        current=run(self.audit.path,emit=lambda *a:None)
        self.assertEqual(current,verify(self.audit.path))

    def test_input_change_can_be_prepared_without_destroying_archive(self):
        first=run(self.audit.path,emit=lambda *a:None)
        xlsx(self.audit.path/'entrada/a.xlsx',rows=[(2,record(coord='32.6N117W'),False)])
        with self.assertRaises(PipelineError):verify(self.audit.path)
        current=run(self.audit.path,emit=lambda *a:None)
        self.assertNotEqual(first['ejecucion_id'],current['ejecucion_id'])
        self.assertTrue((self.audit.path/'salida/manifiestos'/(first['ejecucion_id']+'.json')).exists())
        self.assertEqual(current,verify(self.audit.path))

    def test_acta_checklist_failures_survive_next_run(self):
        m=run(self.audit.path,emit=lambda *a:None)
        out=self.audit.path/'salida'
        for name in ('acta_checkpoint.md','checklist_entrega.md'):self.assertIn(name,m['artefactos'])
        xlsx(self.audit.path/'entrada/a.xlsx',sheets=[('Unknown',[(1,{'A':'WRONG'},False)])])
        with self.assertRaises(PipelineError):run(self.audit.path,emit=lambda *a:None)
        files=list((out/'fallos').glob('*.json'));self.assertEqual(len(files),1)
        self.assertEqual(json.loads(files[0].read_text())['estado'],'FALLIDO')
        xlsx(self.audit.path/'entrada/a.xlsx')
        run(self.audit.path,emit=lambda *a:None)
        self.assertTrue((out/'fallos'/files[0].name).exists())

    def test_publication_guard_disallows_sensitive_paths(self):
        for name in ['AuditoriaCFE/auditorias/REAL/entrada/a.csv','AuditoriaCFE/auditorias/REAL/configuracion.json',
                     'AuditoriaCFE/recursos/new.dwg','a.kmz','a.xlsx','x/.venv/py.py','x/00_RESPUESTAS_ORIGINALES.md']:
            self.assertEqual(violations([name]),[name])
        self.assertFalse(violations(['AuditoriaCFE/src/auditoriacfe/cad.py','.github/workflows/pipeline.yml']))

    def test_post_publication_validation_failure_rolls_back(self):
        first=run(self.audit.path,emit=lambda *a:None)
        with patch('auditoriacfe.reporting.verify',side_effect=[first,PipelineError('simulated validation failure')]):
            with self.assertRaises(PipelineError):run(self.audit.path,emit=lambda *a:None)
        self.assertEqual(first,verify(self.audit.path))
