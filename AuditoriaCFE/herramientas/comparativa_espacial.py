"""Genera las doce variantes A4.1.1 desde lotes A4_1_r5 verificados."""
import argparse
import csv
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT/'src'))
from auditoriacfe.cad import package
from auditoriacfe.dedup import identified_groups
from auditoriacfe.geofence import contains
from auditoriacfe.native_evidence import verify_native
from auditoriacfe.projection import read_projected, route_id
from auditoriacfe.reporting import PROJECTED_V2, csv_file, verify
from auditoriacfe.spatial_experiment import Inventory, RADII
from auditoriacfe.traceability import generate_workbooks
from auditoriacfe.util import digest, json_text, sha256

NAMES = {'Natura':16, 'Mirador':18, 'Otay-Florido':16}
ROOT = PROJECT/'auditorias/_comparativa_A4_1_1'
SOURCE = 'https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/02004'
ORIGINALS = ('00_elementos_unificados.csv','00_elementos_revision.csv','01_elementos_normalizados.csv',
    '02_DIAGNOSTICO_NO_VERIFICADO.csv','summary.csv','reporte_incidencias.csv','linaje_y_calidad.jsonl',
    'asociaciones_elemento_ruta.csv','topologia_propuesta.csv','reporte_topologia.json','resumen_conteos.csv')
INCLUDED = 'COORDENADAS_ADMITIDAS_VISUALIZACION.csv'
EXCLUDED = 'COORDENADAS_DESCARTADAS_VISUALIZACION.csv'
DECISIONS = 'DECISIONES_VISUALIZACION.csv'
FIELDS = ('auditoria variante_radio_m elemento_id tipo ruta_id subruta archivo_fuente hoja_fuente fila_fuente '
    'coordenada_original latitud_normalizada longitud_normalizada componente_espacial_id cantidad_postes_componente '
    'vecinos_dentro_radio distancia_vecino_m distancia_al_componente_conservado_m estado_territorial motivo_exclusion '
    'etapa_exclusion estado_revision evidencia_o_referencia hash_fuente incluido alerta_espacial soporte '
    'elemento_conservado_mas_cercano').split()


def save(path, data):
    path.write_text(json_text(data),encoding='utf-8')


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def dicts(path, fields, rows):
    csv_file(path, fields, ([row.get(k) for k in fields] for row in rows))


def base(name):
    return PROJECT/'auditorias'/name/'salida/resultados_cad/A4_1_r5'/name


def territory(path):
    if path is None:
        return None, dict(estado='PENDIENTE_VALIDACION_TERRITORIAL')
    from shapely.geometry import shape
    doc = json.loads(path.read_text(encoding='utf-8'))
    features = doc['features']
    if len(features)!=1 or features[0]['properties']['cvegeo']!='02004':
        raise ValueError('GeoJSON no corresponde a AGEM Tijuana 02004')
    geom = shape(features[0]['geometry'])
    if geom.geom_type not in ('Polygon','MultiPolygon') or geom.is_empty or not geom.is_valid:
        raise ValueError('Polígono territorial inválido')
    if not (-180<=geom.bounds[0]<geom.bounds[2]<=180 and -90<=geom.bounds[1]<geom.bounds[3]<=90):
        raise ValueError('GeoJSON fuera de coordenadas geográficas')
    return geom, dict(estado='REFERENCIA_GEOESTADISTICA_EXPLORATORIA', fuente=SOURCE, clave='02004',
                      crs='WGS84 lon/lat GeoJSON', sha256=sha256(path), cobertura_DATRA='PENDIENTE_VALIDACION_TERRITORIAL')


def decision(name, radius, row, occurrence, result, territorial, evidence):
    return dict(auditoria=name,variante_radio_m=radius,elemento_id=row['elemento_id'],tipo=row['tipo'],
        ruta_id=route_id(name,occurrence['ruta_salida']),subruta=occurrence['ruta_salida'],
        archivo_fuente=occurrence['archivo_relativo'],hoja_fuente=occurrence['hoja'],fila_fuente=occurrence['fila'],
        coordenada_original=occurrence['coordenada_original'],latitud_normalizada=row.get('latitud'),
        longitud_normalizada=row.get('longitud'),componente_espacial_id=result.get('componente'),
        cantidad_postes_componente=result.get('postes'),vecinos_dentro_radio=result.get('vecinos'),
        distancia_vecino_m=result.get('distancia_vecino'),distancia_al_componente_conservado_m=result.get('distancia_conservado'),
        estado_territorial=territorial,motivo_exclusion='' if result['incluido'] else result['motivo'],
        etapa_exclusion='FILTRADO_CARTOGRAFICO_EXPERIMENTAL',estado_revision='PENDIENTE_REVISION',
        evidencia_o_referencia=evidence,hash_fuente=occurrence['archivo_sha256'],incluido='SI' if result['incluido'] else 'NO',
        alerta_espacial='|'.join(result.get('alertas',[])),soporte=result.get('soporte'),
        elemento_conservado_mas_cercano=result.get('vecino_conservado_id'))


