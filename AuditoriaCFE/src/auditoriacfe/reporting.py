"""Productos deterministas, reconciliación y publicación recuperable."""
import csv
import json
import os
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

from .util import PipelineError, digest, json_text, sha256, within, output_path
from .dedup import identified_groups

MINIMUM = ["Ruta", "Elemento de Red", "Coordenadas"]
SUMMARY = "elemento_id,auditoria,tipo,ruta_prevalente,estado,coordenada,archivo_prevalente,hoja_prevalente,fila_prevalente,ocurrencias,coincide_maestro,novedad_vs_baseline,observaciones".split(",")
INCIDENTS = "incidencia_id,codigo,severidad,archivo,hoja,fila,valor_original,valor_elegido,motivo,estado_revision".split(",")
TOPOLOGY = "propuesta_id,origen_id,destino_id,ruta,tramo,distancia_plana_m,metodo,estado,justificacion".split(",")
PROJECTED = "elemento_id,ruta_id,tipo,latitud,longitud,este_m,norte_m,crs".split(",")
UNIFIED = "elemento_id,ruta_prevalente,tipo,coordenada_original,coordenada_interpretada,estado_preparacion,admision_geografica,apto_csv_01,archivo_prevalente,hoja_prevalente,fila_prevalente,ocurrencias".split(",")
REVISION = 'revision_id,elemento_id,ocurrencia_id,auditoria,archivo,hoja,fila,tipo_original,coordenada_original,codigo_incidencia,estado_actual,accion_requerida,fuente_evidencia,resolucion_id'.split(',')


def revision_file(stage, records, audit):
    rows = []
    for r in records:
        if r['estado'] in ('VALIDO','DUPLICADO'):
            continue
        for i,event in enumerate(r['incidencias']):
            resolution = r.get('resolucion_manual',{})
            rows.append(['R-'+digest([r['ocurrencia_id'],i]),r['elemento_id'],r['ocurrencia_id'],audit,
                         r['archivo_relativo'],r['hoja'],r['fila'],r['tipo_original'],r['coordenada_original'],
                         event['codigo'],r['estado'],'REVISAR_EVIDENCIA',resolution.get('evidencia',''),resolution.get('resolucion_id','')])
    csv_file(stage/'00_elementos_revision.csv', REVISION,rows)


