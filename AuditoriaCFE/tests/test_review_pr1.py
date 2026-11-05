import unittest
import json
import shutil
import zipfile
from xml.etree import ElementTree as ET
from unittest.mock import patch
from support import AuditFixture
from auditoriacfe.cli import main
from support import xlsx
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import recover,verify
from auditoriacfe.util import PipelineError,sha256


class ReviewPR1Tests(unittest.TestCase):
    def test_preparation_is_scoped_before_any_writes(self):
        fixture=AuditFixture();self.addCleanup(fixture.close)
        with patch('auditoriacfe.intake.bootstrap',return_value={}) as boot, patch('auditoriacfe.intake.prepare_master',return_value={}) as master, patch('auditoriacfe.cli.run',return_value={}), patch('auditoriacfe.cad.prepare_copy'):
            self.assertEqual(main(['--auditoria',fixture.path.name,'--preparar-entradas']),0)
        boot.assert_called_once_with([fixture.path.name])
        master.assert_called_once_with([fixture.path.name])

    def fixture(self,**cfg):
        f=AuditFixture();self.addCleanup(f.close)
        xlsx(f.path/'entrada/a.xlsx');f.save(**cfg)
        return f

    def test_xlsx_reconciles_text_security_and_binary_determinism(self):
        f=self.fixture(pipeline_integral=True,schema_02=1,geografia_permitida=None)
        first=run(f.path,emit=lambda *a:None);second=run(f.path,emit=lambda *a:None)
        self.assertEqual(first,second)
        from auditoriacfe.traceability import NAMES,workbook
        for name,sheets in zip(NAMES,(6,7)):
            self.assertIn(name,first['artefactos'])
            with zipfile.ZipFile(f.path/'salida'/name) as z:
                members=[n for n in z.namelist() if n.startswith('xl/worksheets/')]
                self.assertEqual(len(members),sheets)
                for n in members:
                    root=ET.fromstring(z.read(n));ns={'s':root.tag.split('}')[0][1:]}
                    self.assertFalse(root.findall('.//s:f',ns))
                    self.assertTrue(all(c.get('t')=='inlineStr' for c in root.findall('.//s:c',ns)))
                    self.assertIsNotNone(root.find('s:autoFilter',ns))
                    self.assertIsNotNone(root.find('.//s:pane',ns))
        p=f.path/'literal.xlsx';workbook(p,[('Text',[['value'],['=HYPERLINK("evil")'],['32.12345678901234567890']])])
        with zipfile.ZipFile(p) as z:
            xml=z.read('xl/worksheets/sheet1.xml').decode()
            self.assertIn('32.12345678901234567890',xml);self.assertNotIn('<f>',xml)

    def test_csv_version_and_integral_switch_are_independent(self):
        for schema,enabled in ((1,True),(2,False)):
            with self.subTest(schema=schema):
                f=self.fixture(schema_02=schema,pipeline_integral=enabled)
                m=run(f.path,emit=lambda *a:None)
                self.assertEqual(m['schema_version']['02'],schema)
                self.assertEqual(m['schema_version']['manifiesto'],2 if enabled else 1)
                self.assertEqual('01_trazabilidad_limpieza.xlsx' in m['artefactos'],enabled)

    def test_recovery_both_directories_preserves_invalid_mutable_work(self):
        f=self.fixture(pipeline_integral=True)
        first=run(f.path,emit=lambda *a:None)
        out=f.path/'salida';previous=f.path/'temporales/salida_anterior'
        shutil.copytree(out,previous)
        (out/'00_elementos_unificados.csv').write_text('corrupted')
        (out/'operator_note.txt').write_text('PRESERVE')
        from auditoriacfe.reporting import audit_lock
        with audit_lock(f.path):recover(f.path)
        self.assertEqual(first,verify(f.path))
        quarantines=list((f.path/'temporales').glob('salida_cuarentena_*'))
        self.assertEqual(len(quarantines),1)
        self.assertEqual((quarantines[0]/'operator_note.txt').read_text(),'PRESERVE')

    def test_recovery_invalid_candidates_never_deletes_them(self):
        f=self.fixture(pipeline_integral=True)
        run(f.path,emit=lambda *a:None)
        out=f.path/'salida';previous=f.path/'temporales/salida_anterior'
        shutil.copytree(out,previous)
        for folder in (out,previous):(folder/'00_elementos_unificados.csv').write_text('corrupted')
        with self.assertRaises(PipelineError):recover(f.path)
        self.assertTrue(out.exists() and previous.exists())

    def test_native_integrity_independent_from_immutable_package(self):
        f=self.fixture(pipeline_integral=True);m=run(f.path,emit=lambda *a:None)
        from auditoriacfe.native_evidence import verify_native
        with self.assertRaises(PipelineError):verify_native(f.path)
        root=f.path/'salida/resultados_cad';root.mkdir()
        drawing=root/'fake.dwg';drawing.write_bytes(b'FIXTURE')
        (root/'acta_evidencia_nativa.json').write_text(json.dumps(dict(schema='evidencia-nativa-v1',ejecucion_id=m['ejecucion_id'],resultado='SOLO_FIXTURE',archivos=[dict(archivo='fake.dwg',sha256=sha256(drawing),bytes=7)])))
        self.assertEqual(verify_native(f.path)['integridad'],'OK')
        drawing.write_bytes(b'EDITED')
        self.assertEqual(verify(f.path),m)
        with self.assertRaises(PipelineError):verify_native(f.path)

    def test_intake_snapshot_unselected_directories_unchanged(self):
        import tempfile
        from pathlib import Path
        from auditoriacfe.intake import bootstrap,prepare_master
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);audits=root/'project/auditorias';audits.mkdir(parents=True)
            for name in ('Mirador','Natura','Otay-Florido','Tijuana-General'):
                (audits/name).mkdir();(audits/name/'owner.txt').write_text(name)
            def snap():
                return {str(p.relative_to(audits)):(sha256(p),p.stat().st_mtime_ns) for p in audits.rglob('*') if p.is_file() and 'Mirador' not in p.parts}
            before=snap()
            with patch('auditoriacfe.intake.PROJECT',root/'project'),patch('auditoriacfe.intake.AUDITS',audits):
                bootstrap(['Mirador']);prepare_master(['Mirador'])
            self.assertEqual(snap(),before)

    def test_cajetin_mapping_is_attribute_based_and_no_second_type_table(self):
        from auditoriacfe.cad import RUNTIME,static_check
        source=RUNTIME.read_text(encoding='utf-8')
        self.assertTrue(static_check(source))
        for tag in ('TOTAL_POSTES','TOTAL_CAJAS','TOTAL_EXCEDENTES'):
            self.assertIn(tag,source)
        self.assertIn('(cons 410 datra:*layout*)',source)
        self.assertIn('PENDIENTE_AJUSTE_PLANTILLA',source)
        self.assertNotIn('(datra:text "TIPOS"',source)
        self.assertIn('datra:restore snapshot',source)
        self.assertIn('(or datra:*failure* (vl-catch-all-error-p result))',source)

    def test_private_evidence_zip_explicit_inventory_hashes_and_determinism(self):
        import tempfile
        from pathlib import Path
        from auditoriacfe.evidence_package import REQUIRED,build,verify_package
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);stage=root/'stage';stage.mkdir()
            origins={name:'SOLO_FIXTURE_SINTETICO' for name in REQUIRED}
            for name in REQUIRED:
                p=stage/name;p.parent.mkdir(exist_ok=True);p.write_text('SYNTHETIC '+name)
            (stage/'PRIVATE_SOURCE.kmz').write_bytes(b'NEVER_INCLUDE')
            a=root/'a.zip';b=root/'b.zip'
            build(stage,a,dict(commit='FIXTURE'),origins);build(stage,b,dict(commit='FIXTURE'),origins)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            self.assertEqual(verify_package(a)['commit'],'FIXTURE')
            with zipfile.ZipFile(a,'a') as z:z.writestr('PRIVATE_SOURCE.kmz',b'PRIVATE')
            with self.assertRaises(PipelineError):verify_package(a)

    def test_large_graph_is_referenced_not_squeezed_into_summary_cell(self):
        f=self.fixture(pipeline_integral=True)
        m=run(f.path,emit=lambda *a:None)
        out=f.path/'salida';stage=f.path/'large';shutil.copytree(out,stage)
        graph=dict(estado='SOLO_PUNTOS_PRELIMINAR',aislados=['FICTICIO-'+str(i) for i in range(10000)])
        m['topologia_detalle']=graph
        path=stage/'reporte_topologia.json';path.write_text(json.dumps(graph))
        checksum=sha256(path)
        from auditoriacfe.traceability import generate_workbooks
        generate_workbooks(stage,m,[])
        self.assertEqual(sha256(path),checksum)
        with zipfile.ZipFile(stage/'02_trazabilidad_transformacion.xlsx') as z:
            summary=z.read('xl/worksheets/sheet1.xml').decode()
            self.assertIn('reporte_topologia.json',summary)
            self.assertNotIn('FICTICIO-',summary)
