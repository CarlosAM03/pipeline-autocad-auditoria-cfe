import csv
import json
import os
import unittest
from unittest.mock import patch
from support import AuditFixture,GEO,xlsx
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import verify
from auditoriacfe.projection import read_projected, route_id
from auditoriacfe.util import PipelineError


class CP02IntegralTests(unittest.TestCase):
    def setUp(self):
        self.audit=AuditFixture();self.addCleanup(self.audit.close)
        xlsx(self.audit.path/'entrada/a.xlsx')

    def execute(self,**changes):
        self.audit.save(**changes)
        return run(self.audit.path,emit=lambda *a:None)

    def evidence(self):
        (self.audit.path/'control.txt').write_text('TEST ONLY',encoding='utf-8')
        return dict(archivo='control.txt',aprobado_por='TEST',fecha='2026-11-05',crs='EPSG:32611',unidades='m',tolerancia_m=0.01,
                    controles=[dict(latitud=0,longitud=-117,este_m=500000,norte_m=0),dict(latitud=1,longitud=-117,este_m=500000,norte_m=110530.15880237566)])

    def test_v1_v2_reader_and_true_route_id(self):
        self.execute(crs_validado=True,evidencia_crs=self.evidence())
        path=self.audit.path/'salida/02_elementos_proyectados.csv'
        first,version=read_projected(path,self.audit.path.name)
        self.assertEqual(version,1)
        m=self.execute(schema_02=2)
        second,version=read_projected(path,self.audit.path.name)
        self.assertEqual(version,2)
        self.assertEqual(first,second)
        self.assertEqual(second[0]['ruta_id'],route_id(self.audit.path.name,'Ruta'))
        self.assertEqual(m['schema_version']['02'],2)
        self.assertEqual(verify(self.audit.path),m)

    def test_legacy_manifest_migration_retains_history(self):
        first=self.execute()
        old_archive=(self.audit.path/'manifiestos'/(first['ejecucion_id']+'.json')).read_bytes()
        second=self.execute(schema_02=2)
        self.assertFalse((self.audit.path/'manifiesto_ejecucion.json').exists())
        self.assertEqual(old_archive,(self.audit.path/'salida/manifiestos'/(first['ejecucion_id']+'.json')).read_bytes())
        self.assertEqual(verify(self.audit.path),second)
        self.assertEqual(second,self.execute())

    def test_interruption_during_migration_restores_old_authority(self):
        first=self.execute()
        original=os.replace
        def fail(src,dst):
            if str(src).split(os.sep)[-1].startswith('proceso1_'):raise KeyboardInterrupt()
            return original(src,dst)
        with patch('auditoriacfe.reporting.os.replace',side_effect=fail), self.assertRaises(KeyboardInterrupt):
            self.execute(schema_02=2)
        self.assertEqual(verify(self.audit.path),first)

    def test_diagnostic_requires_copy_and_never_creates_productive_02(self):
        with self.assertRaises(PipelineError):self.execute(schema_02=2,diagnostico=True,geografia_permitida=None)
        (self.audit.path/'entrada/copy.dwg').write_bytes(b'CAD-FIXTURE-NOT-REAL')
        m=self.execute(cad=dict(base_dwg='copy.dwg',copia=True))
        self.assertFalse(m['crs_validado'])
        self.assertFalse((self.audit.path/'salida/02_elementos_proyectados.csv').exists())
        self.assertTrue((self.audit.path/'salida/02_DIAGNOSTICO_NO_VERIFICADO.csv').exists())
        self.assertEqual(m['diagnostico']['estado'],'DIAGNOSTICO_NO_VERIFICADO')

    def test_changed_input_or_manifest_is_rejected(self):
        self.execute(schema_02=2)
        (self.audit.path/'entrada/a.xlsx').write_bytes(b'CHANGED')
        with self.assertRaises(PipelineError):verify(self.audit.path)

    def test_retry_transient_windows_denial(self):
        original=os.replace;calls=[]
        def transient(src,dst):
            if not calls:
                calls.append(1);raise PermissionError('transient scanner')
            return original(src,dst)
        with patch('auditoriacfe.reporting.os.replace',side_effect=transient):
            m=self.execute(schema_02=2)
        self.assertEqual(verify(self.audit.path),m)
