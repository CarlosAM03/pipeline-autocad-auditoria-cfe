import csv
import json
import unittest
from support import AuditFixture, GEO, record, xlsx
from auditoriacfe.pipeline import run
from auditoriacfe.resolutions import HEADER
from auditoriacfe.util import sha256, PipelineError


class CP01IntegralTests(unittest.TestCase):
    def setUp(self):
        self.audit=AuditFixture()
        self.addCleanup(self.audit.close)

    def source(self,rows=None):
        return xlsx(self.audit.path/'entrada/a.xlsx',rows=rows)

    def execute(self,**cfg):
        self.audit.save(**cfg)
        return run(self.audit.path,emit=lambda *a:None)

    def resolutions(self,action,new='',original='MALO',field='coordenada',**extra):
        r=dict(resolucion_id='R1',archivo_sha256=sha256(self.audit.path/'entrada/a.xlsx'),archivo_relativo='a.xlsx',
               hoja='Datos',fila='2',valor_original=original,campo=field,accion=action,valor_nuevo=new,
               motivo='fixture',evidencia='fuente TEST',responsable='owner TEST',fecha='2026-11-05',aprobada='true')
        r.update(extra)
        with (self.audit.path/'entrada/resoluciones_manual.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,HEADER);w.writeheader();w.writerow(r)

    def test_correction_preserves_raw_and_source(self):
        p=self.source([(2,record(coord='MALO'),False)])
        before=sha256(p)
        self.resolutions('CORREGIR_COORDENADA','32.5N 117W')
        m=self.execute()
        row=json.loads((self.audit.path/'salida/linaje_y_calidad.jsonl').read_text(encoding='utf-8'))
        self.assertEqual(row['coordenada_original'],'MALO')
        self.assertEqual(row['coordenada_normalizada'],'32.5N 117W')
        self.assertEqual(m['conteos']['VALIDO'],1)
        self.assertEqual(before,sha256(p))

    def test_exclusion_stays_in_review(self):
        self.source([(2,record(coord='MALO'),False)])
        self.resolutions('EXCLUIR',field='registro')
        m=self.execute()
        self.assertEqual(m['conteos']['RECHAZADO'],1)
        self.assertEqual(m['conteos']['filas_csv_00'],0)
        self.assertIn('EXCLUSION_MANUAL',(self.audit.path/'salida/00_elementos_revision.csv').read_text(encoding='utf-8'))

    def test_wrong_hash_original_and_unapproved(self):
        self.source([(2,record(coord='MALO'),False)])
        self.resolutions('CORREGIR_COORDENADA','32.5N 117W',archivo_sha256='0'*64)
        with self.assertRaises(PipelineError):self.execute()
        self.resolutions('CORREGIR_COORDENADA','32.5N 117W',aprobada='false')
        self.assertEqual(self.execute()['conteos']['RECHAZADO'],1)

    def test_types_equivalences(self):
        self.source([(2,record(typ='Caja de Empalme'),False),(3,record(typ='CAJA_DEMPALME'),False),(4,record(typ='Postes'),False)])
        m=self.execute()
        self.assertEqual(m['conteos']['CAJA_EMP'],1)
        self.assertEqual(m['conteos']['POSTE'],1)
        self.assertEqual(m['conteos']['DUPLICADO'],1)

    def area(self,geometry):
        (self.audit.path/'entrada/area.geojson').write_text(json.dumps(geometry),encoding='utf-8')
        return dict(archivo='area.geojson',aprobada=True,crs='EPSG:4326',version='TEST-v1',
                    responsable='TEST',fecha='2026-11-05',evidencia='TEST only')

    def test_polygon_hole_boundary_and_outside(self):
        self.source([(2,record(coord='32.1N 117.9W'),False),(3,record(coord='32.5N 117W'),False),(4,record(coord='32N 118W'),False)])
        geo=self.area(dict(type='Polygon',coordinates=[[[-118,32],[-116,32],[-116,33],[-118,33],[-118,32]],
                                                       [[-117.2,32.3],[-116.8,32.3],[-116.8,32.7],[-117.2,32.7],[-117.2,32.3]]]))
        m=self.execute(geografia_permitida=geo)
        self.assertEqual(m['conteos']['VALIDO'],2)
        self.assertEqual(m['conteos']['REVISAR'],1)

    def test_invalid_polygon_and_unapproved(self):
        self.source()
        geo=self.area(dict(type='Polygon',coordinates=[[[-118,32],[-116,33],[-118,33],[-116,32],[-118,32]]]))
        with self.assertRaises(PipelineError):self.execute(geografia_permitida=geo)
        geo=self.area(dict(type='Polygon',coordinates=[[[-118,32],[-116,32],[-116,33],[-118,33],[-118,32]]]))
        geo['aprobada']=False
        self.assertEqual(self.execute(geografia_permitida=geo)['conteos']['VALIDO'],0)

    def test_corridor_and_exception(self):
        self.source()
        geo=self.area(dict(type='LineString',coordinates=[[-117,32.4],[-117,32.6]]))
        geo['corredor_m']=20
        self.assertEqual(self.execute(geografia_permitida=geo)['conteos']['VALIDO'],1)
        self.resolutions('EXCEPCION_AMBITO',field='ambito',original='32.500000N 117.000000W')
        self.assertEqual(self.execute(geografia_permitida=None)['conteos']['VALIDO'],1)
