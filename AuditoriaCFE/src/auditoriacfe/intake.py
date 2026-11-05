"""Copias explícitas de fuentes autorizadas; nunca busca directorios alternativos."""
import json
import shutil
from .config import AUDITS, PROJECT
from .util import PipelineError, output_path, sha256, json_text, within

PREFIX = 'CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/'
SOURCES = {
    'Natura':['CFE Natura  - Datra/Natura  - Datra.xlsx'],
    'Mirador':[PREFIX+'Mirador/'+n for n in ('STD HACIA CNAL 12.xlsx','Ruta canal 12 level antes 2014 Completo.xlsx','Copy of STD HACIA CNAL 12.xlsx')],
    'Otay-Florido':[PREFIX+'Otay - Florido/'+n for n in ('ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx','RUTA FLO-OTAY FO96 final.xlsx','ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx')],
    'Tijuana-General':['Postes_CFE.xlsx']}


def bootstrap():
    history = PROJECT.parent/'Auditorias-20261104T035633Z-1-001'
    reports = {}
    for name,sources in SOURCES.items():
        audit = output_path(AUDITS/name,AUDITS)
        entry = output_path(audit/'entrada',audit)
        entry.mkdir(parents=True,exist_ok=True)
        copied = []
        for source in sources:
            original = within(history/'postes'/source,history/'postes')
            target = output_path(entry/original.name,audit)
            checksum = sha256(original)
            if target.exists() and sha256(target) != checksum:
                raise PipelineError('Copia operativa modificada: no sobrescribir')
            if not target.exists():
                shutil.copyfile(original,target)
            if sha256(target) != checksum or sha256(original) != checksum:
                raise PipelineError('Hash de copia no coincide')
            copied.append(dict(archivo=target.name,origen=source,sha256=checksum))
        manifest = output_path(entry/'manifiesto_fuentes.json',audit)
        manifest.write_text(json_text(copied),encoding='utf-8')
        cfg = dict(auditoria=name,fuentes_en_orden=[x['archivo'] for x in copied],hojas_por_fuente={},
                   excepciones_cabecera={},geografia_permitida=None,crs_validado=False,schema_02=2,
                   crs_candidato='EPSG:32611',baseline_historica=None,maestro_informativo=None)
        if name == 'Mirador':
            cfg['hojas_por_fuente']['Copy of STD HACIA CNAL 12.xlsx']=['Sheet1','Sheet2']
            cfg['excepciones_cabecera']['Ruta canal 12 level antes 2014 Completo.xlsx']={'Hoja1':'F3_D_VACIA'}
        config_file = output_path(audit/'configuracion.json',audit)
        if not config_file.exists():
            config_file.write_text(json_text(cfg),encoding='utf-8')
        reports[name]=copied
    return reports
