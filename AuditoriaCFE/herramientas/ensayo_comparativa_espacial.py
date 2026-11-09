import csv, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
import fitz

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'src'))
from auditoriacfe.cad import literal
from auditoriacfe.util import PipelineError,sha256,within
EXE=Path('C:/Program Files/Autodesk/AutoCAD 2026/accoreconsole.exe')
INSPECTOR=PROJECT/'src/auditoriacfe/cad_diagnostics.lsp'

def console(dwg,work,stem,body):
    script=work/(stem+'.scr');script.write_text(body,encoding='utf-8')
    with (work/(stem+'.log')).open('wb') as f:
        process=subprocess.run([str(EXE),'/i',str(dwg),'/s',str(script),'/l','en-US'],
            cwd=work,stdout=f,stderr=subprocess.STDOUT,timeout=1100)
    raw=(work/(stem+'.log')).read_bytes()
    log=raw.decode('utf-16-le' if b'\0' in raw[:100] else 'cp1252',errors='replace')
    (work/(stem+'.txt')).write_text(log,encoding='utf-8')
    errors=[line.strip() for line in log.splitlines() if re.search(r'; error:|Unknown command|DATRA FALLIDO',line,re.I)]
    if process.returncode or errors:
        raise RuntimeError((process.returncode,errors[:12]))
    return log

def capture(path):
    return [json.loads(line) for line in path.read_text(encoding='cp1252').splitlines()]
def geometry(rows):
    return sorted(json.dumps({k:v for k,v in r.items() if k!='handle'},sort_keys=True)
        for r in rows if r['kind'] in ('owned','inherited_model','attribute'))

def run(job):
    name,radius=job
    audit=PROJECT/'auditorias/_comparativa_A4_1_1'/name/f'{radius:03d}m'
    manifest=json.loads((audit/'MANIFIESTO_VARIANTE.json').read_text());out=audit;dwg=within(out/manifest['cad']['copia_relativa'],out/'resultados_cad')
    if dwg.name!=f'{name}_A4_1_1_{radius:03d}m.dwg' or sha256(dwg)!=manifest['cad']['base_sha256']:
        raise PipelineError('El ensayo requiere la copia experimental recién preparada')
    work=dwg.parent/'evidencia';work.mkdir(exist_ok=False)
    sheets=json.loads((out/'presentacion_paginas.json').read_text())['hojas']
    layout=sheets[0]['layout']
    def q(path):return literal(path.as_posix())
    trusted='(setq a4:trusted (getvar "TRUSTEDPATHS"))\n'
    trusted+=f'(setvar "TRUSTEDPATHS" (strcat a4:trusted ";" {q(out)} ";" {q(INSPECTOR.parent)}))\n'
    runtime=f'(load {q(out/"cad_runtime.lsp")})\n(load {q(INSPECTOR)})\n'
    def scr(name):return f'_.SCRIPTCALL\n{q(out/name)}\n'
    def export(name):return f'(dc:export {q(dwg)} {q(work/(name+".jsonl"))})\n'
    restore='(setvar "TRUSTEDPATHS" a4:trusted)\n'
    body=trusted+runtime+export('base')+scr('01_configurar_plano.scr')+scr('02_dibujar_auditoria.scr')+export('primera')
    body+=scr('02_dibujar_auditoria.scr')+export('segunda')+restore+'_.QSAVE\n_.QUIT\n'
    console(dwg,work,'ejecucion',body)
    first,second=capture(work/'primera.jsonl'),capture(work/'segunda.jsonl')
    assert geometry(first)==geometry(second), 'No idempotente'
    assert [r for r in capture(work/'base.jsonl') if r['kind']=='inherited_model']==[r for r in second if r['kind']=='inherited_model'], 'Cambió el inventario heredado'
    print(name,radius,'SCR y repeticion OK',len(sheets),flush=True)
    body=trusted+runtime+export('reapertura')+'(setvar "PDFSHX" 0)\n'
    pages=[]
    for sheet in sheets:
        page=work/f"{sheet['numero']:03d}.pdf";pages.append(page)
        body+='_.-PLOT\n_No\n'+sheet['layout']+'\n\nDWG To PDF.pc3\n'+q(page)+'\n_No\n_Yes\n'
    body+=restore+'_.QSAVE\n_.QUIT\n'
    console(dwg,work,'trazado',body)
    validate(job)


