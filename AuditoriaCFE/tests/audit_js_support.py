"""Reproducción readonly de funciones JS copiadas, sin generar instrucciones CAD."""
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from support import PROJECT
from auditoriacfe.util import sha256

HISTORY = PROJECT.parent / "Auditorias-20261104T035633Z-1-001"
JS_ROOT = HISTORY / "ScriptsHistoricos"
FILES = [JS_ROOT / n for n in ("generar.js", "ordenar.js", "trayectoria.js", "STD-MIRADOR.csv", "STD-OTAY-FLORIDO.csv")]
FILES += [HISTORY / "Auditorias" / n for n in ("STD-MIRADOR.txt", "STD-OTAY-FLORIDO.txt")]


def inspect_js():
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Auditoría JS requiere Node.js; reproducción NO ejecutada")
    before = {str(p.relative_to(HISTORY)): sha256(p) for p in FILES}
    runtime = PROJECT / "tests/_runtime"
    runtime.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="js_copias_", dir=runtime) as temp:
        copy_dir = Path(temp)
        for original in FILES[:5]:
            target = copy_dir / original.name
            shutil.copyfile(original, target)
            if sha256(target) != sha256(original):
                raise AssertionError("Copia de auditoría no idéntica")
        (copy_dir / "quoted.csv").write_text('Ruta,Elemento de Red,Coordenadas\n"Ruta, con coma",poste,32.5N 117W\n', encoding="utf-8")
        process = subprocess.run([node, str(PROJECT / "tests/js_audit_harness.cjs"), str(copy_dir)],
                                 capture_output=True, text=True, encoding="utf-8", check=True, timeout=60)
        data = json.loads(process.stdout)
    # Se contrasta el TXT; no se ejecuta como SCRIPT ni se interpreta en AutoCAD.
    data["txt"] = {}
    for name in ("STD-MIRADOR", "STD-OTAY-FLORIDO"):
        lines = (HISTORY / "Auditorias" / (name + ".txt")).read_text(encoding="utf-8-sig").splitlines()
        points = [tuple(map(float, lines[i + 1].split(","))) for i, line in enumerate(lines) if line == "POINT"]
        predicted = data["libraries"]["generar"][name + ".csv"]["points"]
        deviations = [math.hypot(p["x"] - q[0], p["y"] - q[1]) for p, q in zip(predicted, points)]
        data["txt"][name] = dict(points=len(points), text=sum(line == "TEXT" for line in lines),
                                 pline=sum(line == "PLINE" for line in lines),
                                 pdmode=[lines[i + 1] for i, line in enumerate(lines) if line == "PDMODE"],
                                 same_cardinality=len(points) == len(predicted),
                                 max_sequence_error_m=max(deviations, default=0))
    after = {str(p.relative_to(HISTORY)): sha256(p) for p in FILES}
    if before != after:
        raise AssertionError("Histórico alterado durante auditoría")
    data["sha256"] = before
    return data


def compact(data):
    """Evidencia legible, sin miles de coordenadas ni datos replicados."""
    return dict(node=data["node"], sha256=data["sha256"],
                libraries={name: {case: {k: v for k, v in value.items() if k not in ("points", "components", "route_lengths")} if isinstance(value, dict) else value
                                  for case, value in cases.items()} for name, cases in data["libraries"].items()},
                txt={name: {**{k: v for k, v in info.items() if k != "pdmode"},
                            "pdmode_values": sorted(set(info["pdmode"]))} for name, info in data["txt"].items()})


if __name__ == "__main__":
    print(json.dumps(compact(inspect_js()), ensure_ascii=False, indent=2))
