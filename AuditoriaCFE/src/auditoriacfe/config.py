"""Configuración explícita; no descubre fuentes de otras auditorías."""
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation
from .util import PipelineError, within

PROJECT = Path(__file__).resolve().parents[2]
AUDITS = PROJECT / "auditorias"
DEFAULTS = dict(hojas_por_fuente={}, excepciones_cabecera={}, maestro_informativo=None,
                baseline_historica=None, geografia_permitida=None, ids_confiables=[],
                crs_candidato="EPSG:32611", crs_validado=False, evidencia_crs=None,
                cercanos_m=None, schema_02=1, cad=None, kmz=None, mapa_ids=None,
                diagnostico=False)


def audit_path(name):
    if not name or Path(name).name != name or name in (".", "..") or "/" in name or "\\" in name:
        raise PipelineError("Nombre de auditoría inválido")
    within(AUDITS, PROJECT)
    return within(AUDITS / name, AUDITS)


def load(audit):
    path = within(audit / "configuracion.json", audit)
    try:
        def no_constants(text):
            raise ValueError(f"Constante JSON no finita: {text}")
        raw = json.loads(path.read_text(encoding="utf-8"), parse_constant=no_constants)
    except (OSError, ValueError) as exc:
        raise PipelineError(f"Configuración ausente o JSON inválido: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise PipelineError("Configuración debe ser objeto JSON")
    allowed = set(DEFAULTS) | {"auditoria", "fuentes_en_orden"}
    if set(raw) - allowed:
        raise PipelineError(f"Claves de configuración no reconocidas: {sorted(set(raw) - allowed)}")
    cfg = {**DEFAULTS, **raw}
    if cfg.get("auditoria") != audit.name:
        raise PipelineError("auditoria debe coincidir con nombre de carpeta")
    sources = cfg.get("fuentes_en_orden")
    if not isinstance(sources, list) or not sources or not all(isinstance(s, str) for s in sources):
        raise PipelineError("P-01: fuentes_en_orden obligatoria y no vacía")
    if len(sources) != len(set(sources)):
        raise PipelineError("fuentes_en_orden contiene duplicados")
    for s in sources:
        if Path(s).is_absolute() or "\\" in s or ".." in Path(s).parts or not s.lower().endswith(".xlsx"):
            raise PipelineError(f"Fuente debe ser XLSX relativo con separador /: {s}")
        within(audit / "entrada" / s, audit / "entrada")
    for field in ("hojas_por_fuente", "excepciones_cabecera"):
        if not isinstance(cfg[field], dict) or set(cfg[field]) - set(sources):
            raise PipelineError(f"{field}: fuentes desconocidas")
    for sheets in cfg["hojas_por_fuente"].values():
        if not isinstance(sheets, list) or not all(isinstance(s, str) for s in sheets):
            raise PipelineError("hojas_por_fuente requiere listas de nombres exactos")
    for exceptions in cfg["excepciones_cabecera"].values():
        if not isinstance(exceptions, dict) or any(v != "F3_D_VACIA" for v in exceptions.values()):
            raise PipelineError("Única excepción de cabecera admitida: F3_D_VACIA")
    if type(cfg["crs_validado"]) is not bool:
        raise PipelineError("crs_validado debe ser booleano")
    geo = cfg["geografia_permitida"]
    if geo is not None and (not isinstance(geo,dict) or type(geo.get('aprobada')) is not bool):
        raise PipelineError('geografia_permitida requiere objeto y aprobada booleana')
    if type(cfg['schema_02']) is not int or cfg['schema_02'] not in (1,2) or type(cfg['diagnostico']) is not bool:
        raise PipelineError('schema_02 debe ser 1/2 y diagnostico booleano')
    if geo is not None and not geo.get('archivo'):
        try:
            bounds = [Decimal(str(geo[k])) for k in ("lat_min", "lat_max", "lon_min", "lon_max")]
            if not all(v.is_finite() for v in bounds) or not (-90 <= bounds[0] < bounds[1] <= 90 and -180 <= bounds[2] < bounds[3] <= 180):
                raise ValueError("límites fuera de rango")
            if type(geo.get("aprobada")) is not bool:
                raise ValueError("aprobada debe ser booleano")
            if geo["aprobada"] and not geo.get("evidencia"):
                raise ValueError("falta evidencia del perímetro")
        except (KeyError, TypeError, InvalidOperation, ValueError) as exc:
            raise PipelineError(f"geografia_permitida inválida: {exc}") from exc
    if cfg["cercanos_m"] is not None:
        try:
            threshold = Decimal(str(cfg["cercanos_m"]))
            if not threshold.is_finite() or threshold <= 0:
                raise ValueError()
        except (InvalidOperation, ValueError):
            raise PipelineError("cercanos_m requiere número positivo finito")
    if not isinstance(cfg["ids_confiables"], list):
        raise PipelineError("ids_confiables debe ser lista")
    seen = set()
    for item in cfg["ids_confiables"]:
        if not isinstance(item, dict) or not all(item.get(k) for k in ("archivo", "hoja", "fila", "id", "evidencia")):
            raise PipelineError("ID confiable requiere archivo, hoja, fila, id y evidencia")
        key = (item["archivo"], item["hoja"], item["fila"])
        if item["archivo"] not in sources or type(item["fila"]) is not int or item["fila"] < 1 or key in seen or not isinstance(item["id"], str):
            raise PipelineError("Identificador confiable ambiguo o fuera de fuentes")
        seen.add(key)
    return cfg


def inventory(audit, readonly_root=None):
    root = Path(readonly_root).resolve() if readonly_root is not None else within(audit / "entrada", audit)
    if not root.is_dir():
        raise PipelineError(f"No existe entrada/: {root}")
    files = []
    for path in root.rglob("*"):
        within(path, root)
        if path.is_file():
            if path.suffix.lower() in {".xls", ".xlsm", ".xlsb"}:
                raise PipelineError(f"Formato no admitido: {path.name}")
            if path.suffix.lower() == ".xlsx":
                if path.name.startswith("~$"):
                    raise PipelineError(f"Cerrar Excel y retirar archivo de bloqueo: {path.name}")
                files.append(path.relative_to(root).as_posix())
    return sorted(files)


def validate_inventory(cfg, files):
    if set(cfg["fuentes_en_orden"]) != set(files):
        raise PipelineError(f"P-01: precedencia debe cubrir TODOS los XLSX de entrada. Detectados={files}; declarados={cfg['fuentes_en_orden']}")


def reference_path(audit, spec, baseline=False):
    if not isinstance(spec, dict) or not isinstance(spec.get("archivo"), str) or not spec.get("fecha"):
        raise PipelineError("Referencia requiere archivo y fecha declarados")
    if baseline and spec.get("auditoria") != audit.name:
        raise PipelineError("Baseline debe declarar la misma auditoría")
    path = Path(spec["archivo"])
    path = (audit / path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_file() or path.suffix.lower() not in (".xlsx", ".csv"):
        raise PipelineError(f"Referencia CSV/XLSX no disponible: {path}")
    return path
