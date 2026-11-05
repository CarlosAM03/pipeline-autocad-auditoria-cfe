import argparse
import sys
import zipfile
from xml.etree.ElementTree import ParseError
from . import config
from .pipeline import run
from .util import PipelineError, json_text


def main(argv=None):
    parser = argparse.ArgumentParser(description="Proceso 1 CFE/DATRA: XLSX → CSV y reportes, sin CAD")
    parser.add_argument("--auditoria", help="Nombre exacto bajo AuditoriaCFE/auditorias/")
    parser.add_argument("--dry-run", action="store_true", help="Inventario/configuración, sin escribir")
    parser.add_argument("--entrada-prueba", help="Raíz XLSX explícita solo lectura; corrida de PRUEBA, no productiva")
    parser.add_argument("--verificar-salida", action="store_true", help="Verificar hashes de salida contra manifiesto activo")
    args = parser.parse_args(argv)
    try:
        name = args.auditoria
        if not name:
            choices = sorted(p.name for p in config.AUDITS.iterdir() if p.is_dir() and (p / "entrada").is_dir()) if config.AUDITS.exists() else []
            if not choices:
                raise PipelineError("No hay auditorías con entrada/. Crear carpeta y configuracion.json según README.")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            selected = input("Seleccione número de auditoría: ").strip()
            if not selected.isdigit() or not 1 <= int(selected) <= len(choices):
                raise PipelineError("Selección inválida")
            name = choices[int(selected) - 1]
        audit = config.audit_path(name)
        if args.verificar_salida:
            from .reporting import verify
            manifest = verify(audit)
            print(f"Integridad OK: {manifest['ejecucion_id']}; estado={manifest['estado']}; no equivale a aprobación geográfica/CAD")
            return 0
        result = run(audit, args.dry_run, args.entrada_prueba)
        if args.dry_run:
            print(json_text(result))
        return 0
    except (PipelineError, OSError, ValueError, KeyError, EOFError, zipfile.BadZipFile, ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrumpido; verificar hashes del manifiesto antes de consumir salida.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
