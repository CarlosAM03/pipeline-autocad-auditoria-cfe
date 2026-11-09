"""Custodia de paths públicos nuevos/modificados y oráculo congelado."""
import argparse
import hashlib
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FORBIDDEN={'.xlsx','.xls','.xlsm','.xlsb','.kmz','.kml','.dwg','.dwt','.zip','.pdf'}


def violations(paths, *, staged=False):
    errors=[]
    for name in paths:
        path=Path(name)
        if (path.suffix.lower() in FORBIDDEN or '00_RESPUESTAS_ORIGINALES' in name or
            (staged and path.name.lower() in ('logo_datra.png','mapatijuanaparamarco.png')) or
            name.startswith('Auditorias-20261104T035633Z-1-001/') or
            name.startswith('AuditoriaCFE/auditorias/_comparativa_A4_1_1/') or
            name.startswith(('AuditoriaCFE/auditorias/_a4_2/', 'AuditoriaCFE/auditorias/_a4_2_1/')) or
            any(part in ('.venv','.venv-cp01','entrada','salida','temporales','_runtime','__pycache__') for part in path.parts) or
            (name.startswith('AuditoriaCFE/auditorias/') and path.name in
             ('configuracion.json','topologia_confirmada.csv','resoluciones_manual.csv'))):
            errors.append(name)
    return errors


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged',action='store_true')
    args=parser.parse_args(argv)
    command=['git','diff','--cached','--name-only','--diff-filter=AM','-z'] if args.staged else ['git','ls-files','-z']
    names=subprocess.check_output(command,cwd=ROOT).decode().split('\0')
    # Las tres configs demo anteriores son deuda heredada, no permiso para agregar más.
    legacy={'AuditoriaCFE/auditorias/'+n+'/configuracion.json' for n in ('Demo-Sintetica','Prueba-Historica-Mirador','Prueba-Historica-Otay')}
    inherited_pdf='AuditoriaCFE/Codex/00_Diagnostico/02_CAD_Origen/FASE3B_Integracion_Desde_PlanoTijuana/PlantillaMarcoDatraMapaTijuana.pdf'
    if not args.staged and hashlib.sha256((ROOT/inherited_pdf).read_bytes()).hexdigest()=='48e5074803b58e2e7f2b22f8a294df34c3aa09d5eaf31511d180e055b15500ef':
        legacy.add(inherited_pdf)
    errors=violations([n for n in names if n and (args.staged or n not in legacy)], staged=args.staged)
    oracle=ROOT/'AuditoriaCFE/tests/fixtures/reporting_7baa82c.py'
    normalized=oracle.read_text(encoding='utf-8').encode('utf-8')
    expected='443e5eab1cd9f86651f381721f8f38cc7eac2512d5a52230c429765428d2c4e8'
    if hashlib.sha256(normalized).hexdigest()!=expected:errors.append('Oráculo legacy cambió')
    if errors:
        print('PUBLICACION BLOQUEADA:\n'+'\n'.join(errors));return 2
    print('Custodia pública y hash del oráculo OK (no equivale a auditoría de licencia de recursos heredados).')
    return 0


if __name__=='__main__':raise SystemExit(main())
