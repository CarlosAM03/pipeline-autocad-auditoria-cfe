"""Consolida la revisión A4.1.1 después de los trazados Core Console."""
import json
import shutil
import zipfile
from collections import Counter
from xml.etree import ElementTree as ET

import fitz

from comparativa_espacial import (DECISIONS, EXCLUDED, INCLUDED, NAMES, PROJECT, RADII, ROOT,
                                  base, csv_file, dicts, read, save, sha256, verify, verify_native)

DOC = PROJECT/'Codex/04_Diagnostico_Presentacion_CAD/A4_1_1_Depuracion_Espacial'


def json_read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def capture_exclusion(variant, name, out, evidence, excluded):
    if not excluded:
        save(evidence/'SECTOR_HUERFANO.json',dict(estado='SIN_EXCLUSIONES_EN_VARIANTE'))
        return
    sample=max((r for r in excluded if r['distancia_al_componente_conservado_m']),
               key=lambda r:float(r['distancia_al_componente_conservado_m']),default=excluded[0])
    baseline=base(name)/'salida'
    index={r['elemento_id']:r for r in read(baseline/'indice_presentacion.csv')}
    coords={r['elemento_id']:r for r in read(baseline/'02_DIAGNOSTICO_NO_VERIFICADO.csv')}
    key=sample['elemento_id']
    if key not in index:
        save(evidence/'SECTOR_HUERFANO.json',dict(estado='SIN_VISTA_BASE',elemento_id=key))
        return
    row=coords[key]
    plan=json_read(baseline/'presentacion_paginas.json')['hojas']
    primary=int(index[key]['pagina'])-1
    def paper(sheet):
        scale=sheet['escala']
        cx,cy=sheet['centro']
        return 410+(float(row['este_m'])-cx)/scale,302.5+(float(row['norte_m'])-cy)/scale
    def crop(pdf, sheet, index, output):
        x,y=paper(sheet)
        def pt(m):return m*72/25.4
        with fitz.open(pdf) as doc:
            doc[index].get_pixmap(dpi=140,clip=fitz.Rect(pt(max(0,x-28)),pt(max(0,594-y-35)),
                             pt(min(841,x+72)),pt(min(594,594-y+30)))).save(output)
    source=baseline/'resultados_cad'/f'{name}_A4_1.pdf'
    crop(source,plan[primary],primary,evidence/'HUERFANO_BASE_A4_1.png')
    pages=json_read(variant/'presentacion_paginas.json')['hojas']
    in_view=[(i,s) for i,s in enumerate(pages) if 145<=paper(s)[0]<=675 and 70<=paper(s)[1]<=535]
    if in_view:
        i,s=min(in_view,key=lambda item:item[1]['escala'])
        crop(out,s,i,evidence/'HUERFANO_CONTEXTO_SIN_SIMBOLO.png')
    save(evidence/'SECTOR_HUERFANO.json',dict(elemento_id=key,pagina_base=primary+1,
         pdf_base_sha256=sha256(source),pagina_contexto=i+1 if in_view else None,
         estado='CONTEXTO_EN_VARIANTE' if in_view else 'FUERA_DE_VISTAS_DE_LA_VARIANTE'))


