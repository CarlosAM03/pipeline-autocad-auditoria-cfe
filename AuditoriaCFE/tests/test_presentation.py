import csv
import json
import unittest
from collections import Counter
from itertools import combinations

from support import AuditFixture, record, xlsx
from auditoriacfe.intake import BOMBEROS, SOURCES
from auditoriacfe.pipeline import run
from auditoriacfe.presentation import Profile, overlaps, plan
from auditoriacfe.reporting import verify
from auditoriacfe.util import PipelineError


class PresentationTests(unittest.TestCase):
    def test_partitions_include_extremes_and_coincident_points(self):
        points = [dict(id=str(i),x=i if i<100 else 10000,y=i%4,geo='32.500N 117.000W',label=f'P-{i}',tipo='POSTE')
                  for i in range(102)]
        profile = Profile.parse({})
        pages = plan(points,profile,'DATRA_A1')
        self.assertEqual(pages,plan(list(reversed(points)),profile,'DATRA_A1'))
        self.assertEqual(pages[0]['vista'],'GENERAL')
        self.assertEqual(pages[0]['bbox'][-2],10000)
        sectors = pages[0]['sectores']
        self.assertEqual(len(sectors),len(pages)-1)
        self.assertFalse(any(overlaps(a['caja'],b['caja']) for a,b in combinations(sectors,2)))
        assigned = []
        for page in pages:
            labels = page['etiquetas']
            assigned.extend(item['id'] for item in labels)
            self.assertFalse(any(overlaps(a['caja'],b['caja']) for a,b in combinations(labels,2)))
        self.assertEqual(Counter(assigned),Counter(p['id'] for p in points))

    def test_independent_symbol_text_and_camera_parameters(self):
        points = [dict(id='P',x=200,y=150,geo='32.500N 117.000W',label='P-7',tipo='POSTE')]
        large = plan(points,Profile.parse(dict(poste_mm=2,coordenada_mm=2)),'DATRA_A1')[0]
        small = plan(points,Profile.parse(dict(poste_mm=1,coordenada_mm=2)),'DATRA_A1')[0]
        self.assertEqual(large['centro'],small['centro'])
        self.assertEqual(large['etiquetas'],small['etiquetas'])
        self.assertEqual(small['simbolos_mm']['POSTE'],1)
        for cfg in (dict(poste_mm=float('inf')),dict(escala_detalle=True),dict(margen_mm=-1),dict(otra=1)):
            with self.assertRaises(PipelineError):
                Profile.parse(cfg)

    def test_bomberos_precedence_linaje_and_cad_index(self):
        self.assertEqual([name for name,sources in SOURCES.items() if any(s.endswith(BOMBEROS) for s in sources)],['Otay-Florido'])
        self.assertTrue(SOURCES['Otay-Florido'][-1].endswith(BOMBEROS))
        fixture=AuditFixture()
        self.addCleanup(fixture.close)
        audit=fixture.path
        xlsx(audit/'entrada/a.xlsx',rows=[(2,record(route='Base'),False)])
        xlsx(audit/'entrada'/BOMBEROS,rows=[(2,record(route='Bomberos'),False),
                                          (3,record(route='Bomberos',coord='32.600N 117.000W'),False)])
        (audit/'entrada/base.dwg').write_bytes(b'FAKE')
        fixture.save(fuentes_en_orden=['a.xlsx',BOMBEROS],schema_02=2,geografia_permitida=None,
                     cad=dict(base_dwg='base.dwg',copia=True,presentacion={}))
        manifest=run(audit,diagnostico=True,emit=lambda _:None)
        self.assertEqual(verify(audit),manifest)
        self.assertEqual(manifest['conteos']['ocurrencias'],3)
        self.assertEqual(manifest['conteos']['DUPLICADO'],1)
        self.assertEqual(manifest['conteos']['filas_csv_00'],2)
        self.assertEqual(manifest['conteos']['filas_csv_01'],0)
        out=audit/'salida'
        occurrences=[r for line in (out/'linaje_y_calidad.jsonl').read_text(encoding='utf-8').splitlines()
                     if BOMBEROS in line for r in [json.loads(line)]]
        self.assertEqual(len(occurrences),2)
        self.assertIn('Bomberos',(out/'asociaciones_elemento_ruta.csv').read_text(encoding='utf-8'))
        self.assertEqual(len(list(out.glob('*.scr'))),2)
        self.assertFalse((out/'02_elementos_proyectados.csv').exists())
        with (out/'indice_presentacion.csv').open(encoding='utf-8',newline='') as f:
            index=list(csv.DictReader(f))
        self.assertEqual(len({r['elemento_id'] for r in index}),2)
        self.assertGreater(len({r['pagina'] for r in index}),1)
        self.assertIn('cad_presentation.lsp',manifest['artefactos'])
