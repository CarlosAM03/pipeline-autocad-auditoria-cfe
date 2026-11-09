"""Compilación determinista; no ejecuta AutoCAD ni acredita evidencia física."""
import math
import re
import shutil
from collections import Counter
from decimal import Decimal
from pathlib import Path

from .projection import read_projected
from . import cad_presentation
from .presentation import Profile
from .util import PipelineError, digest, json_text, sha256, within

RUNTIME = Path(__file__).with_name('cad_runtime.lsp')
TYPES = {'POSTE': ('P', 'DATRA_POSTE_V1'), 'CAJA_EMP': ('C', 'DATRA_CAJA_EMP_V1'),
         'EXCEDENTE': ('E', 'DATRA_EXCEDENTE_V1')}


def literal(value):
    """Una cadena AutoLISP, nunca código procedente de una celda."""
    value = str(value)
    if any(ord(c) < 32 for c in value):
        raise PipelineError('Control no permitido en literal CAD')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def number(value):
    result = float(value)
    if not math.isfinite(result):
        raise PipelineError('Número CAD no finito')
    return repr(result)


def geo_label(row):
    lat,lon=Decimal(row['latitud']),Decimal(row['longitud'])
    return f'{abs(lat)}{"N" if lat>=0 else "S"} {abs(lon)}{"E" if lon>=0 else "W"}'


def static_check(text):
    """Chequeo léxico, explícitamente distinto de una ejecución AutoLISP nativa."""
    depth = 0
    string = escape = comment = False
    for c in text:
        if comment:
            if c == '\n': comment = False
            continue
        if string:
            if escape: escape = False
            elif c == '\\': escape = True
            elif c == '"': string = False
        elif c == ';': comment = True
        elif c == '"': string = True
        elif c == '(': depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0: raise PipelineError('Paréntesis CAD sin apertura')
    if string or depth: raise PipelineError('Código CAD incompleto')
    return True


