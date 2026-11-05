"""Topología física separada de identidad; solo entrada humana autoriza aristas."""
import csv
import math
from collections import defaultdict
from decimal import Decimal
from .util import PipelineError, digest, within, sha256
from .projection import route_id

CONFIRMED='arista_id,origen_id,destino_id,ruta_id,tramo_id,clase,evidencia,responsable,fecha_aprobacion,estado'.split(',')
PROPOSED='propuesta_id,origen_id,destino_id,ruta,tramo,distancia_plana_m,metodo,estado,justificacion,score,geometria_fuente'.split(',')
MAP_HEADER='id_externo,elemento_id,evidencia,responsable,fecha,aprobada'.split(',')


def read_csv(path,header):
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=header:raise PipelineError('Contrato topológico/IDs desconocido')
        rows=list(reader)
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise PipelineError('CSV topológico incompleto')
    return rows


def graph_report(nodes,edges):
    graph={n:set() for n in nodes}
    for edge in edges:
        a,b=edge['origen_id'],edge['destino_id']
        graph[a].add(b);graph[b].add(a)
    seen=set();components=[]
    for start in graph:
        if start in seen:continue
        todo=[start];comp=[]
        while todo:
            n=todo.pop()
            if n in seen:continue
            seen.add(n);comp.append(n);todo.extend(graph[n]-seen)
        components.append(sorted(comp))
    trunks={n for e in edges if e['clase']=='TRONCAL' for n in (e['origen_id'],e['destino_id'])}
    branches={n for e in edges if e['clase']=='RAMAL' for n in (e['origen_id'],e['destino_id'])}
    return dict(nodos=len(graph),aristas=len(edges),componentes=components,
                ciclos_independientes=len(edges)-len(graph)+len(components),
                extremos_candidatos=[n for n,v in graph.items() if len(v)==1],
                aislados=[n for n,v in graph.items() if not v],
                bifurcaciones=[n for n,v in graph.items() if len(v)>2],
                alerta_B06=bool(trunks and len(branches)>=len(trunks)),
                inicio_final='NO_DETERMINADO')


def confirmed_edges(audit,elements):
    path=within(audit/'entrada/topologia_confirmada.csv',audit/'entrada')
    nodes={r['elemento_id']:r for r in elements if r['tipo_canonico']=='POSTE'}
    if not path.exists():return [],dict(estado='SOLO_PUNTOS_PRELIMINAR',**graph_report(nodes,[]))
    result={};ids=set();pending=0
    routes={route_id(audit.name,r['ruta_salida']) for r in elements}
    from datetime import date
    for row in read_csv(path,CONFIRMED):
        if row['estado']!='CONFIRMADA':pending+=1;continue
        if not all(row.values()) or row['arista_id'] in ids or row['origen_id']==row['destino_id']:
            raise PipelineError('Arista confirmada incompleta/duplicada/autobucle')
        ids.add(row['arista_id'])
        try:date.fromisoformat(row['fecha_aprobacion'])
        except ValueError as exc:raise PipelineError('Fecha de aprobación inválida') from exc
        if row['origen_id'] not in nodes or row['destino_id'] not in nodes:
            raise PipelineError('Arista debe unir POSTE admitidos existentes')
        if row['ruta_id'] not in routes or row['clase'] not in ('TRONCAL','RAMAL','ENLACE'):
            raise PipelineError('Ruta/clase de arista no declarada')
        key=tuple(sorted((row['origen_id'],row['destino_id'])))
        if key in result:
            result[key]['asociaciones'].append(row)
        else:
            result[key]=dict(row,asociaciones=[row])
    edges=list(result.values())
    return edges,dict(estado='ARISTAS_CONFIRMADAS' if edges else 'SOLO_PUNTOS_PRELIMINAR',
                      sha256=sha256(path),pendientes=pending,**graph_report(nodes,edges))


def propose(audit,elements,features,tolerance=0,map_file=None):
    from pyproj import Geod
    geod=Geod(ellps='WGS84');mapping={};nodes={r['elemento_id']:r for r in elements if r['tipo_canonico']=='POSTE'}
    if not math.isfinite(float(tolerance)) or tolerance<0 or tolerance>1000:
        raise PipelineError('Tolerancia KMZ debe estar entre 0 y 1000 m, solo diagnóstico')
    if map_file:
        for row in read_csv(within(audit/'entrada'/map_file,audit/'entrada'),MAP_HEADER):
            if row['aprobada'].lower()!='true':continue
            if row['id_externo'] in mapping or row['elemento_id'] not in nodes or not all(row.values()):
                raise PipelineError('Mapa de ID externo inválido/ambiguo')
            mapping[row['id_externo']]=row['elemento_id']
    from bisect import bisect_left,bisect_right
    exact_index=defaultdict(list)
    ordered=sorted(nodes.values(),key=lambda r:float(r['latitud']))
    latitudes=[float(r['latitud']) for r in ordered]
    for r in nodes.values():exact_index[(Decimal(r['longitud']),Decimal(r['latitud']))].append(r)
    matches=[];proposals=[];seen=set();mapped_positions={};cache={}
    def match(point):
        if tuple(point) in mapped_positions:return mapped_positions[tuple(point)],1.0
        if tuple(point) in cache:return cache[tuple(point)]
        lon,lat=point
        exact=exact_index.get((Decimal(str(lon)),Decimal(str(lat))),[])
        if len(exact)==1:return exact[0]['elemento_id'],1.0
        if not tolerance:return None,0
        candidates=[]
        delta=tolerance/100000+0.001
        for r in ordered[bisect_left(latitudes,lat-delta):bisect_right(latitudes,lat+delta)]:
            # Prefiltro angular solo acelera; Geod decide la distancia.
            if abs(float(r['latitud'])-lat)>tolerance/100000+0.001:continue
            _,_,distance=geod.inv(lon,lat,float(r['longitud']),float(r['latitud']))
            if distance<=tolerance:candidates.append((r['elemento_id'],distance))
        answer=(None,0) if len(candidates)!=1 else (candidates[0][0],max(0,1-candidates[0][1]/max(tolerance,1e-12)))
        cache[tuple(point)]=answer
        return answer
    for feature in sorted(features,key=lambda f:f['tipo']!='Point'):
        if feature['tipo']=='Point':
            selected=mapping.get(feature['id_externo'])
            candidate,score=(selected,1.0) if selected else match(feature['coordenadas'][0])
            if selected:
                key=tuple(feature['coordenadas'][0])
                if key in mapped_positions and mapped_positions[key]!=selected:
                    raise PipelineError('Punto KMZ vinculado a varios postes físicos')
                mapped_positions[key]=selected
            matches.append(dict(fuente_id=feature['fuente_id'],elemento_id=candidate,score=score,estado='NO_CONFIRMADA'))
        if feature['tipo']!='LineString':continue
        vertices=[match(p) for p in feature['coordenadas']]
        for (a,sa),(b,sb) in zip(vertices,vertices[1:]):
            if not a or not b or a==b:continue
            k=(tuple(sorted((a,b))),feature['fuente_id'])
            if k in seen:continue
            seen.add(k)
            proposals.append(['T-'+digest(k),a,b,feature['nombre'],'','',
                              'KMZ_GEOMETRIA_CANDIDATA','NO_CONFIRMADA','Requiere firma en topologia_confirmada.csv',min(sa,sb),feature['fuente_id']])
    return proposals,matches
