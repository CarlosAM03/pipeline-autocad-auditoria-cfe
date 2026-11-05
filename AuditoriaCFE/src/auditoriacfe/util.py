"""Serialización exacta, identificadores y custodia de rutas."""
import hashlib
import json
from pathlib import Path


class PipelineError(ValueError):
    pass


def json_text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def digest(value):
    return hashlib.sha256(json_text(value).encode("utf-8")).hexdigest()


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def within(path, root):
    path, root = Path(path).resolve(), Path(root).resolve()
    if not path.is_relative_to(root):
        raise PipelineError(f"Ruta fuera del ámbito autorizado: {path}")
    return path


def output_path(path, audit):
    """No escribir a través de enlaces/junctions: podrían apuntar a entrada/."""
    path = Path(path)
    resolved = within(path, audit)
    if resolved != path.absolute():
        raise PipelineError(f"Destino de escritura con enlace o alias no permitido: {path}")
    return resolved


def decimal_key(value):
    # Decimal.normalize()/unary minus pueden redondear con el contexto global.
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if value == 0 else text
