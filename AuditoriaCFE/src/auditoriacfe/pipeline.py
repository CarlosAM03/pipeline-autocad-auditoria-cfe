"""Orquestación de Proceso 1. Nunca ejecuta CAD ni modifica las entradas."""
import platform
import shutil
import tempfile
from pathlib import Path

from . import __version__
from . import config
from .comparison import compare_reference
from .dedup import consolidate
from .projection import prepare_projection, project
from .quality import prepare
from .reporting import audit_lock, counts, generate, publish, recover
from .schemas import extract
from .topology import nearby
from .util import PipelineError, digest, json_text, sha256, within, output_path


def run(audit, dry_run=False, readonly_root=None, emit=print):
    within(config.AUDITS, config.PROJECT)
    audit = within(audit, config.AUDITS)
    if not audit.is_dir():
        raise PipelineError(f"No existe auditoría: {audit}")
    if dry_run:
        cfg, root = preflight(audit, readonly_root, emit)
        # Sin abrir celdas ni escribir bloqueos/manifiestos.
        return dict(estado="DRY_RUN", fuentes=cfg["fuentes_en_orden"], configuracion=cfg,
                    entrada_prueba=str(root) if readonly_root else None)
    with audit_lock(audit):
        recover(audit)
        try:
            cfg, root = preflight(audit, readonly_root, emit)
            return execute(audit, root, cfg, readonly_root is not None, emit)
        except (Exception, KeyboardInterrupt) as exc:
            directory = output_path(audit / "manifiestos", audit)
            directory.mkdir(exist_ok=True)
            config_file = within(audit / "configuracion.json", audit)
            failure = dict(auditoria=audit.name, estado="FALLIDO", error=str(exc),
                           config_archivo_sha256=sha256(config_file) if config_file.is_file() else None,
                           entrada=str(readonly_root or audit / "entrada"), version_pipeline=__version__)
            output_path(directory / ("fallo_" + digest(failure) + ".json"), audit).write_text(json_text(failure), encoding="utf-8")
            raise


def preflight(audit, readonly_root, emit):
    files = config.inventory(audit, readonly_root)
    emit(f"Auditoría: {audit.name}; XLSX detectados: {len(files)}")
    for name in files:
        emit(f"  {name}")
    cfg = config.load(audit)
    config.validate_inventory(cfg, files)
    root = Path(readonly_root).resolve() if readonly_root is not None else (audit / "entrada").resolve()
    emit("Precedencia: " + " -> ".join(cfg["fuentes_en_orden"]))
    emit("P-02/P-03/P-04/P-05/P-06/P-09: ver configuración, controles y revisión humana.")
    return cfg, root


