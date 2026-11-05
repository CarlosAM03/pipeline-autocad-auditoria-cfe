"""Integración readonly declarada, reproducibilidad y comparación de artefactos.

Actualiza solamente las tres auditorías de PRUEBA ya existentes. No genera
XLSX, CAD ni configuraciones, y nunca escribe dentro del histórico.
"""
import argparse
import csv
import json
from pathlib import Path

from support import AUDITS, PROJECT
from auditoriacfe.pipeline import run
from auditoriacfe.reporting import UNIFIED, verify
from auditoriacfe.util import sha256


def validate(audit, manifest):
    output = audit / "salida"
    with (output / "00_elementos_unificados.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == UNIFIED
        rows = list(reader)
    with (output / "01_elementos_normalizados.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["Ruta", "Elemento de Red", "Coordenadas"]
        normalized = list(reader)
    records = [json.loads(l) for l in (output / "linaje_y_calidad.jsonl").read_text(encoding="utf-8").splitlines()]
    groups = {r["elemento_id"]:r for r in records if r["elemento_id"] and r["prevalente_id"] == r["ocurrencia_id"]}
    counts = manifest["conteos"]
    assert len(rows) == len(groups) == counts["filas_csv_00"] == counts["unicos_identificados"]
    assert {r["elemento_id"] for r in rows} == set(groups)
    assert len(normalized) == counts["filas_csv_01"] == counts["unicos_exportables"]
    assert sum(int(r["ocurrencias"]) for r in rows) == counts["ocurrencias_con_identidad"]
    assert all(r["estado_preparacion"] == "IDENTIFICADO" for r in rows)
    assert all(r["apto_csv_01"] == ("SI" if groups[r["elemento_id"]]["estado"] == "VALIDO" else "NO") for r in rows)
    projected_path = output / "02_elementos_proyectados.csv"
    assert projected_path.exists() == bool(counts["csv_02_generado"])
    if projected_path.exists():
        with projected_path.open(encoding="utf-8", newline="") as f:
            projected = list(csv.DictReader(f))
        assert len(projected) == len(normalized) == counts["filas_csv_02"]
        assert {r["elemento_id"] for r in projected} == {r["elemento_id"] for r in rows if r["apto_csv_01"] == "SI"}
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparar-anterior", action="store_true", help="Usar snapshot local previo a la extensión si existe")
    args = parser.parse_args()
    runtime = PROJECT / "tests/_runtime"
    before_path = runtime / "extension_antes.json"
    old = json.loads(before_path.read_text(encoding="utf-8")) if args.comparar_anterior else None
    base = PROJECT.parent / "Auditorias-20261104T035633Z-1-001/postes/CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR"
    sources = {"Prueba-Historica-Mirador":base / "Mirador", "Prueba-Historica-Otay":base / "Otay - Florido",
               "Demo-Sintetica":AUDITS / "Demo-Sintetica/entrada"}
    results = {}
    for name, root in sources.items():
        audit = AUDITS / name
        # Evitar reemplazar silenciosamente un lote modificado por el operador.
        verify(audit)
        first = run(audit, readonly_root=root, emit=lambda *args: None)
        snapshot = {p.name:p.read_bytes() for p in (audit / "salida").iterdir()}
        second = run(audit, readonly_root=root, emit=lambda *args: None)
        assert first == second == verify(audit)
        assert snapshot == {p.name:p.read_bytes() for p in (audit / "salida").iterdir()}
        counts = validate(audit, first)
        if old:
            for filename, meta in old[name]["artefactos"].items():
                if filename != "resumen_conteos.csv":
                    assert first["artefactos"][filename] == meta, (name, filename)
            for metric, value in old[name]["conteos"].items():
                assert counts[metric] == value, (name, metric)
        results[name] = dict(ejecucion_id=first["ejecucion_id"], conteos=counts,
                             artefactos_previos_identicos=bool(old), reproducible=True)
        print(name, json.dumps(results[name], ensure_ascii=False))
    if old:
        for filename, expected in old["custodia"].items():
            assert sha256(PROJECT.parent / filename) == expected, filename
        assert sha256(PROJECT.parent / "README.md") == old["readme_usuario_sha256"]
    runtime.mkdir(exist_ok=True)
    (runtime / "extension_validacion.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Integridad, reproducibilidad, cardinalidades y custodia OK")


if __name__ == "__main__":
    main()
