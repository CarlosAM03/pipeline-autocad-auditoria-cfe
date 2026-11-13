"""ZIP de revisión privado con inventario explícito; nunca incorpora un árbol completo."""
import json
import zipfile
from pathlib import PurePosixPath
from .util import PipelineError,json_text,sha256,within

REQUIRED='''README_PRIMERO.md
informes/CODE_REVIEW_RESOLUCION_H01_H10.md
informes/RESULTADOS_PRUEBAS.md
informes/E2E_MIRADOR.md
informes/VALIDACION_CAD_Y_PDF.md
informes/PASOS_OPERADOR.md
informes/PENDIENTES_ACEPTACION_OWNER.md
datos/01_trazabilidad_limpieza.xlsx
datos/02_trazabilidad_transformacion.xlsx
datos/resumen_conteos.csv
datos/extracto_revision.csv
datos/extracto_linaje.csv
datos/topologia_resumen.json
datos/manifiesto_ejecucion.json
cad/01_configurar_plano.scr
cad/02_dibujar_auditoria.scr
cad/cad_runtime.lsp
cad/cad_datos.lsp
cad/reporte_validacion_cad.json
cad/reporte_nativo_MIRADOR.txt
cad/reporte_nativo_FIXTURE.txt
planos/MIRADOR_DIAGNOSTICO_A1.pdf
planos/FIXTURE_GRAFO_CONFIRMADO_A1.pdf
vistas/mirador_pagina_completa.png
vistas/mirador_etiquetas_densas.png
vistas/mirador_cajetin_conteos.png
vistas/mirador_paneles.png
vistas/fixture_grafo_y_distancias.png
vistas/fixture_resumen.png
logs/pruebas_resumen.txt
logs/autocad_eventos_clave.txt
logs/versiones_entorno.txt'''.splitlines()


def build(staging,destination,metadata,origins):
    if set(origins)!=set(REQUIRED):raise PipelineError('Inventario de evidencia incompleto/no autorizado')
    files=[]
    for name in REQUIRED:
        parts=PurePosixPath(name)
        if parts.is_absolute() or '..' in parts.parts or '\\' in name:raise PipelineError('Ruta ZIP insegura')
        p=within(staging/name,staging)
        if not p.is_file():raise PipelineError('Falta evidencia requerida: '+name)
        files.append(dict(archivo=name,sha256=sha256(p),bytes=p.stat().st_size,tipo=p.suffix,
                          origen=origins[name],compresion='DEFLATE_9',redacciones='Consultar origen; PDF/XLSX/SCR/LISP íntegros'))
    manifest=dict(metadata,archivos=files,politica_hash='Inventario excluye MANIFEST_EVIDENCIAS.json y SHA256SUMS.txt para evitar autorreferencia; SHA256SUMS incluye manifiesto y contenidos, se excluye a sí mismo',
                  privados_excluidos=['XLSX fuente','DWG/DWT','KMZ','JSONL completo','caches','credenciales'])
    (staging/'MANIFEST_EVIDENCIAS.json').write_text(json_text(manifest),encoding='utf-8')
    inventory=REQUIRED+['MANIFEST_EVIDENCIAS.json']
    (staging/'SHA256SUMS.txt').write_text(''.join(sha256(staging/name)+'  '+name+'\n' for name in sorted(inventory)),encoding='ascii')
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(inventory+['SHA256SUMS.txt']):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(staging/name).read_bytes(),compresslevel=9)
    verify_package(destination)
    return dict(archivo=destination.name,bytes=destination.stat().st_size,sha256=sha256(destination),objetivo_12MiB=destination.stat().st_size<=12*1024*1024,
                top_10=sorted(files,key=lambda x:x['bytes'],reverse=True)[:10])


def verify_package(path):
    import hashlib
    with zipfile.ZipFile(path) as z:
        if set(z.namelist())!=set(REQUIRED+['MANIFEST_EVIDENCIAS.json','SHA256SUMS.txt']) or len(z.namelist())!=len(REQUIRED)+2:
            raise PipelineError('ZIP contiene archivos ausentes/adicionales/duplicados')
        if z.testzip():raise PipelineError('CRC de ZIP inválido')
        manifest=json.loads(z.read('MANIFEST_EVIDENCIAS.json'))
        if {r['archivo'] for r in manifest['archivos']}!=set(REQUIRED):raise PipelineError('Inventario de manifiesto incompleto')
        for item in manifest['archivos']:
            data=z.read(item['archivo'])
            if hashlib.sha256(data).hexdigest()!=item['sha256'] or len(data)!=item['bytes']:
                raise PipelineError('Hash de evidencia inválido: '+item['archivo'])
        sums=z.read('SHA256SUMS.txt').decode('ascii').splitlines()
        if len(sums)!=len(REQUIRED)+1:raise PipelineError('Checksum incompleto')
        for line in sums:
            checksum,name=line.split('  ',1)
            if hashlib.sha256(z.read(name)).hexdigest()!=checksum:raise PipelineError('SHA256SUMS inválido')
    return manifest