def validate(job):
    name,radius=job
    audit=PROJECT/'auditorias/_comparativa_A4_1_1'/name/f'{radius:03d}m'
    manifest=json.loads((audit/'MANIFIESTO_VARIANTE.json').read_text())
    out=audit
    dwg=within(out/manifest['cad']['copia_relativa'],out/'resultados_cad')
    work=dwg.parent/'evidencia'
    sheets=json.loads((out/'presentacion_paginas.json').read_text())['hojas']
    pages=[work/f"{sheet['numero']:03d}.pdf" for sheet in sheets]
    first,second=capture(work/'primera.jsonl'),capture(work/'segunda.jsonl')
    assert geometry(first)==geometry(second)
    assert [r for r in capture(work/'base.jsonl') if r['kind']=='inherited_model']==[r for r in second if r['kind']=='inherited_model']
    rows=capture(work/'reapertura.jsonl')
    assert geometry(second)==geometry(rows), 'No persistió geometría'
    source=out/'COORDENADAS_ADMITIDAS_VISUALIZACION.csv'
    with source.open(encoding='utf-8',newline='') as f:
        points={r['elemento_id']:r for r in csv.DictReader(f)}
    blocks=[r for r in rows if r['kind']=='owned' and r['space']=='Model' and r['type']=='INSERT']
    assert len(blocks)==len(points)==len({r['id'] for r in blocks})
    from math import dist
    residual=max(dist(r['position'][:2],(float(points[r['id']]['este_m']),float(points[r['id']]['norte_m']))) for r in blocks)
    assert residual<1e-7
    assert all(r['block']=='DATRA_'+points[r['id']]['tipo']+'_V1' for r in blocks)
    with (out/'indice_presentacion.csv').open(encoding='utf-8',newline='') as f:
        index={r['elemento_id']:r for r in csv.DictReader(f)}
    assert points.keys()==index.keys()
    text=[r for r in rows if r['kind']=='owned' and r['type']=='TEXT' and r['layer']=='DATRA_A4_ETIQUETA' and r['id'] in points]
    assert len(text)==len(points)
    assert all(r['space']==index[r['id']]['layout'] and r['value']==index[r['id']]['coordenada_geografica'] for r in text)
    assert Counter(r['id'] for r in text)==dict.fromkeys(points,1)
    layout_metrics={}
    sector_marks=[r for r in rows if r['kind']=='owned' and r['type']=='TEXT' and r['id'].startswith('SECTOR_A4-')]
    assert len(sector_marks)==len(sheets)-1
    assert {r['value'] for r in sector_marks}=={f'D{i}' for i in range(2,len(sheets)+1)}
    assert all(r['space']==sheets[0]['layout'] for r in sector_marks)
    text_by_layout={}
    for r in text+sector_marks:text_by_layout.setdefault(r['space'],[]).append(r)
    for sheet in sheets:
        lay=sheet['layout']
        viewport=[r for r in rows if r['kind']=='viewport' and r['layout']==lay and r['layer']=='DATRA_VIEWPORTS' and r['width_paper']>500]
        assert len(viewport)==1, (lay,viewport)
        vp=viewport[0]
        assert abs(vp['view_height_model']/465-sheet['escala'])<1e-6 and dist(vp['view_center_dcs'][:2],sheet['centro'])<1e-5
        boxes=[]
        for r in text_by_layout.get(lay,[]):
            x,y,*_=r['position'];a,b=r['textbox_local']
            boxes.append((x+a[0],y+a[1],x+b[0],y+b[1]))
        from auditoriacfe.presentation import overlaps
        from itertools import combinations
        collisions=sum(overlaps(a,b) for a,b in combinations(boxes,2))
        clipped=sum(a<145 or b<70 or c>675 or d>535 for a,b,c,d in boxes)
        totals={r['tag']:r['value'] for r in rows if r['kind']=='attribute' and r['layout']==lay and r['tag'].startswith('TOTAL_')}
        assert totals==dict(TOTAL_POSTES=str(manifest['cad']['conteos'].get('POSTE',0)),
            TOTAL_CAJAS=str(manifest['cad']['conteos'].get('CAJA_EMP',0)),TOTAL_EXCEDENTES=str(manifest['cad']['conteos'].get('EXCEDENTE',0))), (lay,totals)
        assert not clipped and collisions==0
        sheet_attributes={r['tag']:r['value'] for r in rows if r['kind']=='attribute' and r['layout']==lay}
        assert sheet_attributes['NUM_PLANO']==f"{sheet['numero']}/{len(sheets)}" and sheet_attributes['AUDITORIA']==name
        layout_metrics[lay]=dict(aabb=collisions,recortes=clipped,cajetin=totals)
    merged=fitz.open()
    for sheet,pdf in zip(sheets,pages):
        info=subprocess.run(['pdfinfo',str(pdf)],check=True,capture_output=True).stdout
        assert b'(A1)' in info and re.search(rb'Pages:\s+1\b',info), info
        assert sheet['layout'].encode() in info
        with fitz.open(pdf) as doc:
            assert len(doc)==1 and 'AutoCAD' in doc.metadata['creator']
            assert doc[0].rect.width>doc[0].rect.height and doc[0].get_cdrawings()
            doc[0].get_pixmap(dpi=53).save(work/f"{sheet['numero']:03d}_fitz.png")
            merged.insert_pdf(doc)
    merged.set_metadata(dict(title=f'{name} - {radius} m - DIAGNOSTICO NO VERIFICADO',creator='AutoCAD Core Console 2026; compilacion de paginas PyMuPDF'))
    pdf=dwg.with_suffix('.pdf')
    merged.save(pdf,garbage=4,deflate=True)
    info=subprocess.run(['pdfinfo',str(pdf)],check=True,capture_output=True).stdout
    assert re.search(rb'Pages:\s+'+str(len(sheets)).encode()+rb'\b',info)
    (work/'pdfinfo.txt').write_bytes(info)
    subprocess.run(['pdftoppm','-r','43','-png',str(pdf),str(work/'poppler')],check=True)
    with fitz.open(pdf) as doc:
        assert len(doc)==len(sheets)
        page=max(sheets,key=lambda sheet:sheet['etiquetas'])['numero']-1
        doc[page].get_pixmap(dpi=115).save(work/'detalle_mas_denso.png')
    assert all(sha256(out/f)==h for f,h in manifest['originales'].items())
    metrics=dict(auditoria=name,ejecucion=manifest['ejecucion_id'],puntos=len(points),xy_max=residual,
        paginas=len(sheets),layouts=layout_metrics,sha_dwg=sha256(dwg),sha_pdf=sha256(pdf))
    (work/'validacion.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    with (work/'SHA256SUMS.txt').open('w',encoding='utf-8') as f:
        for path in sorted([dwg,pdf,*work.glob('*')]):
            if path.is_file() and path.name!='SHA256SUMS.txt':
                f.write(f'{sha256(path)}  {path.relative_to(dwg.parent).as_posix()}\n')
    print(name,radius,'VALIDADO',len(points),len(sheets),residual,flush=True)

if __name__=='__main__':
    from concurrent.futures import ThreadPoolExecutor, as_completed
    jobs=[(n,r) for n in ('Natura','Mirador','Otay-Florido') for r in (50,100,200,300)]
    if sys.argv[1:]:
        jobs=[(n,r) for n,r in jobs if f'{n}/{r:03d}m' in sys.argv[1:]]
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures={pool.submit(run,job):job for job in jobs}
        errors=[]
        for future in as_completed(futures):
            job=futures[future]
            try:future.result()
            except Exception:
                import traceback
                traceback.print_exc()
                errors.append(job)
    print('NATIVO',len(jobs)-len(errors),'OK',errors,flush=True)
    raise SystemExit(bool(errors))
