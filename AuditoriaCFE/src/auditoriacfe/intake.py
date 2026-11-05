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
        missing=[source for source in sources if not (history/'postes'/source).is_file()]
        if missing:
            reports[name]=dict(estado='PENDIENTE_EVIDENCIA',fuentes_ausentes=missing)
            continue
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
        extras=[]
        for source,target_name in [(history/'Rutas Con nombre Ultima Version.kmz','rutas_candidatas.kmz'),
                                   (PROJECT/'recursos/PlantillaMarcoDatraMapaTijuana.dwg','base_trabajo.dwg')]:
            if not source.is_file():continue
            target=output_path(entry/target_name,audit)
            if target.exists() and sha256(target)!=sha256(source):
                raise PipelineError('Recurso operativo cambió: no sobrescribir copia')
            if not target.exists():shutil.copyfile(source,target)
            extras.append(dict(archivo=target_name,sha256=sha256(target),origen=source.relative_to(PROJECT.parent).as_posix()))
            if source.suffix=='.kmz':cfg['kmz']=dict(archivo=target_name,tolerancia_m=0)
            else:cfg['cad']=dict(base_dwg=target_name,copia=True,unidades_verificadas=False,layout='DATRA_A1')
        (entry/'manifiesto_recursos.json').write_text(json_text(extras),encoding='utf-8')
        config_file = output_path(audit/'configuracion.json',audit)
        if not config_file.exists():
            config_file.write_text(json_text(cfg),encoding='utf-8')
        reports[name]=copied
    return reports


def prepare_master():
    """Derivado de extracción fiel, comparación informativa separada del inventario."""
    from .schemas import extract
    from .reporting import csv_file,MINIMUM
    import csv
    import io
    import hashlib
    from datetime import date
    source=PROJECT.parent/'Auditorias-20261104T035633Z-1-001/postes/Postes_CFE.xlsx'
    if not source.exists():return dict(estado='PENDIENTE_EVIDENCIA',motivo='Postes_CFE.xlsx ausente')
    checksum=sha256(source)
    rows,_,_=extract(source,source.name,checksum)
    stream=io.StringIO(newline='')
    writer=csv.writer(stream);writer.writerow(MINIMUM)
    writer.writerows([r['ruta_original'],r['tipo_original'],r['coordenada_original']] for r in rows)
    expected=hashlib.sha256(stream.getvalue().encode('utf-8')).hexdigest()
    for name in ('Natura','Mirador','Otay-Florido'):
        audit=within(AUDITS/name,AUDITS)
        if not (audit/'entrada').is_dir():continue
        path=output_path(audit/'entrada/referencia_maestro.csv',audit)
        if path.exists() and sha256(path)!=expected:raise PipelineError('Derivado maestro modificado: no sobrescribir ni atribuir procedencia falsa')
        if not path.exists():csv_file(path,MINIMUM,([r['ruta_original'],r['tipo_original'],r['coordenada_original']] for r in rows))
        proof_file=audit/'entrada/procedencia_maestro.json'
        copied_date=date.today().isoformat()
        if proof_file.exists():
            previous=json.loads(proof_file.read_text(encoding='utf-8'))
            if previous.get('fuente_sha256')!=checksum or previous.get('derivado_sha256')!=sha256(path):
                raise PipelineError('Procedencia maestro no concuerda con archivos')
            copied_date=previous['fecha_copia']
            date.fromisoformat(copied_date)
        proof=dict(fuente_sha256=checksum,derivado_sha256=sha256(path),fecha_copia=copied_date,
                   fecha_levantamiento='NO_DETERMINADO',uso='INFORMATIVO_NO_BASELINE')
        proof_file.write_text(json_text(proof),encoding='utf-8')
        config_file=audit/'configuracion.json'
        cfg=json.loads(config_file.read_text(encoding='utf-8'))
        if cfg.get('maestro_informativo') is None:
            cfg['maestro_informativo']=dict(archivo='entrada/referencia_maestro.csv',fecha=copied_date+' (copia; levantamiento NO_DETERMINADO)')
            config_file.write_text(json_text(cfg),encoding='utf-8')
    return dict(estado='GENERADO_INFORMATIVO',filas=len(rows),fuente_sha256=checksum)
