"""Referencias informativas declaradas, nunca filtros del plano individual."""
import csv
from .config import reference_path
from .coordinates import parse
from .quality import TYPES
from .schemas import extract
from .util import PipelineError, decimal_key, sha256


def compare_reference(audit, spec, baseline=False):
    if spec is None:
        return None, None
    path = reference_path(audit, spec, baseline)
    file_hash = sha256(path)
    keys, bad = set(), []
    if path.suffix.lower() == ".xlsx":
        data, profiles, auxiliary = extract(path, path.name, file_hash, spec.get("hojas"), spec.get("excepciones_cabecera"))
        rows = [(r["fila"], r["tipo_original"], r["coordenada_original"]) for r in data]
    else:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            data = list(csv.reader(stream))
        header = ["Ruta", "Elemento de Red", "Coordenadas"]
        if not data or data[0] != header:
            if not spec.get("sin_cabecera", False):
                raise PipelineError("Referencia CSV sin encabezado estricto: declarar sin_cabecera=true")
            start = 0
        else:
            start = 1
        rows = []
        for i, row in enumerate(data[start:], start + 1):
            if not any(row):
                continue
            if len(row) != 3:
                raise PipelineError(f"Referencia CSV: fila {i} no tiene tres campos")
            rows.append((i, row[1], row[2]))
    for number, typ, coord in rows:
        canonical = TYPES.get(typ.strip().casefold())
        if canonical == "REGISTRO":
            continue
        try:
            lat, lon = parse(coord)
            if not canonical:
                raise PipelineError("TIPO_DESCONOCIDO")
            keys.add((canonical, decimal_key(lat), decimal_key(lon)))
        except PipelineError as exc:
            bad.append(dict(fila=number, tipo=typ, coordenada=coord, motivo=str(exc)))
    if sha256(path) != file_hash:
        raise PipelineError("Referencia cambió durante lectura")
    return keys, dict(archivo=str(path), sha256=file_hash, fecha=spec["fecha"],
                      auditoria=spec.get("auditoria"), claves=len(keys),
                      casos_no_comparables=bad, comparacion_completa=not bad)
