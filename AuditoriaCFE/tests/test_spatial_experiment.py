import tempfile
import unittest
from pathlib import Path

import support
from auditoriacfe.cad import package
from auditoriacfe.geofence import contains
from auditoriacfe.projection import route_id
from auditoriacfe.reporting import PROJECTED_V2,csv_file
from auditoriacfe.spatial_experiment import GEOD, Inventory, RADII, distance, within_radius
from auditoriacfe.util import PipelineError


def point(key, meters, kind='POSTE', route='R'):
    lon,lat,_=GEOD.fwd(-117,32.5,90,meters)
    return dict(elemento_id=key,tipo=kind,latitud=str(lat),longitud=str(lon),ruta_nombre=route)


class SpatialExperimentTests(unittest.TestCase):
    def test_geodesic_inclusive_at_each_radius(self):
        for r in RADII:
            with self.subTest(r=r):
                a,b=point('a',0),point('b',r)
                from auditoriacfe.spatial_experiment import position
                d=distance(position(a),position(b))
                self.assertAlmostEqual(d,r,places=7)
                self.assertTrue(within_radius(d,r))
                self.assertFalse(within_radius(r+0.001,r))
                _,groups=Inventory([a,b]).classify(r)
                self.assertEqual([g['posiciones'] for g in groups],[2])

    def test_one_five_six_terminal_bridges_distinct_positions(self):
        rows=[point(str(i),10000+i*40,route=str(i%2)) for i in range(6)]
        rows += [point(f'five{i}',i*40) for i in range(5)]
        rows += [point('alone',20000),point('extra_identity',160),
                 point('box',10120,'CAJA_EMP'),point('spare',10120,'EXCEDENTE'),
                 point('unsupported',100,'CAJA_EMP')]
        inv=Inventory(rows)
        result,groups=inv.classify(50)
        self.assertEqual(sorted(g['posiciones'] for g in groups),[1,5,6])
        self.assertEqual(sum(g['conservado'] for g in groups),1)
        self.assertTrue(result['0']['incluido'])
        self.assertEqual(result['0']['alertas'],['PUNTO_TERMINAL','PUENTE_ESPACIAL'])
        self.assertEqual(result['2']['alertas'],['PUENTE_ESPACIAL'])
        self.assertEqual(result['five4']['motivo'],'MICROCOMPONENTE_ESPACIAL')
        self.assertFalse(result['extra_identity']['incluido'])
        self.assertTrue(result['box']['incluido'] and result['spare']['incluido'])
        self.assertEqual(result['unsupported']['motivo'],'PENDIENTE_REVISION')
        self.assertTrue(any(d==0 and {a,b}=={'box','spare'} for a,b,d,_ in inv.fusion()))
        self.assertEqual(len(result),len(rows))

    def test_monotonicity_statistics_and_invalid(self):
        rows=[point(str(i),i*80) for i in range(8)]
        rows += [dict(point('invalid',10),latitud='NaN')]
        inv=Inventory(rows)
        previous=set()
        for r in RADII:
            data,groups=inv.classify(r)
            keep={k for k,v in data.items() if v['incluido']}
            self.assertLessEqual(previous,keep)
            self.assertEqual(sum(g['posiciones'] for g in groups),8)
            self.assertEqual(data['invalid']['motivo'],'COORDENADA_INVALIDA')
            previous=keep
        self.assertEqual(len(previous),8)
        self.assertEqual(inv.statistics()[1]['n'],8)
        self.assertEqual(sum(bin['n'] for bin in inv.statistics()[5]['histograma']),8)

    def test_boundary_does_not_split_geodesic_chain(self):
        from shapely.geometry import box
        from auditoriacfe.spatial_experiment import position
        rows=[point(str(i),i*40) for i in range(6)]
        boundary=float(rows[2]['longitud'])
        area=box(-118,32,boundary,33)
        self.assertTrue(contains(area,*position(rows[0])))
        self.assertFalse(contains(area,*position(rows[-1])))
        data,_=Inventory(rows).classify(50)
        self.assertTrue(all(v['incluido'] for v in data.values()))

    def test_cad_experiment_keeps_source_csv_and_only_draws_selected_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve()/'050m'
            (root/'entrada').mkdir(parents=True)
            (root/'entrada/base.dwg').write_bytes(b'fixture')
            source=root/'02_DIAGNOSTICO_NO_VERIFICADO.csv'
            csv_file(source,PROJECTED_V2,[[k,route_id('Natura','R'),'R','POSTE','32.5','-117',i,i,'EPSG:32611']
                                        for i,k in enumerate(('A','B'))])
            original=source.read_bytes()
            cfg=dict(diagnostico=True,cad=dict(copia=True,base_dwg='base.dwg',presentacion={}))
            experiment=dict(auditoria='Natura',radio_m=50,ids={'A'})
            report=package(root,root,cfg,dict(estado='CRS_PENDIENTE'),[],experiment=experiment)
            self.assertEqual(report['elementos'],1)
            self.assertEqual(source.read_bytes(),original)
            lisp=(root/'cad_datos.lsp').read_text(encoding='utf-8')
            self.assertIn('(datra:point "A"',lisp)
            self.assertNotIn('(datra:point "B"',lisp)
            self.assertNotIn('(datra:edge ',lisp)
            self.assertEqual(len(list(root.glob('*.scr'))),2)
            with self.assertRaises(PipelineError):
                package(root,root,dict(cfg,diagnostico=False),dict(estado='CRS_PENDIENTE'),[],experiment=experiment)
