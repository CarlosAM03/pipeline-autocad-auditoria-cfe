import csv
import json
import unittest
import zipfile
from support import AuditFixture, record, xlsx
from auditoriacfe.spatial_sources import read_spatial
from auditoriacfe.network import graph_report,confirmed_edges,propose,CONFIRMED
from auditoriacfe.projection import route_id
from auditoriacfe.util import PipelineError

KML='''<kml xmlns="http://www.opengis.net/kml/2.2"><Document>
<Placemark id="A"><name>A</name><ExtendedData><Data name="id"><value>external-A</value></Data></ExtendedData><Point><coordinates>-117,32.5,0</coordinates></Point></Placemark>
<Placemark><name>Route</name><MultiGeometry><LineString><coordinates>-117,32.5 -117,32.6 -117,32.7</coordinates></LineString><Point><coordinates>-117,32.6</coordinates></Point></MultiGeometry></Placemark>
</Document></kml>'''


class NetworkIntegralTests(unittest.TestCase):
    def setUp(self):
        self.audit=AuditFixture();self.addCleanup(self.audit.close)

    def elements(self):
        return [dict(elemento_id=str(i),tipo_canonico='POSTE',ruta_salida='R',latitud=str(32.5+i/10),longitud='-117') for i in range(4)]

    def test_kml_kmz_multigeometry_data(self):
        p=self.audit.path/'entrada/test.kmz'
        with zipfile.ZipFile(p,'w') as z:z.writestr('doc.kml',KML)
        features,info=read_spatial(p)
        self.assertEqual(info['puntos'],2);self.assertEqual(info['lineas'],1)
        self.assertEqual(features[0]['datos']['id'],'external-A')
        proposals,matches=propose(self.audit.path,self.elements(),features)
        self.assertEqual(len(proposals),2)
        self.assertTrue(all(row[7]=='NO_CONFIRMADA' for row in proposals))

    def test_zip_traversal_bomb_no_kml_xml_entity(self):
        p=self.audit.path/'entrada/bad.kmz'
        for name,data in [('../outside.kml',KML),('large.kml','x'*(17*1024*1024)),('nothing.txt','x'),('doc.kml','<!DOCTYPE a [<!ENTITY x "boom">]><kml/>')]:
            with self.subTest(name=name):
                with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:z.writestr(name,data)
                with self.assertRaises((PipelineError,ValueError)):read_spatial(p)
        self.assertFalse((self.audit.path/'outside.kml').exists())
        from auditoriacfe.geofence import safe_xml
        with self.assertRaises(PipelineError):safe_xml('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE a [<!ENTITY x "boom">]><kml/>'.encode('utf-16'))

    def write_edges(self,pairs,**changes):
        with (self.audit.path/'entrada/topologia_confirmada.csv').open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,CONFIRMED);writer.writeheader()
            for i,(a,b) in enumerate(pairs):
                row=dict(arista_id=f'e{i}',origen_id=a,destino_id=b,ruta_id=route_id(self.audit.path.name,'R'),
                         tramo_id='T',clase='TRONCAL',evidencia='TEST',responsable='owner TEST',fecha_aprobacion='2026-11-05',estado='CONFIRMADA')
                row.update(changes);writer.writerow(row)

    def test_branch_cycle_shared_routes_no_false_return(self):
        elements=self.elements()
        self.write_edges([('0','1'),('1','2'),('1','3'),('3','0')])
        edges,report=confirmed_edges(self.audit.path,elements)
        self.assertEqual(len(edges),4)
        self.assertEqual(report['ciclos_independientes'],1)
        self.assertNotIn(('2','3'),[(e['origen_id'],e['destino_id']) for e in edges])

    def test_disconnect_crossings_and_duplicate_physical_edge(self):
        self.write_edges([('0','1'),('1','0')])
        edges,report=confirmed_edges(self.audit.path,self.elements())
        self.assertEqual(len(edges),1)
        self.assertEqual(len(edges[0]['asociaciones']),2)
        self.assertEqual(len(report['componentes']),3)
        self.assertEqual(report['inicio_final'],'NO_DETERMINADO')

    def test_unknown_ids_boxes_and_pending_not_authority(self):
        self.write_edges([('0','NOT_REAL')])
        with self.assertRaises(PipelineError):confirmed_edges(self.audit.path,self.elements())
        self.write_edges([('0','1')],estado='PROPUESTA')
        edges,report=confirmed_edges(self.audit.path,self.elements())
        self.assertEqual(edges,[])
        self.write_edges([('0','1')])
        elements=self.elements();elements[1]['tipo_canonico']='CAJA_EMP'
        with self.assertRaises(PipelineError):confirmed_edges(self.audit.path,elements)

    def test_no_confirmation_no_lines_even_with_proposals(self):
        edges,report=confirmed_edges(self.audit.path,self.elements())
        self.assertEqual(edges,[])
        self.assertEqual(report['estado'],'SOLO_PUNTOS_PRELIMINAR')
