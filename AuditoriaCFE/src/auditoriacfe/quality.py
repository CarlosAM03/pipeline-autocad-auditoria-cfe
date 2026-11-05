"""Calidad por ocurrencia, independiente de conectividad y del maestro."""
from decimal import Decimal
from .coordinates import resolve, serialize
from .util import digest
from .schemas import label

TYPES = {"poste": "POSTE", "excedente": "EXCEDENTE", "cajadedmpalme": "CAJA_EMP",
         "caja_emp": "CAJA_EMP", "registro": "REGISTRO"}


def canonical_type(text):
    token = label(text).replace(' ','').replace('_','').replace('-','')
    return {'poste':'POSTE','postes':'POSTE','excedente':'EXCEDENTE','excedentes':'EXCEDENTE',
            'cajaemp':'CAJA_EMP','cajadedmpalme':'CAJA_EMP','cajadeempalme':'CAJA_EMP',
            'cajadempalme':'CAJA_EMP','cajaempalme':'CAJA_EMP','registro':'REGISTRO'}.get(token)


def prepare(records, cfg):
    area = cfg.get('_geofence')
    accredited = {(i["archivo"], i["hoja"], i["fila"]): i for i in cfg["ids_confiables"]}
    used = set()
    for r in records:
        r["ocurrencia_id"] = "O-" + digest([cfg["auditoria"], r["archivo_relativo"], r["archivo_sha256"], r["hoja"], r["fila"]])
        r.update(elemento_id=None, prevalente_id=None, latitud=None, longitud=None,
                 coordenada_normalizada=None, ruta_salida=r["ruta_original"],
                 tipo_canonico=canonical_type(r["tipo_original"]), incidencias=[])
        def issue(code, severity, reason):
            r["incidencias"].append(dict(codigo=code, severidad=severity, motivo=reason))
        key = (r["archivo_relativo"], r["hoja"], r["fila"])
        trusted = accredited.get(key)
        if trusted:
            used.add(key)
            r["id_confiable"] = trusted
        resolution = r.get('resolucion_manual')
        action = resolution['accion'] if resolution and resolution['aprobada'].lower() == 'true' else None
        if action:
            issue('RESOLUCION_MANUAL','INFO',f"{resolution['resolucion_id']}: {resolution['motivo']}; evidencia={resolution['evidencia']}")
        if action == 'EXCLUIR':
            r['estado'] = 'RECHAZADO'
            issue('EXCLUSION_MANUAL','ERROR','Excluido de geometría por decisión acreditada; origen preservado')
            continue
        if action == 'CORREGIR_TIPO':
            r['tipo_canonico'] = canonical_type(resolution['valor_nuevo'])
        if action == 'ID_EQUIPO_ACREDITADO':
            if trusted and trusted['id']!=resolution['valor_nuevo']:
                from .util import PipelineError
                raise PipelineError('ID acreditado contradice resolución manual: resolver conflicto explícitamente')
            r['id_confiable'] = dict(id=resolution['valor_nuevo'],evidencia=resolution['evidencia'])
        if r["tipo_canonico"] == "REGISTRO":
            r["estado"] = "FUERA_ALCANCE"
            issue("REGISTRO_SUBTERRANEO", "INFO", "A09: no dibujar ni contar como CFE")
            continue
        r["estado"] = "VALIDO"
        if not r["tipo_canonico"]:
            r["estado"] = "REVISAR"
            issue("TIPO_DESCONOCIDO", "ERROR", "No pertenece al catálogo aprobado")
        if not r["ruta_original"].strip():
            r["estado"] = "REVISAR"
            issue("RUTA_VACIA", "ERROR", "No se completa por arrastre")
        selected = dict(r,coordenada_original=resolution['valor_nuevo']) if action == 'CORREGIR_COORDENADA' else r
        coords, events = resolve(selected)
        for event in events:
            issue(*event)
        if coords is None:
            r["estado"] = "RECHAZADO"
            continue
        lat, lon = coords
        r.update(latitud=format(lat, "f"), longitud=format(lon, "f"),
                 coordenada_normalizada=serialize(lat, lon))
        if lat < 0 or lon > 0:
            r["estado"] = "REVISAR"
            issue("HEMISFERIO_NO_NW", "ERROR", "Interpretable, fuera del formato geográfico admitido de estas fuentes")
        geo = cfg["geografia_permitida"]
        if not geo or not geo.get("aprobada"):
            r["estado"] = "REVISAR"
            issue("GEOGRAFIA_PENDIENTE", "ADVERTENCIA", "P-03: falta perímetro acreditado; no afirmar admisión local")
        elif geo.get('archivo'):
            from .geofence import contains
            if area is None or not contains(area,lat,lon):
                r['estado'] = 'REVISAR'
                issue('FUERA_AMBITO','ERROR','Fuera del polígono/corredor acreditado')
        elif not (Decimal(str(geo["lat_min"])) <= lat <= Decimal(str(geo["lat_max"])) and
                  Decimal(str(geo["lon_min"])) <= lon <= Decimal(str(geo["lon_max"]))):
            r["estado"] = "REVISAR"
            issue("FUERA_AMBITO", "ERROR", "Posición remota requiere corroboración; no se corrigen dígitos")
        if action == 'EXCEPCION_AMBITO' and r['estado'] == 'REVISAR' and r['tipo_canonico'] in ('POSTE','CAJA_EMP','EXCEDENTE') and r['ruta_original'].strip() and lat >= 0 and lon <= 0:
            r['incidencias'] = [i for i in r['incidencias'] if i['codigo'] not in ('GEOGRAFIA_PENDIENTE','FUERA_AMBITO')]
            r['estado'] = 'VALIDO'
            issue('EXCEPCION_AMBITO_ACREDITADA','INFO','Admisión individual acreditada, no aprobación global del perímetro')
        schema, cells = r["esquema"], r["celdas_originales"]
        for k in ("ruta", "tipo", "coord"):
            cell = cells.get(schema[k], {})
            if cell.get("es_formula"):
                issue("FORMULA_PRIMARIA", "ADVERTENCIA", "Caché leído sin recalcular; vigencia no acreditada")
                r["estado"] = "REVISAR"
    if set(accredited) != used:
        from .util import PipelineError
        raise PipelineError("ids_confiables referencia una ocurrencia no encontrada")
    return records
