"""Resoluciones del responsable: identidad de fuente y evidencia obligatorias."""
import csv
from datetime import date
from .util import PipelineError, sha256, within

HEADER = 'resolucion_id,archivo_sha256,archivo_relativo,hoja,fila,valor_original,campo,accion,valor_nuevo,motivo,evidencia,responsable,fecha,aprobada'.split(',')
ACTIONS = {'EXCLUIR':'registro', 'CORREGIR_COORDENADA':'coordenada', 'CORREGIR_TIPO':'tipo',
           'EXCEPCION_AMBITO':'ambito', 'ID_EQUIPO_ACREDITADO':'id_equipo'}


def load_resolutions(audit, records):
    path = within(audit / 'entrada/resoluciones_manual.csv', audit / 'entrada')
    if not path.exists():
        return None
    file_hash = sha256(path)
    origins = {(r['archivo_sha256'],r['archivo_relativo'],r['hoja'],r['fila']):r for r in records}
    seen, ids = set(), set()
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != HEADER:
            raise PipelineError('Contrato de resoluciones_manual.csv no reconocido')
        for row in reader:
            if None in row or not all(row.get(k) for k in HEADER if k != 'valor_nuevo'):
                raise PipelineError('Resolución incompleta')
            try:
                date.fromisoformat(row['fecha'])
                key = (row['archivo_sha256'],row['archivo_relativo'],row['hoja'],int(row['fila']))
            except ValueError as exc:
                raise PipelineError('Fecha/fila inválida de resolución') from exc
            if row['resolucion_id'] in ids or key in seen:
                raise PipelineError('Resoluciones múltiples/conflictivas para la misma ocurrencia')
            ids.add(row['resolucion_id']); seen.add(key)
            if key not in origins:
                raise PipelineError('Resolución no corresponde a archivo/hash/hoja/fila existente')
            r = origins[key]
            if row['aprobada'].lower() not in ('true','false') or row['accion'] not in ACTIONS or row['campo'] != ACTIONS[row['accion']]:
                raise PipelineError('Acción/campo/aprobación inválida en resolución')
            expected = r['tipo_original'] if row['campo'] == 'tipo' else r['coordenada_original']
            if row['valor_original'] != expected:
                raise PipelineError('Valor original no coincide con la resolución')
            if row['accion'] in ('CORREGIR_COORDENADA','CORREGIR_TIPO','ID_EQUIPO_ACREDITADO') and not row['valor_nuevo'].strip():
                raise PipelineError('Falta valor nuevo acreditado')
            r['resolucion_manual'] = dict(row)
    if sha256(path) != file_hash:
        raise PipelineError('Resoluciones cambiaron durante lectura')
    return dict(archivo='resoluciones_manual.csv', sha256=file_hash, resoluciones=len(ids))
