"""Ensayo opt-in Core Console sobre la copia declarada, nunca sobre la base.

Ejecutar desde raíz: python AuditoriaCFE/herramientas/ensayo_nativo.py --auditoria
Mirador --pdf MIRADOR_DIAGNOSTICO_A1.pdf. No participa en CI ni acredita campo.
"""
import argparse
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from auditoriacfe.config import audit_path
from auditoriacfe.cad import literal,prepare_copy
from auditoriacfe.reporting import verify
from auditoriacfe.util import PipelineError,json_text,sha256


def geometry(path):
    return sorted(line for line in path.read_text(encoding='utf-8',errors='replace').splitlines()
                  if line.startswith(('INSERT|','TEXT|','LWPOLYLINE|','ATTRIB|','LINE|','CIRCLE|','LENGTH|')))


def execute(audit,pdf_name,exe,rollback=False):
    manifest=verify(audit);copy=prepare_copy(audit,manifest)
    if copy is None:raise PipelineError('No hay copia CAD declarada')
    if copy.resolve()==(audit/'entrada'/manifest['cad']['archivo_base']).resolve():
        raise PipelineError('No ejecutar sobre base de entrada')
    if not re.fullmatch(r'[A-Za-z0-9_-]+\.pdf',pdf_name):raise PipelineError('Nombre PDF inválido')
    out=audit/'salida';root=out/'resultados_cad'
    work=root/('ensayo_'+uuid.uuid4().hex[:12]);work.mkdir()
    pdf=work/pdf_name
    # El owner usa el mismo digest que el compilador, no una identidad alternativa.
    from auditoriacfe.util import digest
    owner='AUD-'+digest(audit.name)
    layout=manifest['configuracion']['cad'].get('layout','DATRA_A1')
    mode=manifest['cad']['modo']
    setup='(setq test:trusted (getvar "TRUSTEDPATHS"))\n(setvar "TRUSTEDPATHS" (strcat test:trusted ";'+out.as_posix()+'"))\n'
    setup+='(load '+literal((out/'cad_runtime.lsp').as_posix())+')\n'
    def dump(name):return '(datra:evidence '+literal(copy.as_posix())+' '+literal((work/name).as_posix())+')\n'
    def call(name):return '_.SCRIPTCALL\n'+literal((out/name).as_posix())+'\n'
    script=setup+call('01_configurar_plano.scr')+call('02_dibujar_auditoria.scr')+dump('primera.txt')
    script+=call('02_dibujar_auditoria.scr')+dump('segunda.txt')
    if rollback:
        script+='(datra:run \'(lambda () (datra:draw) (setq datra:*ready* T) (datra:point "ROLLBACK_TEST" "DATRA_POSTE_V1" "POSTE" 0.0 0.0 "TEST" "TEST") (datra:fail "FALLO_SIMULADO_ROLLBACK")))\n'
        script+=dump('rollback.txt')
    script+='(datra:inspect '+literal(copy.as_posix())+' '+literal((work/'inspeccion.txt').as_posix())+')\n'
    script+='_.-PLOT\n_No\n'+layout+'\n\nDWG To PDF.pc3\n'+literal(pdf.as_posix())+'\n_No\n_Yes\n'
    script+='(setvar "TRUSTEDPATHS" test:trusted)\n_.QSAVE\n_.QUIT\n'
    def core(text,name):
        wrapper=work/(name+'.scr');wrapper.write_text(text,encoding='utf-8')
        log=work/(name+'.log')
        with log.open('wb') as stream:
            p=subprocess.run([str(exe),'/i',str(copy),'/s',str(wrapper),'/l','en-US'],stdout=stream,stderr=subprocess.STDOUT,timeout=240)
        raw=log.read_bytes();decoded=raw.decode('utf-16-le',errors='replace')
        unexpected=[line for line in decoded.splitlines() if re.search(r'; error:|Unknown command|DATRA FALLIDO',line,re.I) and 'FALLO_SIMULADO_ROLLBACK' not in line]
        if p.returncode or unexpected:raise PipelineError('Fallo nativo '+name+': '+str(unexpected[:5]))
        return log
    log=core(script,'ejecucion')
    first=geometry(work/'primera.txt');second=geometry(work/'segunda.txt')
    if first!=second:raise PipelineError('SCR02 no idempotente geométricamente')
    if rollback and geometry(work/'rollback.txt')!=second:raise PipelineError('UNDO no restituyó geometría')
    # Reabrir sin volver a dibujar: comprobar persistencia de las entidades.
    reopen=setup+'(setq datra:*owner* '+literal(owner)+' datra:*layout* '+literal(layout)+' datra:*mode* '+literal(mode)+')\n'
    reopen+=dump('reapertura.txt')+'(setvar "TRUSTEDPATHS" test:trusted)\n_.QUIT\n'
    core(reopen,'reapertura')
    if geometry(work/'reapertura.txt')!=second:raise PipelineError('Geometría no persistió tras reabrir')
    inserts=[line for line in second if line.startswith('INSERT|')]
    edges=[line for line in second if line.startswith('LWPOLYLINE|') and 'DATRA_RUTA' in line]
    if len(inserts)!=manifest['cad']['elementos'] or len(edges)!=manifest['cad']['aristas']:
        raise PipelineError('Conteos nativos distintos del compilador')
    lengths={line.split('|')[1]:float(line.split('|')[2]) for line in second if line.startswith('LENGTH|')}
    expected_lengths={row['arista_id']:row['distancia_plana_m'] for row in manifest['cad']['distancias']}
    if lengths.keys()!=expected_lengths.keys() or any(abs(lengths[k]-v)>1e-6 for k,v in expected_lengths.items()):
        raise PipelineError('IDs/longitudes de polilíneas nativas no coinciden')
    expected=manifest['cad']['conteos']
    for kind,tag in [('POSTE','TOTAL_POSTES'),('CAJA_EMP','TOTAL_CAJAS'),('EXCEDENTE','TOTAL_EXCEDENTES')]:
        if 'ATTRIB|'+tag+'|'+str(expected.get(kind,0)) not in second:
            raise PipelineError('Cajetín nativo no actualizado: '+tag)
    if not pdf.is_file():raise PipelineError('No se generó PDF nativo')
    report=work/'reporte_nativo.txt'
    report.write_text('\n'.join(['SOLO_EVIDENCIA_TECNICA; PENDIENTE_OWNER',f'modo={mode}',f'INSERT={len(inserts)}',f'ARISTAS={len(edges)}','IDEMPOTENCIA=OK','REAPERTURA=OK','ROLLBACK='+('OK' if rollback else 'NO_SOLICITADO'),*second])+'\n',encoding='utf-8')
    files=[copy,pdf,report,log,work/'reapertura.log']
    acta=dict(schema='evidencia-nativa-v1',ejecucion_id=manifest['ejecucion_id'],resultado='PROBADO_AUTOCAD_CORE',aceptacion_humana='PENDIENTE',
              modo=mode,INSERT=len(inserts),aristas=len(edges),idempotencia=True,persistencia=True,rollback=rollback,
              longitudes_nativas_m=lengths,
              base_sha256=manifest['cad']['base_sha256'],runtime_sha256=sha256(out/'cad_runtime.lsp'),
              archivos=[dict(archivo=p.relative_to(root).as_posix(),sha256=sha256(p),bytes=p.stat().st_size) for p in files])
    (root/'acta_evidencia_nativa.json').write_text(json_text(acta),encoding='utf-8')
    (work/'resultado.json').write_text(json_text(acta),encoding='utf-8')
    return acta


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--auditoria',required=True);p.add_argument('--pdf',required=True)
    p.add_argument('--exe',default='C:/Program Files/Autodesk/AutoCAD 2026/accoreconsole.exe');p.add_argument('--rollback',action='store_true')
    a=p.parse_args()
    print(json_text(execute(audit_path(a.auditoria),a.pdf,Path(a.exe),a.rollback)))


if __name__=='__main__':main()
