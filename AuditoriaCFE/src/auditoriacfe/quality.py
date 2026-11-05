"""Calidad por ocurrencia, independiente de conectividad y del maestro."""
from decimal import Decimal
from .coordinates import resolve, serialize
from .util import digest

TYPES = {"poste": "POSTE", "excedente": "EXCEDENTE", "cajadedmpalme": "CAJA_EMP",
         "caja_emp": "CAJA_EMP", "registro": "REGISTRO"}


def prepare(records, cfg):
    accredited = {(i["archivo"], i["hoja"], i["fila"]): i for i in cfg["ids_confiables"]}
    used = set()
    for r in records:
        r["ocurrencia_id"] = "O-" + digest([cfg["auditoria"], r["archivo_relativo"], r["archivo_sha256"], r["hoja"], r["fila"]])
        r.update(elemento_id=None, prevalente_id=None, latitud=None, longitud=None,
                 coordenada_normalizada=None, ruta_salida=r["ruta_original"],
                 tipo_canonico=TYPES.get(r["tipo_original"].strip().casefold()), incidencias=[])
        def issue(code, severity, reason):
            r["incidencias"].append(dict(codigo=code, severidad=severity, motivo=reason))
        key = (r["archivo_relativo"], r["hoja"], r["fila"])
        trusted = accredited.get(key)
        if trusted:
            used.add(key)
            r["id_confiable"] = trusted
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
        coords, events = resolve(r)
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
        elif not (Decimal(str(geo["lat_min"])) <= lat <= Decimal(str(geo["lat_max"])) and
                  Decimal(str(geo["lon_min"])) <= lon <= Decimal(str(geo["lon_max"]))):
            r["estado"] = "REVISAR"
            issue("FUERA_AMBITO", "ERROR", "Posición remota requiere corroboración; no se corrigen dígitos")
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
