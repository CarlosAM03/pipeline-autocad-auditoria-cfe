"""Ámbitos acreditados: polígonos/corredores WGS84; sin reparación geométrica."""
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET
from .util import PipelineError, sha256, within

MAX_XML = 16 * 1024 * 1024


def safe_xml(data):
    if len(data) > MAX_XML or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise PipelineError('XML espacial inseguro o excede límite')
    return ET.fromstring(data)


def coordinate(text):
    try:
        parts = [float(v) for v in text.split(',')]
        if len(parts) not in (2,3) or not all(math.isfinite(v) for v in parts) or not (-180 <= parts[0] <= 180 and -90 <= parts[1] <= 90):
            raise ValueError()
    except (ValueError, TypeError) as exc:
        raise PipelineError('Coordenada espacial inválida') from exc
    return parts[:2]


def kml_geometries(root):
    ns = {'k':'http://www.opengis.net/kml/2.2'}
    geometries = []
    for poly in root.findall('.//k:Polygon', ns):
        rings = []
        for bound in ['outerBoundaryIs','innerBoundaryIs']:
            for node in poly.findall('k:'+bound+'/k:LinearRing/k:coordinates', ns):
                rings.append([coordinate(v) for v in (node.text or '').split()])
        geometries.append(dict(type='Polygon', coordinates=rings))
    for line in root.findall('.//k:LineString/k:coordinates', ns):
        geometries.append(dict(type='LineString',coordinates=[coordinate(v) for v in (line.text or '').split()]))
    return geometries


def load_geofence(audit, spec):
    if not spec or not spec.get('archivo'):
        return None, None
    if not all(spec.get(k) for k in ('evidencia','responsable','fecha','version')) or spec.get('crs') != 'EPSG:4326':
        raise PipelineError('Ámbito espacial requiere evidencia/responsable/fecha/versión y EPSG:4326')
    path = within(audit / 'entrada' / spec['archivo'], audit / 'entrada')
    if path.stat().st_size > MAX_XML:
        raise PipelineError('Ámbito excede límite')
    data = path.read_bytes()
    if path.suffix.lower() == '.kml':
        geometries = kml_geometries(safe_xml(data))
    elif path.suffix.lower() in ('.json','.geojson'):
        obj = json.loads(data)
        if obj.get('crs') and obj['crs'] not in ('EPSG:4326',):
            raise PipelineError('CRS GeoJSON no admitido')
        geometries = [f['geometry'] for f in obj['features']] if obj.get('type') == 'FeatureCollection' else [obj['geometry'] if obj.get('type') == 'Feature' else obj]
    else:
        raise PipelineError('Ámbito debe ser GeoJSON o KML')
    from shapely.geometry import shape
    from shapely.ops import transform, unary_union
    from pyproj import Transformer
    areas = []
    for geom in geometries:
        typ = geom.get('type')
        if typ not in ('Polygon','MultiPolygon','LineString','MultiLineString'):
            raise PipelineError('Geometría de ámbito no admitida')
        lines = geom['coordinates'] if typ in ('Polygon','MultiLineString') else [geom['coordinates']]
        if typ == 'MultiPolygon':
            lines = [r for poly in geom['coordinates'] for r in poly]
        for ring in lines:
            if len(ring) < (4 if 'Polygon' in typ else 2):
                raise PipelineError('Anillo/línea incompleto')
            for p in ring:
                if len(p) < 2 or not all(math.isfinite(float(v)) for v in p) or not (-180 <= p[0] <= 180 and -90 <= p[1] <= 90):
                    raise PipelineError('Vértice fuera de rango')
            if any(abs(a[0]-b[0]) > 180 for a,b in zip(ring,ring[1:])):
                raise PipelineError('Ámbito cruza antimeridiano; dividir explícitamente')
            if 'Polygon' in typ and ring[0] != ring[-1]:
                raise PipelineError('Anillo no cerrado explícitamente')
        area = shape(geom)
        if area.is_empty or not area.is_valid:
            raise PipelineError('Ámbito geométricamente inválido')
        if 'LineString' in typ:
            width = float(spec.get('corredor_m',0))
            if not math.isfinite(width) or width <= 0:
                raise PipelineError('Corredor requiere distancia métrica positiva acreditada')
            center = area.centroid
            metric = f'+proj=aeqd +lat_0={center.y} +lon_0={center.x} +datum=WGS84 +units=m'
            forward = Transformer.from_crs(4326,metric,always_xy=True).transform
            inverse = Transformer.from_crs(metric,4326,always_xy=True).transform
            area = transform(inverse,transform(forward,area).buffer(width))
        areas.append(area)
    if not areas:
        raise PipelineError('Ámbito vacío')
    merged = unary_union(areas)
    return merged, dict(archivo=spec['archivo'],sha256=sha256(path),aprobada=spec.get('aprobada') is True,
                        version=spec['version'],crs='EPSG:4326')


def contains(area, lat, lon):
    from shapely.geometry import Point
    return area.covers(Point(float(lon),float(lat)))
