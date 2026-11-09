"""Resumen CFE adaptado a datos comprobables de una revisión diagnóstica."""
import csv
from collections import Counter
from pathlib import Path

from .util import PipelineError


RUNTIME = Path(__file__).with_name('cad_review.lsp')
KINDS = ('POSTE', 'CAJA_EMP', 'EXCEDENTE')


def compile_review(stage, spec, rows, visibility, literal):
    fields = ('fecha', 'elaboro', 'reviso')
    if not isinstance(spec, dict) or set(spec) != set(fields):
        raise PipelineError('cad.revision_documental solo admite fecha, elaboro y reviso')
    for key in fields:
        value = spec[key]
        if not isinstance(value, str) or not value.strip() or len(value) > 40:
            raise PipelineError(f'Campo de revisión inválido: {key}')
        literal(value)
    if visibility is None or visibility['radio_m'] != 300:
        raise PipelineError('La revisión documental requiere visibilidad diagnóstica de 300 m')
    decisions = visibility['decisiones_por_id']
    source = stage/'02_DIAGNOSTICO_NO_VERIFICADO.csv'
    with source.open(encoding='utf-8', newline='') as stream:
        inventory = list(csv.DictReader(stream))
    original = Counter(r['tipo'] for r in inventory)
    drawn = Counter(r['tipo'] for r in rows)
    ids = {r['elemento_id'] for r in inventory}
    included = {key for key, value in decisions.items() if value['incluido']}
    if (ids != decisions.keys() or len(ids) != len(inventory)
            or included != {r['elemento_id'] for r in rows} or len(included) != len(rows)):
        raise PipelineError('Inventario de la tabla CFE no reconciliado')
    with (stage/'anexo_coordenadas_revision.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['elemento_id', 'tipo', 'LONGITUD [°]', 'LATITUD [°]', 'representado'])
        for row in inventory:
            key = row['elemento_id']
            writer.writerow([key, row['tipo'], row['longitud'], row['latitud'], 'SI' if key in included else 'NO'])
    counts = [(kind, original[kind], drawn[kind], original[kind]-drawn[kind]) for kind in KINDS]
    counts.append(('TOTAL', len(inventory), len(rows), len(inventory)-len(rows)))
    matrix = "'("+' '.join(f'({literal(k)} {a} {b} {c})' for k,a,b,c in counts)+')'
    return '(datra:review '+ ' '.join(literal(spec[key]) for key in fields)+' '+matrix+')'
