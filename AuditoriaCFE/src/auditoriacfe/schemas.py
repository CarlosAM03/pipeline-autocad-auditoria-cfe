"""Adaptadores estructurales verificados en diagnóstico, sin nombres de archivo."""
import unicodedata
from .source_ooxml import value
from .util import PipelineError


def label(text):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", text.casefold())
                            if unicodedata.category(c) != "Mn").split())


def detect(cells, blank_d=False):
    h = {c: label(v["valor"]) for c, v in cells.items()}
    route = {"ruta", "nombre ruta"}
    element = {"elemento", "elemento de red"}
    coords = {"coordenadas", "coordenandas completas"}
    base = {}
    if h.get("A") == "nombre" and h.get("B") in element and h.get("C") in coords:
        base = dict(familia="F1_NOMBRE_ABC", ruta="A", tipo="B", coord="C",
                    aux_lat="D", aux_lon="E", oeste_positivo=True)
    elif h.get("A") in route and h.get("B") in element and h.get("C") in coords:
        base = dict(familia="F2_RUTA_ABC_FOTO_D", ruta="A", tipo="B", coord="C",
                    token_lat="E", token_lon="F", aux_lat="G", aux_lon="H")
    elif h.get("B") in route and h.get("C") in element:
        numbered = h.get("A") == "numero"
        if h.get("D") not in coords and not (numbered and not h.get("D") and blank_d):
            raise PipelineError("Cabecera D no reconocida; D vacía requiere excepciones_cabecera explícita")
        if not numbered and h.get("A"):
            raise PipelineError("Columna A desconocida para familia desplazada")
        base = dict(familia="F3_NUMERO_BCD" if numbered else "F4_DESPLAZADO_BCD",
                    ruta="B", tipo="C", coord="D", token_lat="F", token_lon="G",
                    aux_lat="H", aux_lon="I", numero="A" if numbered else None)
    if not base:
        raise PipelineError("Familia XLSX no reconocida por cabeceras")
    return base


def extract(path, relative, file_hash, sheets=None, exceptions=None):
    """Devuelve ocurrencias crudas, perfiles y filas auxiliares explicadas."""
    from .source_ooxml import Workbook
    records, profiles, auxiliary = [], [], []
    with Workbook(path) as book:
        names = [s[0] for s in book.sheets]
        if sheets is None:
            if len(names) > 1:
                raise PipelineError(f"{relative}: declarar orden de todas las hojas: {names}")
            sheets = names
        if sorted(sheets) != sorted(names) or len(sheets) != len(set(sheets)):
            raise PipelineError(f"{relative}: hojas_por_fuente debe enumerar todas las hojas una vez")
        for name in sheets:
            _, part, visibility = next(s for s in book.sheets if s[0] == name)
            profile = dict(archivo=relative, hoja=name, visibilidad=visibility,
                           medios_no_leidos=book.media_count, candidatos=0, familia="VACIA")
            schema = None
            for rownum, cells, hidden in book.rows(part, profile):
                if schema is None:
                    schema = detect(cells, (exceptions or {}).get(name) == "F3_D_VACIA")
                    profile.update(familia=schema["familia"], fila_cabecera=rownum)
                    continue
                operative = any(value(cells, schema[k]) or cells.get(schema[k], {}).get("es_formula")
                                for k in ("ruta", "tipo", "coord"))
                if not operative:
                    auxiliary.append(dict(archivo=relative, hoja=name, fila=rownum,
                                          motivo="SIN_CAMPOS_OPERATIVOS", celdas_originales=cells))
                    continue
                record = dict(archivo_relativo=relative, archivo_sha256=file_hash, hoja=name,
                              fila=rownum, oculta=hidden, familia=schema["familia"],
                              celdas_originales=cells, esquema=schema)
                for dest, src in (("ruta_original", "ruta"), ("tipo_original", "tipo"),
                                  ("coordenada_original", "coord"), ("numero_original", "numero")):
                    record[dest] = value(cells, schema.get(src))
                records.append(record)
                profile["candidatos"] += 1
            profiles.append(profile)
    return records, profiles, auxiliary