def execute(audit, root, cfg, testing, emit):
    records, profiles, auxiliary, sources = [], [], [], []
    for order, name in enumerate(cfg["fuentes_en_orden"]):
        path = within(root / name, root)
        file_hash = sha256(path)
        raw, prof, aux = extract(path, name, file_hash, cfg["hojas_por_fuente"].get(name),
                                 cfg["excepciones_cabecera"].get(name))
        for r in raw:
            r["orden_fuente"] = order
        records.extend(raw)
        profiles.extend(prof)
        auxiliary.extend(aux)
        sources.append(dict(archivo=name, sha256=file_hash, bytes=path.stat().st_size))
    prepare(records, cfg)
    uniques = consolidate(records, audit.name)
    master, master_info = compare_reference(audit, cfg["maestro_informativo"])
    baseline, baseline_info = compare_reference(audit, cfg["baseline_historica"], baseline=True)
    refinfo = dict(maestro=master_info, baseline=baseline_info)
    transformer, crs_info = prepare_projection(cfg, audit)
    warnings = [dict(codigo="LIBERACION_PENDIENTE", motivo="P-04/P-09: salida PRELIMINAR; contrato auxiliar PROPUESTA"),
                dict(codigo="TOPOLOGIA_NO_CONFIRMADA", motivo="P-05: archivo de propuestas vacío; no hay evidencia suficiente para proponer conexiones")]
    if testing:
        warnings.append(dict(codigo="ENTRADA_PRUEBA_SOLO_LECTURA", motivo=f"Fuente explícita de prueba: {root}; corrida NO PRODUCTIVA"))
    if master is None:
        warnings.append(dict(codigo="MAESTRO_NO_DECLARADO", motivo="Comparación informativa NO_DETERMINADO"))
    if baseline is None:
        warnings.append(dict(codigo="BASELINE_NO_DECLARADA", motivo="P-02: novedad NO_DETERMINADO"))
    if crs_info["estado"] == "CRS_PENDIENTE":
        warnings.append(dict(codigo="CRS_PENDIENTE", motivo=crs_info["motivo"]))
    projected = None
    if transformer:
        try:
            projected = project(uniques, transformer, cfg["crs_candidato"])
        except Exception as exc:
            crs_info = dict(estado="CRS_PENDIENTE", motivo=f"Error de transformación: {exc}")
            warnings.append(dict(codigo="CRS_PENDIENTE", motivo=crs_info["motivo"]))
    near = []
    if cfg["cercanos_m"] is not None:
        try:
            near = nearby(uniques, cfg["cercanos_m"])
            for a, b, distance, _ in near:
                warnings.append(dict(codigo="COORDENADAS_CERCANAS", motivo=f"{a} | {b}: {distance} m; no se fusionan ni conectan"))
        except ImportError:
            warnings.append(dict(codigo="CERCANIA_NO_EVALUADA", motivo="Falta pyproj para diagnóstico geodésico optativo"))
    else:
        warnings.append(dict(codigo="CERCANIA_NO_EVALUADA", motivo="Sin umbral cercanos_m declarado; no se inventa un umbral de negocio"))
    for role, info in refinfo.items():
        if info and not info["comparacion_completa"]:
            warnings.append(dict(codigo="REFERENCIA_INCOMPLETA", motivo=f"{role}: {len(info['casos_no_comparables'])} casos no comparables; no afirmar novedad por ausencia"))
    for source in sources:
        if sha256(root / source["archivo"]) != source["sha256"]:
            raise PipelineError("Entrada cambió durante la corrida; no publicar")
    temporary = output_path(audit / "temporales", audit)
    temporary.mkdir(exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="proceso1_", dir=temporary))
    try:
        generate(stage, records, uniques, audit.name, master, baseline, refinfo,
                 projected, warnings, profiles, auxiliary, near)
        code = {p.name: sha256(p) for p in sorted(Path(__file__).parent.glob("*.py"))}
        code["preparar_auditoria.py"] = sha256(config.PROJECT / "preparar_auditoria.py")
        manifest = dict(auditoria=audit.name, estado="PRELIMINAR", modo="PRUEBA" if testing else "OPERATIVO",
                        version_pipeline=__version__, version_identidad="identidad-v1", codigo_hash=digest(code),
                        modulos_sha256=code, python=platform.python_version(),
                        fuentes_ordenadas=sources, entrada=str(root), config_hash=digest(cfg), configuracion=cfg,
                        crs=crs_info, crs_validado=projected is not None, baseline=baseline_info,
                        maestro_ref=master_info, conteos=counts(records, uniques), advertencias=warnings,
                        topologia="NO_CONFIRMADA", aprobacion_humana="PENDIENTE", perfiles_hojas=profiles,
                        artefactos={p.name: dict(sha256=sha256(p), bytes=p.stat().st_size) for p in sorted(stage.iterdir())})
        try:
            import pyproj
            manifest["dependencias"] = dict(pyproj=pyproj.__version__, PROJ=pyproj.proj_version_str)
        except ImportError:
            manifest["dependencias"] = dict(pyproj=None)
        manifest["ejecucion_id"] = digest(manifest)
        manifest["criterio_publicacion"] = "Artefactos de salida válidos para esta corrida solo si TODOS sus hashes coinciden con este manifiesto"
        path = publish(audit, stage, manifest)
        emit(f"PRELIMINAR: {len(records)} ocurrencias; {len(uniques)} únicos exportables. {crs_info['estado']}")
        emit(f"Manifiesto: {path}")
        return manifest
    finally:
        if stage.exists():
            within(stage, temporary)
            shutil.rmtree(stage)
