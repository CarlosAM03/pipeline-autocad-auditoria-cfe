import json
import unittest
from support import AuditFixture, record, xlsx
from auditoriacfe.cad import literal, number, package, prepare_copy, static_check, RASTER_NAMES, RUNTIME
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import verify, csv_file, PROJECTED_V2
from auditoriacfe.projection import route_id
from auditoriacfe.util import PipelineError


class CADIntegralTests(unittest.TestCase):
    def setUp(self):
        self.audit=AuditFixture(); self.addCleanup(self.audit.close)
        xlsx(self.audit.path/'entrada/a.xlsx')
        (self.audit.path/'entrada/base.dwg').write_bytes(b'CAD SYNTHETIC FIXTURE - NOT A DWG')
        self.spec=dict(base_dwg='base.dwg',copia=True,unidades_verificadas=False,layout='DATRA_A1')

    def execute(self,**changes):
        self.audit.save(schema_02=2,cad=self.spec,**changes)
        return run(self.audit.path,emit=lambda *a:None)

    def test_two_scripts_and_gate_without_02(self):
        m=self.execute()
        out=self.audit.path/'salida'
        self.assertEqual(len(list(out.glob('*.scr'))),2)
        self.assertNotIn('(datra:point ',(out/'01_configurar_plano.scr').read_text())
        self.assertNotIn('(datra:point ',(out/'02_dibujar_auditoria.scr').read_text())
        self.assertEqual(m['cad']['cp04'],'PENDIENTE_EVIDENCIA')
        self.assertFalse(m['cad']['unidades_acreditadas'])
        self.assertEqual(verify(self.audit.path),m)

    def test_diagnostic_points_labeled_not_productive(self):
        m=self.execute(diagnostico=True,geografia_permitida=None)
        out=self.audit.path/'salida'
        scr=(out/'cad_datos.lsp').read_text()
        self.assertIn('DIAGNOSTICO_NO_VERIFICADO',scr)
        self.assertEqual(scr.count('(datra:point '),1)
        self.assertNotIn('(datra:edge ',scr)
        self.assertFalse((out/'02_elementos_proyectados.csv').exists())
        self.assertEqual(m['cad']['elementos'],1)

    def test_cad_copy_preserved_and_hashes_reproducible(self):
        first=self.execute(diagnostico=True)
        target=prepare_copy(self.audit.path,first)
        self.assertEqual(target.read_bytes(),(self.audit.path/'entrada/base.dwg').read_bytes())
        target.write_bytes(b'OPERATOR EDITED COPY')
        second=self.execute(diagnostico=True)
        self.assertEqual(first,second)
        self.assertEqual(prepare_copy(self.audit.path,second).read_bytes(),b'OPERATOR EDITED COPY')
        self.assertEqual(verify(self.audit.path),second)
        self.assertEqual((self.audit.path/'entrada/base.dwg').read_bytes(),b'CAD SYNTHETIC FIXTURE - NOT A DWG')

    def test_literal_injection_numeric_and_static_validation(self):
        self.assertEqual(literal('x");(erase "all'), '"x\\");(erase \\"all"')
        for s in ['\n','\x00','\t']:
            with self.assertRaises(PipelineError):literal(s)
        for n in ['NaN','Inf','-Inf']:
            with self.assertRaises(PipelineError):number(n)
        for text in ['(foo','(foo))','("foo)']:
            with self.assertRaises(PipelineError):static_check(text)
        self.assertTrue(static_check(RUNTIME.read_text()))

    def test_raster_package_requires_both_sources_and_preserves_operator_files(self):
        self.spec['recursos_raster']=True
        entry=self.audit.path/'entrada'
        with self.assertRaisesRegex(PipelineError, 'Recurso raster CAD local ausente'):
            self.execute()
        for name in RASTER_NAMES:
            (entry/name).write_bytes(name.encode())
        manifest=self.execute()
        self.assertEqual(set(manifest['cad']['recursos_raster']),set(RASTER_NAMES))
        target=prepare_copy(self.audit.path,manifest)
        self.assertEqual(len(list((self.audit.path/'salida').glob('*.scr'))),2)
        for name in RASTER_NAMES:
            self.assertEqual((target.parent/name).read_bytes(),(entry/name).read_bytes())
        target.write_bytes(b'EDITED DWG')
        self.assertEqual(prepare_copy(self.audit.path,manifest).read_bytes(),b'EDITED DWG')
        edited=target.parent/RASTER_NAMES[0]
        edited.write_bytes(b'EDITED PNG')
        with self.assertRaisesRegex(PipelineError, 'Recurso raster existente distinto'):
            prepare_copy(self.audit.path,manifest)
        self.assertEqual(edited.read_bytes(),b'EDITED PNG')
        (entry/RASTER_NAMES[1]).write_bytes(b'ALTERED SOURCE')
        with self.assertRaisesRegex(PipelineError, 'Cambiaron los recursos raster'):
            prepare_copy(self.audit.path,manifest)

    def test_incompatible_cad_profile_rejected(self):
        for change in [dict(copia=False),dict(layout='Bad");(quit)'),dict(base_dwg='../outside.dwg')]:
            self.spec.update(change)
            with self.assertRaises(PipelineError):self.execute()
            self.spec=dict(base_dwg='base.dwg',copia=True,layout='DATRA_A1')

    def test_confirmed_edges_once_no_dfs_jumps_and_planar_distance(self):
        stage=self.audit.path/'stage';stage.mkdir()
        names=['A','B','C','D']
        rows=[[n,route_id(self.audit.path.name,'R'),'R','POSTE','32.5','-117',x,y,'EPSG:32611']
              for n,(x,y) in zip(names,[(0,0),(3,4),(6,4),(3,9)])]
        csv_file(stage/'02_elementos_proyectados.csv',PROJECTED_V2,rows)
        cfg=dict(cad={**self.spec,'unidades_verificadas':True},diagnostico=False)
        edges=[dict(arista_id=a+b,origen_id=a,destino_id=b,estado='CONFIRMADA',
                    evidencia='TEST ONLY',responsable='TEST',fecha_aprobacion='2026-11-05')
               for a,b in [('A','B'),('B','C'),('B','D'),('D','A'),('B','A')]]
        result=package(stage,self.audit.path,cfg,dict(estado='CONTROLES_VERIFICADOS'),edges)
        scr=(stage/'cad_datos.lsp').read_text()
        self.assertEqual(scr.count('(datra:edge '),4)
        self.assertIn('"5.00 m"',scr)
        self.assertNotIn('"CD"',scr)
        self.assertEqual(result['elementos'],4)
        self.assertEqual(result['aristas'],4)
        edges[0]['estado']='PROPUESTA'
        with self.assertRaises(PipelineError):package(stage,self.audit.path,cfg,dict(estado='CONTROLES_VERIFICADOS'),edges)

    def test_one_a1_and_no_automatic_human_acceptance(self):
        self.execute(diagnostico=True)
        paper=json.loads((self.audit.path/'salida/reporte_papel_A1.json').read_text())
        self.assertEqual(paper['laminas'],1)
        self.assertEqual(paper['orientacion'],'HORIZONTAL')
        self.assertIsNone(paper['evidencia_legibilidad'])
        self.assertEqual(paper['revision_nativa'],'PENDIENTE_EVIDENCIA')

    def test_native_runtime_preserves_map_and_uses_owner_id(self):
        runtime=RUNTIME.read_text()
        self.assertIn('DATRA_CFE',runtime)
        self.assertIn('(if (datra:owned entity) (entdel entity))',runtime)
        self.assertNotIn('PDMODE',runtime)
        self.assertNotIn('_.ERASE',runtime)
        self.assertIn('INSUNITS',runtime)
        self.assertIn('DATRACONTROLES',runtime)

    def test_large_program_short_scr_lines_and_packaged_data(self):
        stage=self.audit.path/'stage';stage.mkdir()
        rows=[[str(n),route_id(self.audit.path.name,'R'),'R','POSTE','32.5','-117',500000+n,3600000,'EPSG:32611'] for n in range(4200)]
        csv_file(stage/'02_elementos_proyectados.csv',PROJECTED_V2,rows)
        report=package(stage,self.audit.path,dict(cad={**self.spec,'unidades_verificadas':True},diagnostico=False),dict(estado='CONTROLES_VERIFICADOS'),[])
        self.assertEqual(report['elementos'],4200)
        script=(stage/'02_dibujar_auditoria.scr').read_text()
        self.assertLess(max(map(len,script.splitlines())),512)
        self.assertIn('cad_datos.lsp',script)
        self.assertEqual((stage/'cad_datos.lsp').read_text().count('(datra:point '),4200)