def package(stage, audit, cfg, crs_info, edges):
    spec = cfg.get('cad')
    if not spec:
        return dict(estado='PENDIENTE_EVIDENCIA', motivo='No se declaró base DATRA en copia')
    if not isinstance(spec, dict) or spec.get('copia') is not True:
        raise PipelineError('CAD requiere copia=true')
    base = within(audit/'entrada'/spec.get('base_dwg', ''), audit/'entrada')
    if not base.is_file() or base.suffix.lower() != '.dwg':
        raise PipelineError('Base DWG en copia ausente')
    layout = spec.get('layout', 'DATRA_A1')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,30}', layout):
        raise PipelineError('Nombre de layout CAD inseguro')
    if type(spec.get('unidades_verificadas', False)) is not bool:
        raise PipelineError('unidades_verificadas requiere booleano')
    diagnostic = cfg['diagnostico']
    presentation = spec.get('presentacion')
    if presentation is not None:
        Profile.parse(presentation)
    productive = crs_info['estado'] == 'CONTROLES_VERIFICADOS' and not diagnostic
    if productive and spec.get('unidades_verificadas') is not True:
        productive = False
    mode = 'DIAGNOSTICO_NO_VERIFICADO' if diagnostic else 'PRELIMINAR'
    if productive: mode = 'PRELIMINAR_CRS_ACREDITADO'
    # Ensayos ficticios no deben presentarse como acreditación de una base real.
    if spec.get('rotulo_fixture'):
        if not audit.name.startswith('Fixture-') or spec['rotulo_fixture']!='SOLO_FIXTURE_SINTETICO':
            raise PipelineError('Rótulo fixture reservado a auditorías Fixture- ficticias')
        mode='SOLO_FIXTURE_SINTETICO'
    source = stage/('02_DIAGNOSTICO_NO_VERIFICADO.csv' if diagnostic else '02_elementos_proyectados.csv')
    rows = []
    if source.exists() and (productive or diagnostic): rows, _ = read_projected(source, audit.name)
    owner = 'AUD-' + digest(audit.name)
    copy_name = 'plano_' + sha256(base)[:16] + '.dwg'
    if spec.get('copia_nombre'):
        copy_name=spec['copia_nombre']
        if not isinstance(copy_name,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}\.dwg',copy_name):
            raise PipelineError('copia_nombre debe ser nombre DWG simple seguro')
    target = audit/'salida/resultados_cad'/copy_name
    destination = audit/'salida'
    header = f'(load {literal((destination/"cad_runtime.lsp").as_posix())})\n'
    common = [literal(target.as_posix()), literal(owner), literal(layout), literal(mode)]
    setup = header + "(datra:run '(lambda () (datra:configure " + ' '.join(common)
    # La unidad de inserción no acredita que los objetos del mapa estén en metros.
    setup += (' T' if spec.get('unidades_verificadas') else ' nil') + ')))\n'
    # Mantener exactamente dos SCR; si el gate impide dibujar, el segundo es seguro.
    commands = ['(datra:begin ' + ' '.join(common) + ')']
    if type(spec.get('prototipos',True)) is not bool:raise PipelineError('prototipos requiere booleano')
    commands.append('(setq datra:*prototypes* '+('T' if spec.get('prototipos',True) else 'nil')+')')
    counts = Counter(); labels = set()
    index = {}
    label_index = {}
    for row in sorted(rows, key=lambda r: r['elemento_id']):
        kind = row['tipo']; counts[kind] += 1
        # Número estable derivado del ID completo; colisión => bloquear, nunca ocultar.
        label = TYPES[kind][0] + '-' + str(int(digest(row['elemento_id'])[:10],16))
        if label in labels: raise PipelineError('Colisión de etiqueta CAD; ampliar numeración')
        labels.add(label)
        x, y = number(row['este_m']), number(row['norte_m'])
        commands.append('(datra:point ' + ' '.join([literal(row['elemento_id']), literal(TYPES[kind][1]),
                        literal(kind), x, y, literal(label), literal(geo_label(row))]) + ')')
        index[row['elemento_id']] = row
        label_index[row['elemento_id']] = label
    physical = set(); drawn_edges = []
    # Diagnóstico candidato siempre SOLO PUNTOS, incluso si hay una propuesta de red.
    if productive:
        for edge in edges:
            a, b = edge['origen_id'], edge['destino_id']
            if a not in index or b not in index or any(index[n]['tipo'] != 'POSTE' for n in (a,b)):
                raise PipelineError('Arista CAD sin dos POSTE proyectados')
            pair = tuple(sorted((a,b)))
            if pair in physical: continue
            if edge.get('estado') != 'CONFIRMADA' or not all(edge.get(k) for k in ('evidencia','responsable','fecha_aprobacion')):
                raise PipelineError('Arista CAD no confirmada')
            physical.add(pair)
            p, q = index[a], index[b]
            distance = math.hypot(float(p['este_m'])-float(q['este_m']),float(p['norte_m'])-float(q['norte_m']))
            coords = [number(r[k]) for r in (p,q) for k in ('este_m','norte_m')]
            commands.append('(datra:edge ' + ' '.join([literal(edge['arista_id']),*coords,literal(f'{distance:.2f} m')]) + ')')
            drawn_edges.append(dict(arista_id=edge['arista_id'],distancia_plana_m=distance))
    bounds = None
    scale = 1.0
    if rows:
        xs = [float(r['este_m']) for r in rows]; ys = [float(r['norte_m']) for r in rows]
        bounds = [min(xs),min(ys),max(xs),max(ys)]
        # Reservar papel para etiquetas al este de cada símbolo; no recortarlas
        # en el borde cuando un punto esté en el extremo del inventario.
        scale = max((bounds[2]-bounds[0])/410,(bounds[3]-bounds[1])/445,0.01)
        # Propuesta visual: texto 3 mm y coordenada 2.5 mm en papel.
        # Se declara estimación, no revisión visual ni promesa de legibilidad.
        commands.insert(1, f'(setq datra:*height* {number(max(scale*3.0,0.05))})')
    expected_counts = "'("+' '.join(str(counts[kind]) for kind in TYPES)+')'
    page_data = None
    if bounds and presentation is not None:
        check, views, sizes, page_data = cad_presentation.compile_pages(
            stage, rows, presentation, layout, owner, audit.name, label_index, literal, number)
        commands.insert(0, check)
        commands.insert(2, "(setq datra:*symbol-scales* '(" + ' '.join(
            f'({literal(kind)} . {number(size)})' for kind,size in sizes.items()) + '))')
        detail_count = "(datra:cajetin " + expected_counts + ")"
        for line in views:
            commands.append(line)
            if line.startswith('(datra:page '):
                commands.append(detail_count)
    elif bounds:
        commands.append('(datra:viewport ' + ' '.join(number(v) for v in bounds) + ')')
    commands.append('(datra:finish '+literal((destination/'resultados_cad/reporte_nativo.txt').as_posix())+
                    f' {len(rows)} {len(drawn_edges)} '+expected_counts+')')
    # Evitar una línea SCRIPT de megabytes para General: el programa multílínea
    # se carga como LISP. Sigue habiendo exactamente dos SCR operativos.
    program='(defun datra:draw ()\n'+'\n'.join(commands)+'\n)\n(princ)\n'
    static_check(program)
    (stage/'cad_datos.lsp').write_text(program,encoding='utf-8',newline='\n')
    drawing=header+'(load '+literal((destination/'cad_datos.lsp').as_posix())+')\n(datra:run \'datra:draw)\n'
    if page_data is not None:
        helper = cad_presentation.RUNTIME
        static_check(helper.read_text(encoding='utf-8'))
        shutil.copyfile(helper,stage/helper.name)
        drawing = f'(load {literal((destination/helper.name).as_posix())})\n'+drawing
    if not rows:
        drawing = header + '(alert "PENDIENTE_EVIDENCIA: no hay CSV02 habilitado para dibujo. No se inserto geometria.")\n'
    for name, text in [('01_configurar_plano.scr',setup),('02_dibujar_auditoria.scr',drawing)]:
        static_check(text)
        (stage/name).write_text(text,encoding='utf-8',newline='\n')
    static_check(RUNTIME.read_text(encoding='utf-8'))
    shutil.copyfile(RUNTIME,stage/RUNTIME.name)
    paper = dict(formato='ISO_A1_841x594_MM',orientacion='HORIZONTAL',laminas=1,layout=layout,
                 revision_nativa='PENDIENTE_EVIDENCIA',zona_mapa_mm=[145,70,675,535],
                 escala_m_por_mm_estimada=scale,etiquetas_requeridas=len(rows),
                 estado_final='BLOQUEADO_HASTA_IMPRESION_Y_ACEPTACION',
                 alerta_densidad=bool(rows and len(rows)>530*490/(30*4)),
                 limite_densidad='Diagnóstico de ocupación; no umbral de aceptación',
                 evidencia_legibilidad=None)
    paper.update(altura_etiqueta_papel_mm_propuesta=3.0,altura_coordenada_papel_mm_propuesta=2.5)
    if page_data is not None:
        paper.update(laminas=len(page_data['hojas']), hojas=page_data['hojas'],
                     escala_m_por_mm_estimada=None,
                     altura_etiqueta_papel_mm_propuesta=page_data['perfil']['identificador_mm'],
                     altura_coordenada_papel_mm_propuesta=page_data['perfil']['coordenada_mm'])
    report = dict(estado='COMPLETADO_TECNICO',ejecucion_nativa='PENDIENTE_EVIDENCIA',modo=mode,
                  cp04='COMPILADO_PRELIMINAR' if rows else 'PENDIENTE_EVIDENCIA',
                  archivo_base=base.relative_to(audit/'entrada').as_posix(),base_sha256=sha256(base),copia_relativa='resultados_cad/'+copy_name,
                  elementos=len(rows),aristas=len(drawn_edges),distancias=drawn_edges,conteos=dict(counts),
                  controles_crs=crs_info['estado'],unidades_acreditadas=spec.get('unidades_verificadas',False),
                  etiquetas='P/C/E + número estable digest40bits; ID completo conservado en XDATA, colisiones bloqueantes',
                  topologia='CONFIRMADA' if drawn_edges else 'SOLO_PUNTOS_PRELIMINAR',
                  recursos='Bloques esquemáticos v1; no homologan material ni cable',
                  instrucciones='Abrir SOLO la copia_relativa y ejecutar SCR01 y SCR02 con SCRIPT, en ese orden. Revisar antes de guardar/imprimir.')
    if page_data is not None:
        report.update(presentacion='ADR-002', etiquetas='Coordenadas e IDs opcionales en Paper; índice y XDATA conservan ID completo')
    (stage/'reporte_validacion_cad.json').write_text(json_text(report),encoding='utf-8')
    (stage/'reporte_papel_A1.json').write_text(json_text(paper),encoding='utf-8')
    return report


def prepare_copy(audit, manifest):
    """Copia mutable separada de artefactos del compilador. Nunca sobreescribe DWG."""
    report = manifest.get('cad')
    if not report or not report.get('copia_relativa'): return None
    source = within(audit/'entrada'/report['archivo_base'],audit/'entrada')
    if sha256(source) != report['base_sha256']: raise PipelineError('Cambió la base CAD')
    target = within(audit/'salida'/report['copia_relativa'],audit/'salida')
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        # Modo exclusivo impide sobreescribir una edición del operador.
        with source.open('rb') as src, target.open('xb') as dst: shutil.copyfileobj(src,dst)
    return target
