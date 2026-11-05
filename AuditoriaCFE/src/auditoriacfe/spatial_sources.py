"""KML/KMZ acotado, sin extracción ni red; evidencia candidata exclusivamente."""
import stat
import zipfile
from pathlib import PurePosixPath
from .geofence import safe_xml, coordinate
from .util import PipelineError, sha256

NS={'k':'http://www.opengis.net/kml/2.2'}
MAX_TOTAL=64*1024*1024
MAX_PART=16*1024*1024


def read_kml(data, source):
    root=safe_xml(data);result=[]
    for index,pm in enumerate(root.findall('.//k:Placemark',NS)):
        name=pm.findtext('k:name','',NS)
        fields={}
        for node in pm.findall('.//k:Data',NS):
            key=node.get('name','')
            if key in fields:raise PipelineError('ExtendedData ambiguo')
            fields[key]=node.findtext('k:value','',NS)
        for node in pm.findall('.//k:SimpleData',NS):
            key=node.get('name','')
            if key in fields:raise PipelineError('ExtendedData ambiguo')
            fields[key]=node.text or ''
        identity=pm.get('id') or fields.get('id') or name or str(index)
        for typ in ('Point','LineString','Polygon'):
            for part,node in enumerate(pm.findall('.//k:'+typ,NS)):
                coord=node.find('.//k:coordinates',NS)
                raw=coord.text or '' if coord is not None else ''
                try:
                    points=[coordinate(v) for v in raw.split()]
                    if not points or (typ=='Point' and len(points)!=1) or (typ=='LineString' and len(points)<2):
                        raise PipelineError('Geometría KML vacía/incompatible')
                except PipelineError as exc:
                    result.append(dict(fuente=source,fuente_id=f'{identity}:{typ}:{part}',id_externo=identity,
                                       nombre=name,tipo='INVALIDA',coordenadas=[],coordenadas_originales=raw,
                                       error=str(exc),datos=fields,estado='RECHAZADA_PARA_GEOMETRIA'))
                    continue
                result.append(dict(fuente=source,fuente_id=f'{identity}:{typ}:{part}',id_externo=identity,
                                   nombre=name,tipo=typ,coordenadas=points,coordenadas_originales=raw,datos=fields,
                                   estado='NO_CONFIRMADA'))
    return result


def read_spatial(path):
    if path.suffix.lower()=='.kml':
        if path.stat().st_size>MAX_PART:raise PipelineError('KML demasiado grande')
        features=read_kml(path.read_bytes(),path.name)
    elif path.suffix.lower()=='.kmz':
        features=[]
        with zipfile.ZipFile(path,'r') as book:
            entries=book.infolist()
            if len(entries)>4096 or sum(i.file_size for i in entries)>MAX_TOTAL:
                raise PipelineError('KMZ excede presupuesto ZIP')
            names=set()
            for item in entries:
                p=PurePosixPath(item.filename)
                if p.is_absolute() or '..' in p.parts or '\\' in item.filename or ':' in item.filename or item.filename in names:
                    raise PipelineError('Ruta/duplicado ZIP inseguro')
                if stat.S_ISLNK(item.external_attr>>16) or item.flag_bits&1:
                    raise PipelineError('KMZ cifrado o con enlaces no admitido')
                names.add(item.filename)
                if item.file_size>MAX_PART or (item.file_size>1024*1024 and item.file_size/max(1,item.compress_size)>200):
                    raise PipelineError('Posible ZIP bomb')
            kmls=sorted(n for n in names if n.lower().endswith('.kml'))
            if not kmls:raise PipelineError('KMZ sin KML')
            for name in kmls:features.extend(read_kml(book.read(name),path.name+'/'+name))
    else:
        raise PipelineError('Solo KML/KMZ admitidos')
    return features,dict(archivo=path.name,sha256=sha256(path),features=len(features),
                         puntos=sum(f['tipo']=='Point' for f in features),lineas=sum(f['tipo']=='LineString' for f in features),
                         invalidas=sum(f['tipo']=='INVALIDA' for f in features),
                         estado='FUENTE_CANDIDATA_NO_CONFIRMADA')