def csv_file(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\r\n")
        writer.writerow(header)
        writer.writerows(rows)


def jsonl_file(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")


def counts(records, uniques, projection_rows=None):
    counter = Counter(r["estado"] for r in records)
    result = dict(ocurrencias=len(records), unicos_exportables=len(uniques), **{s: counter[s] for s in
                  ("VALIDO", "DUPLICADO", "FUERA_ALCANCE", "REVISAR", "RECHAZADO")})
    identified = identified_groups(records)
    result["unicos_identificados"] = len(identified)
    for typ in ("POSTE", "CAJA_EMP", "EXCEDENTE"):
        result[typ] = sum(r["tipo_canonico"] == typ for r in uniques)
    if result["ocurrencias"] != sum(counter.values()) or result["VALIDO"] != len(uniques) or sum(result[t] for t in ("POSTE", "CAJA_EMP", "EXCEDENTE")) != len(uniques):
        raise PipelineError("Conteos no reconciliados")
    prevalent = {r["ocurrencia_id"] for r in records if r["elemento_id"] and r["prevalente_id"] == r["ocurrencia_id"]}
    if len({r["ocurrencia_id"] for r in records}) != len(records):
        raise PipelineError("IDs de ocurrencia no únicos")
    if any(r["prevalente_id"] not in prevalent for r in records if r["estado"] == "DUPLICADO"):
        raise PipelineError("Duplicado sin prevalente")
    # Métricas aditivas: se conservan nombres, valores y orden de las anteriores.
    pending = sum(r["estado"] == "REVISAR" for r in identified)
    result.update(grupos_pendientes_revision=pending,
                  ocurrencias_revision_sin_identidad=counter["REVISAR"] - pending,
                  ocurrencias_con_identidad=sum(bool(r["elemento_id"]) for r in records),
                  filas_csv_00=len(identified), filas_csv_01=len(uniques),
                  csv_02_generado=int(projection_rows is not None),
                  filas_csv_02=len(projection_rows) if projection_rows is not None else 0)
    if (len(identified) != len(uniques) + pending or
            result["ocurrencias_con_identidad"] != len(identified) + counter["DUPLICADO"] or
            result["ocurrencias"] != len(identified) + counter["DUPLICADO"] + counter["RECHAZADO"] +
            counter["FUERA_ALCANCE"] + result["ocurrencias_revision_sin_identidad"]):
        raise PipelineError("Grupos identificados y ocurrencias no reconciliados")
    if projection_rows is not None and len(projection_rows) != len(uniques):
        raise PipelineError("Cardinalidad espacial inconsistente")
    return result


def geographic_admission(record):
    """Estado descriptivo; identificar no habilita la admisión para dibujo."""
    codes = {event["codigo"] for event in record["incidencias"]}
    if "GEOGRAFIA_PENDIENTE" in codes:
        return "PENDIENTE_P03"
    if "FUERA_AMBITO" in codes:
        return "REVISAR_FUERA_AMBITO"
    return "ADMITIDO_P03" if record["estado"] == "VALIDO" else "REVISAR"


def generate(stage, records, uniques, audit, maestro, baseline, refinfo, projection_rows, warnings, profiles, auxiliary, near):
    from .dedup import key
    csv_file(stage / "01_elementos_normalizados.csv", MINIMUM,
             ([r["ruta_salida"], r["tipo_canonico"], r["coordenada_normalizada"]] for r in uniques))
    occurrences = Counter(r["elemento_id"] for r in records if r["elemento_id"])
    admitted_ids = {r["elemento_id"] for r in uniques}
    csv_file(stage / "00_elementos_unificados.csv", UNIFIED,
             ([r["elemento_id"], r["ruta_salida"], r["tipo_canonico"], r["coordenada_original"],
               r["coordenada_normalizada"], "IDENTIFICADO", geographic_admission(r),
               "SI" if r["elemento_id"] in admitted_ids else "NO", r["archivo_relativo"],
               r["hoja"], r["fila"], occurrences[r["elemento_id"]]] for r in identified_groups(records)))
    summarized = uniques + [r for r in records if r["estado"] not in ("VALIDO", "DUPLICADO")]
    summary = []
    for r in summarized:
        admitted = r["estado"] == "VALIDO"
        comparable = bool(r["elemento_id"])
        k = key(r) if comparable else None
        master_match = "NO_DETERMINADO" if maestro is None or not comparable else ("SI" if k in maestro else "NO")
        novelty = "NO_DETERMINADO"
        if baseline is not None and comparable:
            novelty = "EXISTENTE" if k in baseline else ("NUEVO" if refinfo["baseline"]["comparacion_completa"] else "NO_DETERMINADO")
        notes = [i["codigo"] for i in r["incidencias"]]
        if comparable and maestro is not None and not refinfo["maestro"]["comparacion_completa"]:
            notes.append("MAESTRO_INCOMPLETO_NO_ES_AUSENCIA_ACREDITADA")
            if k not in maestro:
                master_match = "NO_DETERMINADO"
        summary.append([r["elemento_id"] or r["ocurrencia_id"], audit, r["tipo_canonico"], r["ruta_salida"],
                        r["estado"], r["coordenada_normalizada"], r["archivo_relativo"], r["hoja"], r["fila"],
                        occurrences[r["elemento_id"]] if r["elemento_id"] else 1, master_match, novelty, "|".join(notes)])
    csv_file(stage / "summary.csv", SUMMARY, summary)
    jsonl_file(stage / "linaje_y_calidad.jsonl", records)
    incidence_rows = []
    for r in records:
        for i, event in enumerate(r["incidencias"]):
            incidence_rows.append(["I-" + digest([r["ocurrencia_id"], i, event]), event["codigo"], event["severidad"],
                                   r["archivo_relativo"], r["hoja"], r["fila"], r["coordenada_original"],
                                   r["coordenada_normalizada"], event["motivo"],
                                   "INFORMATIVO" if event["severidad"] == "INFO" else "PENDIENTE_REVISION"])
    for i, warning in enumerate(warnings):
        incidence_rows.append(["L-" + digest([i, warning]), warning["codigo"], "ADVERTENCIA", "", "", "", "", "", warning["motivo"], "PENDIENTE_REVISION"])
    csv_file(stage / "reporte_incidencias.csv", INCIDENTS, incidence_rows)
    csv_file(stage / "asociaciones_elemento_ruta.csv", ["elemento_id", "auditoria", "ruta_original", "archivo", "hoja", "fila"],
             ([r["elemento_id"], audit, r["ruta_original"], r["archivo_relativo"], r["hoja"], r["fila"]] for r in records if r["elemento_id"]))
    csv_file(stage / "topologia_propuesta.csv", TOPOLOGY, [])
    csv_file(stage / "resumen_conteos.csv", ["metrica", "valor"], counts(records, uniques, projection_rows).items())
    jsonl_file(stage / "perfiles_hojas.jsonl", profiles)
    jsonl_file(stage / "filas_no_operativas.jsonl", auxiliary)
    csv_file(stage / "coordenadas_cercanas.csv", ["origen_id", "destino_id", "distancia_geodesica_m", "estado"], near)
    if projection_rows is not None:
        if len(projection_rows) != len(uniques):
            raise PipelineError("Cardinalidad espacial inconsistente")
        csv_file(stage / "02_elementos_proyectados.csv", PROJECTED, projection_rows)


@contextmanager
def audit_lock(audit):
    """Bloqueo liberado por el SO incluso si el proceso muere."""
    path = output_path(audit / ".proceso1.lock", audit)
    with path.open("a+b") as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise PipelineError("Otra corrida tiene bloqueada esta auditoría") from exc
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def recover(audit):
    previous = output_path(audit / "temporales" / "salida_anterior", audit)
    output = output_path(audit / "salida", audit)
    if previous.exists() and not output.exists():
        os.replace(previous, output)
    return output, previous


def publish(audit, stage, manifest):
    """El lector debe verificar hashes contra manifiesto; publicación por directorio.

    Ante kill entre renames, próxima corrida restaura salida_anterior. Ninguna
    carpeta salida contiene una mezcla de artefactos de dos corridas.
    """
    import shutil
    output, previous = recover(audit)
    if previous.exists():
        within(previous, audit / "temporales")
        shutil.rmtree(previous)
    manifest_dir = output_path(audit / "manifiestos", audit)
    manifest_dir.mkdir(exist_ok=True)
    manifest_path = output_path(manifest_dir / (manifest["ejecucion_id"] + ".json"), audit)
    tmp = output_path(manifest_dir / (manifest["ejecucion_id"] + ".tmp"), audit)
    tmp.write_text(json_text(manifest), encoding="utf-8")
    # Preparado antes de intercambiar directorios; hashes identifican versión.
    os.replace(tmp, manifest_path)
    had_output = output.exists()
    if had_output:
        os.replace(output, previous)
    try:
        os.replace(stage, output)
    except BaseException:
        if had_output:
            os.replace(previous, output)
        raise
    if previous.exists():
        within(previous, audit / "temporales")
        shutil.rmtree(previous)
    active = output_path(audit / "manifiesto_ejecucion.json", audit)
    active_tmp = output_path(audit / "temporales" / "manifiesto_actual.tmp", audit)
    active_tmp.write_text(json_text(manifest), encoding="utf-8")
    os.replace(active_tmp, active)
    return manifest_path


def verify(audit):
    """Consumidores deben verificar antes de usar un lote; rechaza mezcla o edición."""
    active = within(audit / "manifiesto_ejecucion.json", audit)
    manifest = json.loads(active.read_text(encoding="utf-8"))
    output = within(audit / "salida", audit)
    if {p.name for p in output.iterdir()} != set(manifest["artefactos"]):
        raise PipelineError("Conjunto de artefactos no coincide con manifiesto activo")
    for name, meta in manifest["artefactos"].items():
        path = within(output / name, output)
        if sha256(path) != meta["sha256"] or path.stat().st_size != meta["bytes"]:
            raise PipelineError(f"Hash/tamaño no coincide: {name}")
    return manifest
