"""Corridas independientes; una auditoría fallida no cancela las otras."""
from . import config
from .pipeline import run
from .reporting import verify, replace_retry
from .util import json_text, output_path

NAMES=('Natura','Mirador','Otay-Florido','Tijuana-General')


def batch(names=NAMES,dry_run=False,diagnostico=None,verify_only=False,emit=print,persist=True):
    results=[]
    for name in names:
        try:
            audit=config.audit_path(name)
            m=verify(audit) if verify_only else run(audit,dry_run,emit=emit,diagnostico=diagnostico)
            if not dry_run:
                from .cad import prepare_copy
                if not verify_only:prepare_copy(audit,m)
            results.append(dict(auditoria=name,estado=m['estado'],ejecucion_id=m.get('ejecucion_id'),
                                conteos=m.get('conteos'),checkpoints=m.get('checkpoints')))
        except Exception as exc:
            results.append(dict(auditoria=name,estado='FALLIDO',error=str(exc)))
            emit(f'FALLIDO {name}: {exc}')
    summary=dict(estado='FALLIDO' if any(r['estado']=='FALLIDO' for r in results) else 'PRELIMINAR',
                 modo='DRY_RUN' if dry_run else 'VERIFICACION' if verify_only else 'EJECUCION',auditorias=results)
    if persist and not dry_run and not verify_only:
        output=output_path(config.AUDITS/'_batch/salida',config.AUDITS)
        output.mkdir(parents=True,exist_ok=True)
        temp=output/'resumen_batch.tmp';temp.write_text(json_text(summary),encoding='utf-8')
        replace_retry(temp,output/'resumen_batch.json')
    return summary
