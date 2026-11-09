"""Compilación CAD de las vistas ADR-002, opt-in."""
import csv
from pathlib import Path

from .presentation import Profile, SYMBOL_WIDTH, plan
from .util import json_text


RUNTIME = Path(__file__).with_name('cad_presentation.lsp')


def compile_pages(stage, rows, spec, layout, owner, audit_name, index, literal, number):
    from .cad import geo_label
    profile = Profile.parse(spec)
    points = [dict(id=r['elemento_id'], x=float(r['este_m']), y=float(r['norte_m']),
                   geo=geo_label(r), label=index[r['elemento_id']], tipo=r['tipo']) for r in rows]
    pages = plan(points, profile, layout)
    def call(fn, *args):
        return '(' + fn + ' ' + ' '.join(literal(x) if isinstance(x,str) else number(x) for x in args) + ')'
    names = "'(" + ' '.join(literal(p['layout']) for p in pages) + ')'
    commands = [f'(datra:prepare-pages {names})']
    records = []
    for page in pages:
        name, labels = page['layout'], page['etiquetas']
        commands.append(call('datra:page', name, *page['centro'], page['escala']))
        commands.append(call('datra:sheet-title', audit_name, page['numero'], len(pages),
                             page['vista'], len(labels), page['escala']))
        for marker in page.get('sectores', []):
            commands.append(call('datra:annotation', marker['id'], marker['geo'], '',
                                 *marker['ancla'], *marker['fin_lider'], *marker['caja'][:2], 2.3, 0))
        for row in labels:
            commands.append(call('datra:annotation', row['id'], row['geo'], row['label'], *row['ancla'],
                                 *row['fin_lider'], *row['caja'][:2], profile.coordenada_mm, profile.identificador_mm))
            records.append([row['id'],row['tipo'],row['geo'],row['label'],page['numero'],name])
    commands.append(f'(setq datra:*layout* {literal(layout)})')
    with (stage/'indice_presentacion.csv').open('w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['elemento_id','tipo','coordenada_geografica','identificador','pagina','layout'])
        writer.writerows(sorted(records))
    metrics = [dict(p, etiquetas=len(p['etiquetas'])) for p in pages]
    data = dict(hojas=metrics, perfil=vars(profile), identificados=len(points),
                etiquetas_asignadas=len(records), evaluacion='PENDIENTE_REVISION_NATIVA_Y_HUMANA')
    (stage/'presentacion_paginas.json').write_text(json_text(data),encoding='utf-8')
    sizes = {kind:profile.escala_detalle*value/SYMBOL_WIDTH[kind] for kind,value in profile.sizes.items()}
    check = f'(datra:pages-check {names} {literal(owner)})'
    return check, commands, sizes, data
