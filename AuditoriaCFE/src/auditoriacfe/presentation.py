"""Encuadre y colocación de anotaciones en papel, sin editar puntos Model."""
from dataclasses import dataclass, replace
import math

from .util import PipelineError

VIEW = (145, 70, 675, 535)
SYMBOL_WIDTH = {'POSTE': .9, 'CAJA_EMP': .9, 'EXCEDENTE': 1.3}


@dataclass(frozen=True)
class Profile:
    escala_detalle: float = 6.0
    poste_mm: float = 1.1
    caja_mm: float = 1.1
    excedente_mm: float = 1.4
    coordenada_mm: float = 1.8
    identificador_mm: float = 0.0
    separacion_mm: float = 2.0
    margen_mm: float = 12.0
    lider_max_mm: float = 48.0

    @classmethod
    def parse(cls, value):
        if not isinstance(value, dict) or value.keys() - cls.__dataclass_fields__.keys():
            raise PipelineError('cad.presentacion requiere parámetros reconocidos')
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in value.values()):
            raise PipelineError('Parámetro de presentación no finito')
        profile = cls(**value)
        if not (0.01 <= profile.escala_detalle <= 1000 and
                all(.1 <= size <= 10 for size in profile.sizes.values()) and
                .5 <= profile.coordenada_mm <= 5 and 0 <= profile.identificador_mm <= 5 and
                1 <= profile.separacion_mm <= 10 and 5 <= profile.margen_mm <= 60 and
                5 <= profile.lider_max_mm <= 100):
            raise PipelineError('Parámetros de presentación fuera de rango técnico')
        return profile

    @property
    def sizes(self):
        return dict(POSTE=self.poste_mm, CAJA_EMP=self.caja_mm, EXCEDENTE=self.excedente_mm)


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def bounds(points):
    return [min(p[axis] for p in points) for axis in ('x', 'y')] + [
        max(p[axis] for p in points) for axis in ('x', 'y')]


def paper(point, center, scale):
    return (410 + (point['x'] - center[0]) / scale, 302.5 + (point['y'] - center[1]) / scale)


def camera(box, minimum, margin):
    x0, y0, x1, y1 = box
    return [(x0+x1)/2, (y0+y1)/2], max(minimum, (x1-x0)/(530-2*margin), (y1-y0)/(465-2*margin))


def placement(points, center, scale, profile):
    """Cajas conservadoras SHX; los líderes pertenecen a Paper, sin topología."""
    anchors = [paper(point, center, scale) for point in points]
    obstacles = [(x-1, y-1, x+1, y+1) for x,y in anchors]
    output = []
    margin = profile.margen_mm
    for point, (x,y) in zip(points, anchors):
        h = profile.coordenada_mm
        width = max(len(point['geo'])*h, len(point['label'])*profile.identificador_mm)
        height = h + (profile.identificador_mm + 1 if profile.identificador_mm else 0)
        for radius in range(0, int(profile.lider_max_mm)+1, 4):
            gap = profile.separacion_mm + radius
            options = ((x+gap,y-height/2), (x-gap-width,y-height/2),
                       (x-width/2,y+gap), (x-width/2,y-gap-height),
                       (x+gap,y+gap), (x-gap-width,y+gap), (x+gap,y-gap-height),
                       (x-gap-width,y-gap-height))
            for left, bottom in options:
                box = (left, bottom, left+width, bottom+height)
                if not (VIEW[0]+margin <= left and VIEW[1]+margin <= bottom and
                        box[2] <= VIEW[2]-margin and box[3] <= VIEW[3]-margin):
                    continue
                padded = (left-1,bottom-1,box[2]+1,box[3]+1)
                if any(overlaps(padded, other) for other in obstacles):
                    continue
                near = (min(max(x,left),box[2]), min(max(y,bottom),box[3]))
                if math.dist((x,y),near) > profile.lider_max_mm:
                    continue
                obstacles.append(padded)
                output.append(dict(**point, ancla=(x,y), caja=box, fin_lider=near))
                break
            else:
                continue
            break
        else:
            return None
    return output


def plan(points, profile, layout):
    """Cada punto se asigna una vez. Se divide por extensión o falta de espacio."""
    pages = []
    def split(group):
        box = bounds(group)
        center, scale = camera(box, profile.escala_detalle, profile.margen_mm+45)
        labels = None
        if scale <= profile.escala_detalle:
            labels = placement(group, center, scale, profile)
        if labels is None and len(group) == 1:
            raise PipelineError('No cabe una etiqueta completa en la ventana')
        if labels is not None:
            pages.append(dict(bbox=box, centro=center, escala=scale, etiquetas=labels))
            return
        axis = 'x' if box[2]-box[0] >= box[3]-box[1] else 'y'
        ordered = sorted(group, key=lambda p: (p[axis],p['id']))
        middle = len(ordered)//2
        if scale > profile.escala_detalle:
            gaps = [(b[axis]-a[axis], index) for index,(a,b) in enumerate(zip(ordered,ordered[1:]),1)]
            gap, index = max(gaps)
            if gap > profile.escala_detalle*80:
                middle = index
        split(ordered[:middle])
        split(ordered[middle:])

    split(sorted(points,key=lambda p:(p['y'],p['x'],p['id'])))
    if len(pages) > 1:
        box = bounds(points)
        center, scale = camera(box, profile.escala_detalle, profile.margen_mm+10)
        markers = [dict(id=f'SECTOR_A4-{i}',x=detail['centro'][0],y=detail['centro'][1],
                        geo=f'D{i}',label='') for i,detail in enumerate(pages,2)]
        marker_profile = replace(profile, coordenada_mm=2.3, identificador_mm=0)
        marks = placement(markers, center, scale, marker_profile)
        if marks is None and marker_profile.lider_max_mm < 100:
            # La general admite llamadas más largas que las etiquetas de campo.
            marks = placement(markers, center, scale, replace(marker_profile, lider_max_mm=100))
        if marks is None:
            raise PipelineError('Las referencias de sectores no caben en la vista general')
        pages.insert(0,dict(bbox=box,centro=center,escala=scale,etiquetas=[],sectores=marks))
    for index,page in enumerate(pages,1):
        page.update(numero=index,layout=layout if index==1 else f'DATRA_A4_{index:03d}',
                    vista='GENERAL' if not page['etiquetas'] else 'DETALLE',
                    simbolos_mm={k:v*profile.escala_detalle/page['escala'] for k,v in profile.sizes.items()})
    return pages
