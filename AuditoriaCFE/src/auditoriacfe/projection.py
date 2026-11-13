"""Proyección estándar condicionada a aprobación y controles CAD documentados."""
import math
from .util import PipelineError, sha256


def prepare_projection(cfg, audit):
    evidence = cfg.get("evidencia_crs")
    if not cfg["crs_validado"] or not evidence:
        return None, dict(estado="CRS_PENDIENTE", motivo="P-06: falta aprobación y evidencia de controles CAD")
    # Declarar true no basta: evidencia archivada, responsable, fecha, unidades,
    # CRS exacto y dos controles distintos, con tolerancia aportada por owner.
    try:
        if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ("archivo", "aprobado_por", "fecha", "crs", "controles", "tolerancia_m")):
            raise PipelineError("Evidencia CRS incompleta")
        from pathlib import Path
        doc = Path(evidence["archivo"])
        doc = (audit / doc).resolve() if not doc.is_absolute() else doc.resolve()
        if not doc.is_file() or evidence.get("unidades") != "m" or evidence["crs"] != cfg["crs_candidato"]:
            raise PipelineError("Evidencia CRS/metro no concordante o archivo ausente")
        controls = evidence["controles"]
        if len(controls) < 2 or len({(float(c["latitud"]), float(c["longitud"])) for c in controls}) < 2 or len({(float(c["este_m"]), float(c["norte_m"])) for c in controls}) < 2:
            raise PipelineError("Se requieren dos controles no coincidentes")
        tolerance = float(evidence["tolerancia_m"])
        if not math.isfinite(tolerance) or tolerance <= 0:
            raise PipelineError("Tolerancia debe ser positiva y acreditada")
        from pyproj import CRS, Transformer, __version__, proj_version_str
        crs = CRS.from_user_input(evidence["crs"])
        if not crs.is_projected or any(a.unit_conversion_factor != 1 for a in crs.axis_info[:2]):
            raise PipelineError("CRS debe ser proyectado con ejes métricos")
        transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
        residuals = []
        for c in controls:
            lat, lon, east, north = [float(c[k]) for k in ("latitud", "longitud", "este_m", "norte_m")]
            if not all(math.isfinite(v) for v in (lat, lon, east, north)) or not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise PipelineError("Control no finito o fuera de rango mundial")
            x, y = transformer.transform(lon, lat, errcheck=True)
            residual = math.hypot(x - east, y - north)
            if not math.isfinite(residual) or residual > tolerance:
                raise PipelineError(f"Control {c.get('id', '?')} fuera de tolerancia: {residual} m")
            residuals.append(residual)
        return transformer, dict(estado="CONTROLES_VERIFICADOS", crs=crs.to_string(),
                                 evidencia_sha256=sha256(doc), residuales_m=residuals,
                                 pyproj=__version__, PROJ=proj_version_str)
    except Exception as exc:
        # La falla espacial no bloquea la extracción ni genera un CSV supuesto.
        return None, dict(estado="CRS_PENDIENTE", motivo=str(exc))


def route_id(audit, name):
    from .util import digest
    return 'R-' + digest(['ruta-v1',audit,name])


def project(records, transformer, crs, schema=1, audit=''):
    rows = []
    for r in records:
        x, y = transformer.transform(float(r["longitud"]), float(r["latitud"]), errcheck=True)
        if not math.isfinite(x) or not math.isfinite(y):
            raise PipelineError("Proyección no finita; no publicar CSV parcial")
        head = [r['elemento_id'],r['ruta_salida']] if schema == 1 else [r['elemento_id'],route_id(audit,r['ruta_salida']),r['ruta_salida']]
        rows.append(head + [r["tipo_canonico"], r["latitud"],r["longitud"], repr(x), repr(y), crs])
    return rows


def read_projected(path, audit):
    import csv
    from .reporting import PROJECTED, PROJECTED_V2
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames not in (PROJECTED,PROJECTED_V2):
            raise PipelineError('Esquema CSV02 desconocido')
        version=2 if reader.fieldnames == PROJECTED_V2 else 1
        rows=list(reader)
    seen=set(); crs=set()
    for row in rows:
        if None in row or any(v is None for v in row.values()) or row['elemento_id'] in seen or not row['elemento_id']:
            raise PipelineError('IDs/campos CSV02 inválidos')
        seen.add(row['elemento_id']);crs.add(row['crs'])
        if row['tipo'] not in ('POSTE','CAJA_EMP','EXCEDENTE'):
            raise PipelineError('Tipo CSV02 inválido')
        try:
            values=[float(row[k]) for k in ('latitud','longitud','este_m','norte_m')]
            if not all(math.isfinite(v) for v in values) or not (-90<=values[0]<=90 and -180<=values[1]<=180):
                raise ValueError()
        except ValueError as exc:
            raise PipelineError('Valores CSV02 inválidos') from exc
        if version == 1:
            row['ruta_nombre']=row['ruta_id'];row['ruta_id']=route_id(audit,row['ruta_nombre'])
        elif row['ruta_id'] != route_id(audit,row['ruta_nombre']):
            raise PipelineError('ruta_id no corresponde a ruta_nombre/auditoría')
    if len(crs)>1:
        raise PipelineError('CSV02 mezcla CRS')
    return rows,version
