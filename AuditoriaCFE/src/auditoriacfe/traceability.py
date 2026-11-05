"""Libros aditivos v1, sin ETL alternativo. OOXML determinista y portable.

Datos exclusivamente textuales, sin fórmulas, medios ni vínculos externos.
Diseño de referencia inspeccionado con Artifact Tool; emisión stdlib para CI.
"""
import csv
import json
import math
import zipfile
from xml.sax.saxutils import escape, quoteattr
from .util import PipelineError, digest, sha256

NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
NAMES=('01_trazabilidad_limpieza.xlsx','02_trazabilidad_transformacion.xlsx')


def column(index):
    result=''
    while index:
        index,rem=divmod(index-1,26);result=chr(65+rem)+result
    return result


def text(value):
    if value is None:return ''
    if isinstance(value,(dict,list)):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return str(value)


def workbook(path,sheets):
    """ISO/IEC 29500 mínimo: inlineStr evita coerción incluso de =,+,-,@."""
    parts={
        '_rels/.rels':f'<Relationships xmlns="{REL}"><Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        'xl/workbook.xml':f'<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join(f'<sheet name={quoteattr(name)} sheetId="{i}" r:id="r{i}"/>' for i,(name,_) in enumerate(sheets,1))+'</sheets></workbook>',
        'xl/_rels/workbook.xml.rels':f'<Relationships xmlns="{REL}">'+''.join(f'<Relationship Id="r{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+f'<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
        'xl/styles.xml':f'''<styleSheet xmlns="{NS}"><fonts count="2"><font><sz val="10"/><name val="Arial"/><color rgb="FF17364D"/></font><font><b/><sz val="10"/><name val="Arial"/><color rgb="FFFFFFFF"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF17364D"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="49" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="49" fontId="1" fillId="2" borderId="0" xfId="0" applyNumberFormat="1"><alignment vertical="center" wrapText="1"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>''',
    }
    overrides=['<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>','<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    for i,(name,rows) in enumerate(sheets,1):
        rows=list(rows);width=max((len(row) for row in rows),default=1)
        widths=[]
        for c in range(width):
            heading=text(rows[0][c])
            desired=68 if ('sha256' in heading or heading.endswith('_id')) else 44 if 'coordenad' in heading else 28
            if heading in ('valor','estado'):desired=68
            widths.append(max(desired,min(58,len(heading)+3)))
        if len(rows)>1048576 or width>16384:raise PipelineError('Libro excede límites Excel')
        data=[]
        for r,row in enumerate(rows,1):
            cells=[]
            for c,value in enumerate(row,1):
                value=text(value)
                if len(value)>32767 or any(ord(ch)<32 and ch not in '\t\n\r' for ch in value):
                    raise PipelineError('Texto no representable sin pérdida en XLSX')
                cells.append(f'<c r="{column(c)}{r}" s="{1 if r==1 else 0}" t="inlineStr"><is><t xml:space="preserve">{escape(value)}</t></is></c>')
            lines=max((sum(max(1,math.ceil(len(line)/max(1,widths[c]-3))) for line in text(v).split('\n')) for c,v in enumerate(row)),default=1)
            height=34 if r==1 else min(409, max(30,lines*14+6))
            data.append(f'<row r="{r}" ht="{height}" customHeight="1">'+''.join(cells)+'</row>')
        ref=f'A1:{column(width)}{max(len(rows),1)}'
        cols=''.join(f'<col min="{c}" max="{c}" width="{widths[c-1]}" customWidth="1"/>' for c in range(1,width+1))
        parts[f'xl/worksheets/sheet{i}.xml']=f'<worksheet xmlns="{NS}"><dimension ref="{ref}"/><sheetViews><sheetView workbookViewId="0" showGridLines="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetFormatPr defaultRowHeight="30"/><cols>{cols}</cols><sheetData>'+''.join(data)+f'</sheetData><autoFilter ref="{ref}"/></worksheet>'
        overrides.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    parts['[Content_Types].xml']='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'+''.join(overrides)+'</Types>'
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,xml in sorted(parts.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,xml.encode('utf-8'),compresslevel=9)


def csv_rows(stage,name,empty_header):
    path=stage/name
    if not path.exists():return [empty_header]
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.reader(f))


def generate_workbooks(stage,manifest,edges):
    from .reporting import MINIMUM,PROJECTED_V2,PROJECTED
    from .network import CONFIRMED
    source_hashes=[[p.name,sha256(p),str(p.stat().st_size)] for p in sorted(stage.iterdir()) if p.is_file() and p.suffix in ('.csv','.jsonl','.json')]
    source_id=digest(source_hashes)
    records=[json.loads(line) for line in (stage/'linaje_y_calidad.jsonl').read_text(encoding='utf-8').splitlines()]
    fields=['ocurrencia_id','elemento_id','tipo_original','tipo_canonico','ruta_original','ruta_salida','coordenada_original','coordenada_normalizada','latitud','longitud','archivo_relativo','archivo_sha256','hoja','fila','estado','prevalente_id','resolucion_manual','incidencias']
    summary=[['metrica','valor'],['contrato','trazabilidad-xlsx-v1'],['auditoria',manifest['auditoria']],['fuentes_derivadas_id',source_id],['estado','PRELIMINAR; NO ES ACEPTACION PRODUCTIVA']]
    summary.extend([[k,text(v)] for k,v in manifest['conteos'].items()])
    hashes=[['archivo','sha256','bytes']]+source_hashes+[[f"entrada/{s['archivo']}",s['sha256'],s['bytes']] for s in manifest['fuentes_ordenadas']]
    clean=[('Resumen',summary),('Unificados',csv_rows(stage,'00_elementos_unificados.csv',[])),('Revision',csv_rows(stage,'00_elementos_revision.csv',[])),('Incidencias',csv_rows(stage,'reporte_incidencias.csv',[])),('Linaje',[fields]+[[text(r.get(k,'')) for k in fields] for r in records]),('Fuentes_Hashes',hashes)]
    gates=[['control','estado'],['contrato','trazabilidad-xlsx-v1'],['auditoria',manifest['auditoria']],['fuentes_derivadas_id',source_id],['P03',manifest['checkpoints']['CP-02']['admision_geografica']],['P06',manifest['crs']['estado']],['Proyeccion_Validada','SIN FILAS: P03/P06 no acreditados' if not (stage/'02_elementos_proyectados.csv').exists() else 'CSV02 acreditado por controles; aceptación humana pendiente'],['Proyeccion_Diagnostica','DIAGNOSTICO_NO_VERIFICADO; no acredita CRS ni conectividad'],['P05',text(manifest.get('topologia_detalle'))],['P04/P07/P08','PENDIENTE_OWNER; BLOQUEADO_FINAL']]
    transform=[('Resumen_Gates',gates),('Admision_P03',csv_rows(stage,'01_elementos_normalizados.csv',MINIMUM)),('Proyeccion_Validada',csv_rows(stage,'02_elementos_proyectados.csv',PROJECTED_V2 if manifest['schema_version']['02']==2 else PROJECTED)),('Proyeccion_Diagnostica',csv_rows(stage,'02_DIAGNOSTICO_NO_VERIFICADO.csv',PROJECTED_V2)),('Asociaciones_Rutas',csv_rows(stage,'asociaciones_elemento_ruta.csv',[])),('Topologia_Propuesta',csv_rows(stage,'topologia_propuesta.csv',[])),('Topologia_Confirmada',[CONFIRMED]+[[row[k] for k in CONFIRMED] for edge in edges for row in edge.get('asociaciones',[edge])])]
    for name,sheets in zip(NAMES,(clean,transform)):workbook(stage/name,sheets)
    return dict(contrato='trazabilidad-xlsx-v1',fuentes_derivadas_id=source_id,archivos=list(NAMES),precision='TEXTO_EXACTO',formulas=0)