def build(name, area, territory_info, root):
    baseline=base(name)
    source=baseline/'salida'
    manifest=verify(baseline)
    verify_native(baseline)
    assert not (source/'02_elementos_proyectados.csv').exists()
    assert manifest['cad']['aristas']==0 and manifest['cad']['controles_crs']=='CRS_PENDIENTE'
    orig_config=json.loads((baseline/'configuracion.json').read_text(encoding='utf-8'))
    projected,_=read_projected(source/'02_DIAGNOSTICO_NO_VERIFICADO.csv',name)
    canonical=read(source/'00_elementos_unificados.csv')
    records=[json.loads(line) for line in (source/'linaje_y_calidad.jsonl').read_text(encoding='utf-8').splitlines()]
    prevalent={r['elemento_id']:r for r in identified_groups(records)}
    orig_rows={r['elemento_id']:r for r in canonical}
    known={r['elemento_id']:r for r in projected}
    assert orig_rows.keys()==prevalent.keys() and known.keys()<=orig_rows.keys()
    for k,r in known.items():
        assert (r['tipo'],r['latitud'],r['longitud'])==(prevalent[k]['tipo_canonico'],prevalent[k]['latitud'],prevalent[k]['longitud'])
    occurrences=defaultdict(list)
    for r in records:
        if r['elemento_id']:
            occurrences[r['elemento_id']].append(r)
    stats_inventory=Inventory(projected)
    stats=stats_inventory.statistics()
    owner=root/name
    owner.mkdir()
    save(owner/'ESTADISTICAS_VECINOS.json',stats)
    print(name,'vecino 1',stats[1]['n'],stats[1]['media'],stats[1]['moda'],flush=True)
    spatial={k:('PENDIENTE_VALIDACION_TERRITORIAL' if area is None or p is None else
               'DENTRO_AMBITO_CANDIDATO' if contains(area,*p) else 'FUERA_AMBITO_CANDIDATO')
             for k,p in stats_inventory.locations.items()}
    fusion=[(a,b,d,band,known[a]['tipo'],known[b]['tipo'],
             'TIPOS_DISTINTOS' if known[a]['tipo']!=known[b]['tipo'] else 'IDENTIDAD_PENDIENTE',
             prevalent[a]['archivo_relativo'],prevalent[b]['archivo_relativo'],
             prevalent[a]['hoja'],prevalent[a]['fila'],prevalent[b]['hoja'],prevalent[b]['fila'],'GEOD_WGS84; NO FUSIONAR')
            for a,b,d,band in stats_inventory.fusion()]
    by_radius={}
    previous=set()
    for radius in RADII:
        variant=owner/f'{radius:03d}m'
        variant.mkdir()
        for name_file in ORIGINALS:
            shutil.copyfile(source/name_file,variant/name_file)
        target=variant/'entrada'
        target.mkdir()
        base_file=baseline/'entrada'/manifest['cad']['archivo_base']
        assert sha256(base_file)==manifest['cad']['base_sha256']
        shutil.copyfile(base_file,target/base_file.name)
        results,groups=stats_inventory.classify(radius)
        accepted={k for k,r in results.items() if r['incluido']}
        posts={k for k in accepted if known[k]['tipo']=='POSTE'}
        assert previous<=posts
        previous=posts
        for k in orig_rows.keys()-results.keys():
            results[k]=dict(incluido=False,motivo='PENDIENTE_REVISION')
        by_radius[radius]=results
        rows=[]
        for k,orig in orig_rows.items():
            row=known.get(k,dict(elemento_id=k,tipo=orig['tipo'],latitud=prevalent[k]['latitud'],longitud=prevalent[k]['longitud']))
            rows.append(decision(name,radius,row,prevalent[k],results[k],spatial.get(k,'PENDIENTE_VALIDACION_TERRITORIAL'),
                                 'linaje_y_calidad.jsonl; WGS84; ejecución '+manifest['ejecucion_id']))
        excluded=[r for r in rows if r['incluido']=='NO']
        assert len(excluded)+len(accepted)==len(canonical)
        dicts(variant/DECISIONS,FIELDS,rows)
        dicts(variant/EXCLUDED,FIELDS,excluded)
        dicts(variant/INCLUDED,PROJECTED_V2,(r for r in projected if r['elemento_id'] in accepted))
        csv_file(variant/'CANDIDATOS_FUSION_PROXIMIDAD.csv',
                 'id_a id_b distancia_m banda tipo_a tipo_b alerta fuente_a fuente_b hoja_a fila_a hoja_b fila_b evidencia'.split(),fusion)
        csv_file(variant/'OCURRENCIAS_AFECTADAS.csv',
                 'elemento_id ocurrencia_id fuente hoja fila ruta_original ruta_id coordenada_original estado_origen hash_fuente'.split(),
                 ([r['elemento_id'],r['ocurrencia_id'],r['archivo_relativo'],r['hoja'],r['fila'],r['ruta_original'],
                    route_id(name,r['ruta_salida']),r['coordenada_original'],r['estado'],r['archivo_sha256']]
                  for e in excluded for r in occurrences[e['elemento_id']]))
        save(variant/'DISTANCIAS_VECINOS.json',stats)
        dicts(variant/'VECINOS_POSTE.csv',['posicion_id','distancia_1_m','distancia_2_m','distancia_3_m','distancia_5_m'],
              (dict(posicion_id=digest(list(map(str,p))),**{f'distancia_{n}_m':ds[n-1] for n in (1,2,3,5) if len(ds)>=n})
               for p,ds in zip(stats_inventory.posts,stats_inventory.neighbors)))
        for group in groups:
            candidates=[(results[k]['distancia_conservado'],k) for k in group['ids_poste']
                        if results[k].get('distancia_conservado') is not None]
            if not group['conservado'] and candidates:
                distance,k=min(candidates)
                group.update(distancia_conservado=distance, poste_microcomponente_id=k,
                             poste_conservado_id=results[k]['vecino_conservado_id'])
        save(variant/'COMPONENTES_ESPACIALES.json',groups)
        cfg=dict(orig_config,cad=dict(orig_config['cad'],copia_nombre=f'{name}_A4_1_1_{radius:03d}m.dwg'))
        save(variant/'CONFIGURACION_VARIANTE.json',dict(configuracion=cfg,radio_m=radius,
             linea_base=baseline.relative_to(PROJECT.parent).as_posix(),territorio=territory_info))
        cad=package(variant,variant,cfg,manifest['crs'],[],
                    experiment=dict(auditoria=name,radio_m=radius,ids=accepted))
        work=variant/'resultados_cad'
        work.mkdir()
        shutil.copyfile(target/base_file.name,variant/cad['copia_relativa'])
        generate_workbooks(variant,manifest,[],visual_sheet=[FIELDS]+[[r.get(k) for k in FIELDS] for r in rows])
        size_counts=Counter(min(g['posiciones'],6) for g in groups)
        all_by_type=Counter(r['tipo'] for r in rows)
        excluded_by_type=Counter(r['tipo'] for r in excluded)
        by_file=Counter(r['archivo_fuente'] for r in excluded)
        by_route=Counter(r['subruta'] for r in excluded)
        affected=Counter(r['archivo_relativo'] for e in excluded for r in occurrences[e['elemento_id']])
        reconcile=[('TIPO',k,v,v-excluded_by_type[k],excluded_by_type[k]) for k,v in sorted(all_by_type.items())]
        for field,dim in [('archivo_fuente','FUENTE_PREVALENTE'),('subruta','SUBRUTA_PREVALENTE')]:
            original=Counter(r[field] for r in rows)
            removed=Counter(r[field] for r in excluded)
            reconcile.extend((dim,k,v,v-removed[k],removed[k]) for k,v in sorted(original.items()))
        original=Counter(r['archivo_relativo'] for r in records if r['elemento_id'])
        reconcile.extend(('FUENTE_OCURRENCIAS_CON_ID',k,v,v-affected[k],affected[k]) for k,v in sorted(original.items()))
        csv_file(variant/'RECONCILIACION_CONTEOS.csv',['dimension','clave','total','conservado','excluido'],reconcile)
        sheets=json.loads((variant/'presentacion_paginas.json').read_text(encoding='utf-8'))['hojas']
        summary=dict(auditoria=name,radio_m=radius,total_original=len(rows),conservado=len(accepted),excluido=len(excluded),
            porcentaje_excluido=100*len(excluded)/len(rows),posiciones_poste=len(stats_inventory.posts),
            componentes=len(groups),**{f'componentes_{i}':size_counts[i] for i in range(1,6)},
            componentes_conservados=size_counts[6],microcomponentes=sum(size_counts[i] for i in range(1,6)),
            postes_conservados=cad['conteos'].get('POSTE',0),cajas_conservadas=cad['conteos'].get('CAJA_EMP',0),
            excedentes_conservados=cad['conteos'].get('EXCEDENTE',0),
            **{f'{k.lower()}_excluidos':excluded_by_type[k] for k in ('POSTE','CAJA_EMP','EXCEDENTE')},
            fuera_ambito_candidato=sum(v=='FUERA_AMBITO_CANDIDATO' for v in spatial.values()),
            pendientes_territoriales=len(rows),candidatos_fusion=len(fusion),paginas=len(sheets),
            diferencia_paginas=len(sheets)-NAMES[name],colisiones_etiquetas=None,
            paginas_sin_utilidad=None,paginas_detalle_1_a_5=sum(0<s['etiquetas']<=5 for s in sheets),
            cad='PENDIENTE_EVIDENCIA',ocurrencias_origen_no_evaluadas=sum(not r['elemento_id'] for r in records),
            terminales=sum('PUNTO_TERMINAL' in r['alerta_espacial'] for r in rows),
            puentes=sum('PUENTE_ESPACIAL' in r['alerta_espacial'] for r in rows),
            advertencias='Microcomponentes pueden ser legítimos; encadenamiento puede conservar errores; P03/P05/P06 pendientes',
            **{f'vecino_{k}':stats[1][k] for k in ('minimo','moda','media','media_modal','mediana','p10','p25','p75','p90','p95')})
        save(variant/'RESUMEN_VARIANTE.json',summary)
        csv_file(variant/'SUMMARY_COORDENADAS_DESCARTADAS.csv',['metrica','valor'],
                 [*summary.items(),*((f'fuente_prevalente::{k}',v) for k,v in sorted(by_file.items())),
                  *((f'subruta_prevalente::{k}',v) for k,v in sorted(by_route.items())),
                  *((f'fuente_ocurrencias::{k}',v) for k,v in sorted(affected.items()))])
        data=dict(schema='A4.1.1-v1',auditoria=name,radio_m=radius,ejecucion_id=digest(
                  [manifest['ejecucion_id'],radius,sha256(variant/DECISIONS),sha256(variant/'cad_datos.lsp')]),
                  base_id=manifest['ejecucion_id'], base_path=baseline.relative_to(PROJECT.parent).as_posix(),
                  base_manifest_sha256=sha256(source/'manifiesto_ejecucion.json'),fuentes=manifest['fuentes_ordenadas'],
                  originales={f:sha256(source/f) for f in ORIGINALS},cad=cad,territorio=territory_info,
                  id_bomberos=sum(r['archivo_relativo']=='CFE FLO-OTAY-BOMBEROS.xlsx' for r in records))
        save(variant/'MANIFIESTO_VARIANTE.json',data)
        print(name,radius,len(accepted),len(excluded),len(sheets),flush=True)
    matrix_fields=['auditoria','elemento_id','tipo',*[f'{r:03d}m' for r in RADII]]
    csv_file(owner/'MATRIZ_INCLUSION_EXCLUSION.csv',matrix_fields,
             ([name,k,orig_rows[k]['tipo'],*[('INCLUIDO' if by_radius[r][k]['incluido'] else by_radius[r][k]['motivo']) for r in RADII]]
              for k in orig_rows))
    dicts(owner/'TERRITORIO_CANDIDATO.csv',FIELDS,
          (decision(name,0,known[k],prevalent[k],by_radius[50][k],v,SOURCE)
           for k,v in spatial.items() if v=='FUERA_AMBITO_CANDIDATO'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--territorio',type=Path)
    args=parser.parse_args()
    area,info=territory(args.territorio)
    ROOT.mkdir()
    if args.territorio:
        shutil.copyfile(args.territorio,ROOT/'TIJUANA_INEGI_02004.geojson')
    save(ROOT/'PROCEDENCIA_TERRITORIAL.json',info)
    for name in NAMES:
        build(name,area,info,ROOT)


if __name__=='__main__':
    main()