def finish(name,radius):
    variant=ROOT/name/f'{radius:03d}m'
    cad=variant/'resultados_cad'
    work=cad/'evidencia'
    summary=json_read(variant/'RESUMEN_VARIANTE.json')
    manifest=json_read(variant/'MANIFIESTO_VARIANTE.json')
    excluded=read(variant/EXCLUDED)
    decisions=read(variant/DECISIONS)
    retained=read(variant/INCLUDED)
    assert len(decisions)==summary['total_original']==len(retained)+len(excluded)
    assert {r['elemento_id'] for r in retained}.isdisjoint({r['elemento_id'] for r in excluded})
    for f,h in manifest['originales'].items():
        assert sha256(variant/f)==sha256(base(name)/'salida'/f)==h
    projected={r['elemento_id']:r for r in read(variant/'02_DIAGNOSTICO_NO_VERIFICADO.csv')}
    assert all(r==projected[r['elemento_id']] for r in retained)
    config=json_read(variant/'CONFIGURACION_VARIANTE.json')['configuracion']
    baseline_cfg=json_read(base(name)/'configuracion.json')
    assert config['cad']['presentacion']==baseline_cfg['cad']['presentacion']
    assert all(config.get(k)==baseline_cfg.get(k) for k in ('geografia_permitida','crs_validado','kmz'))
    assert manifest['id_bomberos']==(494 if name=='Otay-Florido' else 0)
    assert not (variant/'02_elementos_proyectados.csv').exists()
    for fname in ('01_trazabilidad_limpieza.xlsx','02_trazabilidad_transformacion.xlsx'):
        with zipfile.ZipFile(variant/fname) as z:
            assert z.testzip() is None
            workbook=ET.fromstring(z.read('xl/workbook.xml'))
            sheet_names=[el.attrib['name'] for el in workbook.iter() if el.tag.endswith('}sheet')]
            assert sheet_names[-1]=='Decision_Visual'
            sheet=ET.fromstring(z.read(f'xl/worksheets/sheet{len(sheet_names)}.xml'))
            assert sum(e.tag.endswith('}row') for e in sheet.iter())==len(decisions)+1
            assert not any(e.tag.endswith('}f') for e in sheet.iter())
    non_ident=[json.loads(l) for l in (variant/'linaje_y_calidad.jsonl').read_text(encoding='utf-8').splitlines()]
    csv_file(variant/'OCURRENCIAS_ORIGEN_NO_EVALUADAS.csv',
             ['ocurrencia_id','archivo','hoja','fila','estado_origen','motivo','incidencias'],
             ([r['ocurrencia_id'],r['archivo_relativo'],r['hoja'],r['fila'],r['estado'],
               'FUERA_ALCANCE' if r['estado']=='FUERA_ALCANCE' else 'COORDENADA_INVALIDA'
               if any(i['codigo'] in ('COORD_FUERA_RANGO','COORD_NO_INTERPRETABLE') for i in r['incidencias'])
               else 'PENDIENTE_REVISION','|'.join(i['codigo'] for i in r['incidencias'])]
              for r in non_ident if not r['elemento_id']))
    proof=work/'validacion.json'
    pdf=(variant/manifest['cad']['copia_relativa']).with_suffix('.pdf')
    if proof.is_file():
        metrics=json_read(proof)
        dwg=pdf.with_suffix('.dwg')
        assert sha256(dwg)==metrics['sha_dwg'] and sha256(pdf)==metrics['sha_pdf']
        assert metrics['puntos']==len(retained) and metrics['paginas']==summary['paginas']
        pages=json_read(variant/'presentacion_paginas.json')['hojas']
        assert all(p['escala']==6 for p in pages if p['vista']=='DETALLE')
        assert manifest['cad']['aristas']==0
        with (work/'reapertura.jsonl').open(encoding='cp1252') as stream:
            assert all(r['type']=='INSERT' for r in map(json.loads,stream)
                       if r['kind']=='owned' and r['space']=='Model')
        assert sum(p['etiquetas'] for p in pages)==len(retained)
        assert all(p['etiquetas']>0 for p in pages if p['vista']=='DETALLE')
        with fitz.open(pdf) as document:
            assert len(document)==summary['paginas']
            assert all((round(p.rect.width*25.4/72,3),round(p.rect.height*25.4/72,3))==(841.022,594.078)
                       for p in document)
        summary.update(cad='VALIDADO_TECNICAMENTE_DIAGNOSTICO',
            colisiones_etiquetas=sum(m['aabb'] for m in metrics['layouts'].values()),
            recortes_etiquetas=sum(m['recortes'] for m in metrics['layouts'].values()),
            paginas_sin_utilidad=sum(p['etiquetas']==0 and p['vista']!='GENERAL' for p in pages),
            residuo_xy_max=metrics['xy_max'])
        shutil.copyfile(work/'001_fitz.png',work/'CAPTURA_GENERAL.png')
        capture_exclusion(variant,name,pdf,work,excluded)
    else:
        summary['cad']='PENDIENTE_O_FALLIDO_SIN_ACTA'
    summary['excluidos_fuera_ambito_candidato']=sum(r['estado_territorial']=='FUERA_AMBITO_CANDIDATO' for r in excluded)
    summary['conservados_fuera_ambito_candidato']=summary['fuera_ambito_candidato']-summary['excluidos_fuera_ambito_candidato']
    save(variant/'RESUMEN_VARIANTE.json',summary)
    extras=[r for r in read(variant/'SUMMARY_COORDENADAS_DESCARTADAS.csv') if '::' in r['metrica']]
    extras=[r for r in extras if not r['metrica'].startswith('subruta_asociada::')]
    excluded_ids={r['elemento_id'] for r in excluded}
    associated=Counter(route for _,route in {(r['elemento_id'],r['ruta_original'])
        for r in read(variant/'asociaciones_elemento_ruta.csv') if r['elemento_id'] in excluded_ids})
    csv_file(variant/'SUMMARY_COORDENADAS_DESCARTADAS.csv',['metrica','valor'],
             [*summary.items(),*((r['metrica'],r['valor']) for r in extras),
              *((f'subruta_asociada::{k}',v) for k,v in sorted(associated.items()))])
    groups=json_read(variant/'COMPONENTES_ESPACIALES.json')
    lines=[f'# {name} · {radius} m · diagnóstico experimental','',
        f"Identidades de referencia {summary['total_original']}. Conservadas {len(retained)}. "
        f"Excluidas de la vista {len(excluded)} ({summary['porcentaje_excluido']:.2f} %).",
        f"Posiciones distintas de poste {summary['posiciones_poste']}. Componentes {len(groups)}. "
        f"Conservados {summary['componentes_conservados']}. Microcomponentes {summary['microcomponentes']}.",
        'Tamaños de 1 a 5: '+', '.join(str(summary[f'componentes_{i}']) for i in range(1,6))+'.',
        f"Páginas {summary['paginas']}, cambio frente a A4.1 {summary['diferencia_paginas']:+}. "
        f"Estado CAD {summary['cad']}.",
        f"Tipos excluidos POSTE/CAJA_EMP/EXCEDENTE: {summary['poste_excluidos']}/"
        f"{summary['caja_emp_excluidos']}/{summary['excedente_excluidos']}.",
        f"Media al vecino {summary['vecino_media']:.2f} m y clase modal {summary['vecino_moda']}. "
        f"Terminales conservados {summary['terminales']}, incidencias de puente {summary['puentes']}.",
        f"Fuera de AGEM candidato {summary['fuera_ambito_candidato']}. Cobertura DATRA pendiente "
        f"para {summary['pendientes_territoriales']}. Candidatos de coincidencia/proximidad {summary['candidatos_fusion']}.",
        '', '## Custodia e interpretación','',
        'Las exclusiones afectan esta vista. Un microcomponente puede corresponder a infraestructura legítima. '
        'El grafo es auxiliar de densidad y las líneas de llamada del plano pertenecen a Paper Space.',
        'El resumen CSV desglosa subrutas y fuentes prevalentes y todas las ocurrencias de fuentes afectadas. '
        'COMPONENTES_ESPACIALES.json identifica el poste conservado más cercano a cada microcomponente. '
        'El linaje, el índice de página y los dos XLSX permiten revisar la decisión por ID.',
        '', '## Pruebas','',
        'Aprobados CSV, XLSX y reconciliación de identidades, junto con la custodia de la referencia. '
        f"CAD {summary['cad']}. La impresión física y la aceptación humana están pendientes."]
    text='\n'.join(lines)+'\n'
    for filename in ('RESUMEN_VARIANTE.md','SUMMARY_COORDENADAS_DESCARTADAS.md'):
        (variant/filename).write_text(text,encoding='utf-8')
    files={p.relative_to(variant).as_posix():sha256(p) for p in sorted(variant.rglob('*'))
           if p.is_file() and p.name not in ('SHA256SUMS.txt','MANIFIESTO_VARIANTE.json')
           and p.suffix.lower() not in ('.bak','.dwl','.dwl2')}
    manifest.update(artefactos=files,resultado=summary['cad'],aceptacion_humana='PENDIENTE')
    save(variant/'MANIFIESTO_VARIANTE.json',manifest)
    files['MANIFIESTO_VARIANTE.json']=sha256(variant/'MANIFIESTO_VARIANTE.json')
    (variant/'SHA256SUMS.txt').write_text(''.join(f'{h}  {f}\n' for f,h in sorted(files.items())),encoding='utf-8')
    assert all(sha256(variant/f)==h for f,h in files.items())
    return summary


