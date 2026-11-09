"""Política A4.2 de visibilidad CAD diagnóstica en los tres perfiles autorizados."""
import json
from collections import Counter

from .dedup import identified_groups
from .reporting import csv_file
from .spatial_experiment import Inventory
from .util import PipelineError

AUDITS = frozenset(('Natura','Mirador','Otay-Florido'))
DEFAULT_RADIUS = 300
VERSION = 'A4.2-visibilidad-WGS84-v1'
DECISIONS = 'DECISIONES_VISUALIZACION.csv'
EXCLUSIONS = 'COORDENADAS_DESCARTADAS_VISUALIZACION.csv'
FIELDS = ('auditoria variante_radio_m elemento_id tipo ruta_id subruta archivo_fuente hoja_fuente fila_fuente '
          'coordenada_original latitud_normalizada longitud_normalizada componente_espacial_id cantidad_postes_componente '
          'vecinos_dentro_radio distancia_vecino_m distancia_al_componente_conservado_m estado_territorial motivo_exclusion '
          'etapa_exclusion estado_revision evidencia_o_referencia hash_fuente incluido alerta_espacial soporte '
          'elemento_conservado_mas_cercano').split()


def effective_radius(audit_name, diagnostic, cad):
    if 'radio_visibilidad_m' in cad:
        value = cad['radio_visibilidad_m']
        if value is not None and (type(value) is not int or value <= 0):
            raise PipelineError('cad.radio_visibilidad_m requiere entero positivo o null')
    if not diagnostic or audit_name not in AUDITS or cad.get('presentacion') is None:
        return None
    return cad.get('radio_visibilidad_m', DEFAULT_RADIUS)


def select(stage, rows, radius, audit):
    """Mantiene las filas CSV originales; decide únicamente su aparición en CAD."""
    decisions, groups = Inventory(rows).classify(radius, experimental=False)
    with (stage/'linaje_y_calidad.jsonl').open(encoding='utf-8') as f:
        lineage = list(map(json.loads,f))
    prevalent = {r['elemento_id']:r for r in identified_groups(lineage)}
    mapped = {r['elemento_id']:r for r in rows}
    if mapped.keys()!=prevalent.keys():
        raise PipelineError('El inventario diagnóstico no coincide con el linaje canónico')
    report = []
    visible = []
    excluded = []
    by_type = Counter()
    for key,row in mapped.items():
        origin = prevalent[key]
        d = decisions[key]
        if d['incluido']:
            visible.append(row)
        flag = 'SI' if d['incluido'] else 'NO'
        line = [audit,radius,key,row['tipo'],row['ruta_id'],row['ruta_nombre'],origin['archivo_relativo'],
            origin['hoja'],origin['fila'],origin['coordenada_original'],row['latitud'],row['longitud'],
            d.get('componente'),d.get('postes'),d.get('vecinos'),d.get('distancia_vecino'),d.get('distancia_conservado'),
            'PENDIENTE_VALIDACION_TERRITORIAL','' if d['incluido'] else d['motivo'],
            'VISIBILIDAD_CARTOGRAFICA','PENDIENTE_REVISION' if not d['incluido'] else '',
            'linaje_y_calidad.jsonl; '+VERSION,origin['archivo_sha256'],flag,'|'.join(d.get('alertas',[])),
            d.get('soporte'),d.get('vecino_conservado_id')]
        report.append(line)
        if not d['incluido']:
            excluded.append(line)
        by_type[row['tipo'],flag] += 1
    csv_file(stage/DECISIONS,FIELDS,report)
    csv_file(stage/EXCLUSIONS,FIELDS,excluded)
    metadata = dict(version=VERSION,radio_m=radius,minimo_posiciones_poste=6,
        inventario=len(rows),representados=len(visible),no_representados=len(rows)-len(visible),
        componentes=len(groups),microcomponentes=sum(not g['conservado'] for g in groups),
        decisiones_por_id={k:dict(incluido=d['incluido'],motivo=d['motivo']) for k,d in decisions.items()})
    stats = [(k,v) for k,v in metadata.items() if k!='decisiones_por_id']
    stats.extend((f'{kind}::{flag}',count) for (kind,flag),count in sorted(by_type.items()))
    csv_file(stage/'SUMMARY_COORDENADAS_DESCARTADAS.csv',['metrica','valor'],stats)
    (stage/'SUMMARY_COORDENADAS_DESCARTADAS.md').write_text(
        '# Visibilidad cartográfica diagnóstica\n\n' + '\n'.join(f'- {k} · {v}' for k,v in stats) +
        '\n\nLas identidades se conservan en el inventario y el linaje. Las decisiones individuales figuran en el CSV.\n',
        encoding='utf-8')
    return visible,metadata
