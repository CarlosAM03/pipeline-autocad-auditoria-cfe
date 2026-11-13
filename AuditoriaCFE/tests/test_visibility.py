import csv
import json
import unittest

from support import AuditFixture, record, xlsx
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import verify
from auditoriacfe.spatial_experiment import GEOD
from auditoriacfe.visibility import effective_radius
from auditoriacfe.util import PipelineError


class VisibilityTests(unittest.TestCase):
    def test_scope_default_override_and_legacy(self):
        self.assertEqual(effective_radius('Natura',True,{'presentacion':{}}),300)
        self.assertEqual(effective_radius('Mirador',True,{'presentacion':{},'radio_visibilidad_m':175}),175)
        for name,diagnostic,cad in [('Otro',True,{'presentacion':{}}),('Natura',False,{'presentacion':{}}),
                                    ('Natura',True,{}),('Natura',True,{'presentacion':{},'radio_visibilidad_m':None})]:
            self.assertIsNone(effective_radius(name,diagnostic,cad))
        for bad in (True,0,-5,50.5,'300'):
            with self.assertRaises(PipelineError):
                effective_radius('Natura',True,{'presentacion':{},'radio_visibilidad_m':bad})

    def test_pipeline_visibility_does_not_change_inventory(self):
        fixture=AuditFixture()
        self.addCleanup(fixture.close)
        audit=fixture.path/'Natura'
        entry=audit/'entrada'
        entry.mkdir(parents=True)
        cells=[]
        for i,meters in enumerate((0,40,80,120,160,200,2000),2):
            lon,lat,_=GEOD.fwd(-117,32.5,90,meters)
            cells.append((i,record(coord=f'{lat:.12f}N {abs(lon):.12f}W'),False))
        xlsx(entry/'a.xlsx',rows=cells)
        (entry/'base.dwg').write_bytes(b'fixture')
        cfg=dict(auditoria='Natura',fuentes_en_orden=['a.xlsx'],schema_02=2,diagnostico=True,
                 cad=dict(copia=True,base_dwg='base.dwg',presentacion={}))
        def execute():
            (audit/'configuracion.json').write_text(json.dumps(cfg),encoding='utf-8')
            result=run(audit,emit=lambda _:None)
            self.assertEqual(verify(audit),result)
            return result
        out=audit/'salida'
        first=execute()
        self.assertEqual(first['cad']['visibilidad']['radio_m'],300)
        self.assertEqual(first['cad']['elementos'],6)
        self.assertEqual(first['cad']['visibilidad']['no_representados'],1)
        self.assertEqual(first['conteos']['filas_csv_00'],7)
        self.assertEqual(first['conteos']['filas_csv_01'],0)
        with (out/'COORDENADAS_DESCARTADAS_VISUALIZACION.csv').open(encoding='utf-8',newline='') as f:
            excluded=list(csv.DictReader(f))
        self.assertEqual(len(excluded),1)
        self.assertEqual(excluded[0]['motivo_exclusion'],'MICROCOMPONENTE_ESPACIAL')
        self.assertEqual(excluded[0]['variante_radio_m'],'300')
        self.assertEqual(excluded[0]['archivo_fuente'],'a.xlsx')
        protected={n:(out/n).read_bytes() for n in ('00_elementos_unificados.csv','01_elementos_normalizados.csv',
                   '02_DIAGNOSTICO_NO_VERIFICADO.csv','linaje_y_calidad.jsonl')}
        cfg['cad']['radio_visibilidad_m']=20
        second=execute()
        self.assertEqual(second['cad']['elementos'],0)
        self.assertEqual(second['cad']['visibilidad']['no_representados'],7)
        for name,data in protected.items():
            self.assertEqual((out/name).read_bytes(),data)
        cfg['cad']['radio_visibilidad_m']=None
        third=execute()
        self.assertEqual(third['cad']['elementos'],7)
        self.assertNotIn('visibilidad',third['cad'])
        self.assertFalse((out/'DECISIONES_VISUALIZACION.csv').exists())