def main():
    DOC.mkdir(exist_ok=True)
    all_rows=[]
    matrix=[]
    aggregate=[]
    for name in NAMES:
        verify(base(name))
        verify_native(base(name))
        rows=[finish(name,r) for r in RADII]
        all_rows.extend(rows)
        dicts(ROOT/name/f"COMPARATIVA_{name.upper().replace('-','_')}.csv",list(rows[0]),rows)
        subset=read(ROOT/name/'MATRIZ_INCLUSION_EXCLUSION.csv')
        matrix.extend(subset)
        cols=['auditoria','tipo',*[f'{r:03d}m' for r in RADII]]
        aggregate.extend([(*k,n) for k,n in sorted(Counter(tuple(row[c] for c in cols) for row in subset).items())])
    columns=list(dict.fromkeys(k for row in all_rows for k in row))
    dicts(ROOT/'COMPARATIVA_GLOBAL_A4_1_1.csv',columns,all_rows)
    shutil.copyfile(ROOT/'COMPARATIVA_GLOBAL_A4_1_1.csv',DOC/'COMPARATIVA_GLOBAL_A4_1_1.csv')
    dicts(ROOT/'MATRIZ_INCLUSION_EXCLUSION.csv',list(matrix[0]),matrix)
    csv_file(DOC/'MATRIZ_INCLUSION_EXCLUSION.csv',[*cols,'cantidad'],aggregate)
    print('FIN',Counter(r['cad'] for r in all_rows),'paginas',sum(r['paginas'] for r in all_rows),flush=True)


if __name__=='__main__':
    main()
