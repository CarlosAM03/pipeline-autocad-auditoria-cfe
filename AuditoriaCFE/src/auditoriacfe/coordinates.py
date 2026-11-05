"""Grados decimales exactos; no repara dígitos, coma decimal ni signos ambiguos."""
import re
from decimal import Decimal
from .util import PipelineError

NUMBER = r"(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)"
PAIR = re.compile(rf"\s*({NUMBER})\s*°?\s*([NS])\s*({NUMBER})\s*°?\s*([EW])\s*", re.I)


def parse(text):
    match = PAIR.fullmatch(text)
    if not match:
        raise PipelineError("COORD_NO_INTERPRETABLE")
    lat, lon = Decimal(match[1]), Decimal(match[3])
    if lat > 90 or lon > 180:
        raise PipelineError("COORD_FUERA_RANGO")
    return (lat.copy_negate() if match[2].upper() == "S" else lat,
            lon.copy_negate() if match[4].upper() == "W" else lon)


def serialize(lat, lon):
    return f"{format(lat.copy_abs(), 'f')}{'S' if lat < 0 else 'N'} {format(lon.copy_abs(), 'f')}{'W' if lon <= 0 else 'E'}"


def numeric_aux(lat_text, lon_text, west_positive=False):
    pattern = rf"[+-]?{NUMBER}"
    if not re.fullmatch(pattern, lat_text.strip()) or not re.fullmatch(pattern, lon_text.strip()):
        raise PipelineError("AUX_NO_INTERPRETABLE")
    lat, lon = Decimal(lat_text.strip()), Decimal(lon_text.strip())
    if west_positive:
        if lon < 0:
            raise PipelineError("AUX_SIGNO_AMBIGUO")
        lon = lon.copy_negate()
    if lat.copy_abs() > 90 or lon.copy_abs() > 180:
        raise PipelineError("AUX_FUERA_RANGO")
    return lat, lon


def resolve(record):
    """Retorna coordenada y eventos. Auxiliares no sustituyen texto válido.

    Recuperación: pares interpretables coinciden exactamente; ningún error de
    magnitud ni fórmula sin evidencia de actualización; los tokens primarios
    válidos no pueden contradecir el reemplazo. Conservador por A08.
    """
    from .source_ooxml import value
    cells, schema = record["celdas_originales"], record["esquema"]
    text = record["coordenada_original"]
    events, pairs, broken, formulas = [], [], False, False
    try:
        primary = parse(text)
        primary_error = None
    except PipelineError as exc:
        primary, primary_error = None, str(exc)
    for kind, cols in (("TOKENS", ("token_lat", "token_lon")), ("NUMERICOS", ("aux_lat", "aux_lon"))):
        a, b = (schema.get(k) for k in cols)
        va, vb = value(cells, a), value(cells, b)
        if not va and not vb:
            continue
        formulas |= any(cells.get(c, {}).get("es_formula", False) for c in (a, b))
        try:
            pair = parse(va + " " + vb) if kind == "TOKENS" else numeric_aux(va, vb, schema.get("oeste_positivo", False))
            pairs.append(pair)
            if primary and pair != primary:
                events.append(("AUX_DISCREPANCIA", "ADVERTENCIA", f"{kind}: {va} | {vb}; prevalece texto completo"))
        except PipelineError as exc:
            broken = True
            events.append((str(exc), "ADVERTENCIA", f"{kind}: {va} | {vb}; sin reparación"))
    if primary:
        if serialize(*primary) != text:
            events.append(("FORMATO_NORMALIZADO", "INFO", "Separadores/hemisferios inequívocos normalizados"))
        return primary, events
    # Un entero imposible no autoriza sustituir dígitos con auxiliares.
    if primary_error == "COORD_FUERA_RANGO":
        return None, events + [(primary_error, "ERROR", "Coordenada mundialmente imposible; no corregir dígitos")]
    consistent = bool(pairs) and all(p == pairs[0] for p in pairs) and not broken and not formulas
    if consistent:
        proposed = pairs[0]
        # Comparar los componentes primarios que sí se pueden interpretar.
        for index, hemisphere in ((0, "NS"), (1, "EW")):
            tokens = re.findall(rf"({NUMBER})\s*°?\s*([{hemisphere}])", text, re.I)
            if len(tokens) > 1:
                consistent = False
            for num, hem in tokens:
                val = Decimal(num)
                if hem.upper() in "SW":
                    val = val.copy_negate()
                consistent &= val == proposed[index]
        if consistent:
            return proposed, events + [("RECUPERADO_AUXILIAR", "ADVERTENCIA", "Pares auxiliares inequívocos y consistentes; sin fórmulas")]
    return None, events + [(primary_error, "ERROR", "Sin reemplazo auxiliar inequívoco acreditado")]
