import argparse
import sys
import zipfile
from xml.etree.ElementTree import ParseError
from . import config
from .pipeline import run
from .util import PipelineError, json_text


def main(argv=None):
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(errors='backslashreplace')
    parser = argparse.ArgumentParser(description="Pipeline CFE/DATRA: XLSX -> CSV, evidencia y dos SCR (no ejecuta AutoCAD)")
    parser.add_argument("--auditoria", help="Nombre exacto bajo AuditoriaCFE/auditorias/")
    parser.add_argument("--dry-run", action="store_true", help="Inventario/configuración, sin escribir")
    parser.add_argument("--entrada-prueba", help="Raíz XLSX explícita solo lectura; corrida de PRUEBA, no productiva")
    parser.add_argument("--verificar-salida", action="store_true", help="Verificar hashes de salida contra manifiesto activo")
    parser.add_argument('--verificar-paquete',action='store_true',help='Integridad de entradas, configuración, salidas y SCR antes de CAD')
    parser.add_argument('--verificar-evidencia-cad',action='store_true',help='Verifica por separado hashes del acta nativa/DWG/PDF mutable; no aprueba CRS ni FINAL')
    parser.add_argument('--batch',action='store_true',help='Natura, Mirador, Otay-Florido y Tijuana-General en lotes independientes')
    parser.add_argument('--preparar-entradas',action='store_true',help='Copiar fuentes exactas autorizadas; no sobreescribir copias modificadas')
    parser.add_argument('--diagnostico',action='store_true',default=None,help='Opt-in CRS candidato, copia DWG, solo puntos NO VERIFICADOS; contrato v2')
    args = parser.parse_args(argv)
    try:
        if args.verificar_evidencia_cad and (args.batch or args.preparar_entradas):
            raise PipelineError('Evidencia CAD requiere auditoría individual sin preparación')
        if args.batch and (args.auditoria or args.entrada_prueba):
            raise PipelineError('--batch no se combina con --auditoria/--entrada-prueba')
        if args.batch:
            if args.preparar_entradas:
                if args.dry_run:raise PipelineError('--preparar-entradas escribe copias; no combinar con --dry-run')
                from .intake import bootstrap,prepare_master,SOURCES
                print(json_text(bootstrap(list(SOURCES))))
                print(json_text(prepare_master(list(SOURCES))))
            from .batch import batch
            result=batch(dry_run=args.dry_run,diagnostico=args.diagnostico,
                         verify_only=args.verificar_salida or args.verificar_paquete)
            print(json_text(result))
            return 2 if result['estado']=='FALLIDO' else 0
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
        if args.verificar_evidencia_cad:
            if args.batch or args.preparar_entradas:raise PipelineError('Evidencia CAD requiere auditoría individual sin preparación')
            from .native_evidence import verify_native
            print(json_text(verify_native(audit)))
            return 0
        if args.preparar_entradas:
            if args.dry_run:raise PipelineError('--preparar-entradas escribe copias; no combinar con --dry-run')
            from .intake import bootstrap,prepare_master
            print(json_text(bootstrap([name])))
            print(json_text(prepare_master([name])))
        if args.verificar_salida or args.verificar_paquete:
            from .reporting import verify
            manifest = verify(audit)
            print(f"Integridad OK: {manifest['ejecucion_id']}; estado={manifest['estado']}; SOLO lote reproducible: excluye DWG/PDF mutables, no acredita ejecución ni aprobación CAD")
            return 0
        result = run(audit, args.dry_run, args.entrada_prueba,diagnostico=args.diagnostico)
        if not args.dry_run:
            from .cad import prepare_copy
            prepare_copy(audit,result)
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
