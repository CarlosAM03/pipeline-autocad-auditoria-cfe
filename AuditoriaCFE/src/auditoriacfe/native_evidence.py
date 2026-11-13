"""Verificación independiente de resultados CAD mutables, sin aceptación automática."""
import json
from .util import PipelineError, sha256, within


def verify_native(audit):
    root=within(audit/'salida/resultados_cad',audit)
    path=within(root/'acta_evidencia_nativa.json',root)
    if not path.is_file():
        raise PipelineError('PENDIENTE_EVIDENCIA: no existe acta nativa independiente')
    acta=json.loads(path.read_text(encoding='utf-8'))
    if acta.get('schema')!='evidencia-nativa-v1' or not acta.get('archivos'):
        raise PipelineError('Contrato de evidencia nativa inválido')
    from .reporting import verify
    manifest=verify(audit)
    if acta.get('ejecucion_id')!=manifest['ejecucion_id']:
        raise PipelineError('Evidencia nativa corresponde a otra ejecución')
    for item in acta['archivos']:
        file=within(root/item['archivo'],root)
        if sha256(file)!=item['sha256'] or file.stat().st_size!=item['bytes']:
            raise PipelineError('Resultado CAD mutable cambió: '+item['archivo'])
    return dict(integridad='OK',validacion_nativa=acta.get('resultado','NO_DETERMINADO'),
                aceptacion_humana=acta.get('aceptacion_humana','PENDIENTE'),
                advertencia='Hash no acredita CRS, topología ni firma humana; consultar evidencia y responsable')
