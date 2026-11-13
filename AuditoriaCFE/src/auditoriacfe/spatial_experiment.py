"""Grafo auxiliar WGS84 para experimentos de representación A4.1.1."""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from itertools import combinations
from math import isclose
from statistics import mean, median, pstdev

from pyproj import Geod

from .util import PipelineError, digest

RADII = (50, 100, 200, 300)
BINS = (0, 1, 5, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 500, 1000)
GEOD = Geod(ellps='WGS84')


def position(row):
    try:
        lat, lon = (Decimal(row[k]) for k in ('latitud', 'longitud'))
        if lat.is_finite() and lon.is_finite() and -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
    except (InvalidOperation, TypeError, KeyError):
        pass
    return None


def distance(a, b):
    return GEOD.inv(float(a[1]), float(a[0]), float(b[1]), float(b[0]))[2]


def within_radius(meters, radius):
    # Tolerancia numérica submicrométrica para Geod.fwd seguido de Geod.inv.
    return meters <= radius or isclose(meters, radius, rel_tol=0, abs_tol=1e-8)


def describe(values):
    data = sorted(values)
    if not data:
        return dict(n=0)
    def quantile(q):
        i = (len(data)-1)*q
        j = int(i)
        return data[j] + (i-j)*(data[min(j+1,len(data)-1)]-data[j])
    bins = [(lo, hi, [v for v in data if lo <= v < hi]) for lo,hi in zip(BINS,BINS[1:])]
    bins.append((BINS[-1], None, [v for v in data if v >= BINS[-1]]))
    lo,hi,modal = max(bins,key=lambda b:len(b[2]))
    return dict(n=len(data), minimo=data[0], maximo=data[-1], media=mean(data), mediana=median(data),
                desviacion_poblacional=pstdev(data), **{f'p{p}':quantile(p/100) for p in (10,25,75,90,95)},
                histograma=[dict(desde=a,hasta=b,n=len(v)) for a,b,v in bins],
                moda=[lo,hi], media_modal=mean(modal), n_modal=len(modal),
                dentro_radios={r:sum(within_radius(v,r) for v in data) for r in RADII})


def components(adjacency):
    """DFS iterativo. Un puente desconecta el grafo espacial al retirarlo."""
    discovered, low, parent = {}, {}, {}
    groups, bridges = [], set()
    for root in range(len(adjacency)):
        if root in discovered:
            continue
        discovered[root] = low[root] = len(discovered)
        group = [root]
        stack = [(root, iter(adjacency[root]))]
        while stack:
            node, neighbors = stack[-1]
            neighbor = next(neighbors, None)
            if neighbor is None:
                stack.pop()
                if node in parent:
                    prev = parent[node]
                    low[prev] = min(low[prev], low[node])
                    if low[node] > discovered[prev]:
                        bridges.update((prev, node))
            elif neighbor not in discovered:
                parent[neighbor] = node
                discovered[neighbor] = low[neighbor] = len(discovered)
                group.append(neighbor)
                stack.append((neighbor, iter(adjacency[neighbor])))
            elif neighbor != parent.get(node):
                low[node] = min(low[node], discovered[neighbor])
        groups.append(sorted(group))
    return groups, bridges


class Inventory:
    def __init__(self, rows):
        self.rows = {r['elemento_id']: r for r in rows}
        if len(self.rows) != len(rows):
            raise PipelineError('Inventario espacial contiene IDs repetidos')
        self.locations = {key: position(r) for key,r in self.rows.items()}
        self.by_position = defaultdict(list)
        for key,p in self.locations.items():
            if p is not None:
                self.by_position[p].append(key)
        self.posts = sorted(p for p,ids in self.by_position.items()
                            if any(self.rows[k]['tipo']=='POSTE' for k in ids))
        self.indices = {p:i for i,p in enumerate(self.posts)}
        self.distances = {}
        for p in self.by_position:
            lon,lat = float(p[1]),float(p[0])
            if self.posts:
                _,_,values = GEOD.inv([lon]*len(self.posts),[lat]*len(self.posts),
                                      [float(v[1]) for v in self.posts],[float(v[0]) for v in self.posts])
                self.distances[p] = values
            else:
                self.distances[p] = []
        self.neighbors = [sorted(d for j,d in enumerate(self.distances[p]) if i!=j)
                          for i,p in enumerate(self.posts)]

    def statistics(self):
        return {k:describe([row[k-1] for row in self.neighbors if len(row)>=k]) for k in (1,2,3,5)}

    def fusion(self):
        positions = sorted(self.by_position)
        for i,p in enumerate(positions):
            for a,b in combinations(self.by_position[p],2):
                yield a,b,0.0,'COINCIDENTE_EXACTA'
            for q in positions[i+1:]:
                # Margen conservador: un grado de latitud supera 110 km.
                if q[0]-p[0] > Decimal('0.0001'):
                    break
                meters = distance(p,q)
                if meters <= 10:
                    band = '0_A_1_M' if meters <= 1 else '1_A_5_M' if meters <= 5 else '5_A_10_M'
                    for a in self.by_position[p]:
                        for b in self.by_position[q]:
                            yield a,b,meters,band

    def classify(self, radius, *, experimental=True):
        if experimental and radius not in RADII:
            raise PipelineError('Radio ajeno al experimento')
        adjacent = [[j for j,d in enumerate(self.distances[p]) if i!=j and within_radius(d,radius)]
                    for i,p in enumerate(self.posts)]
        groups, bridges = components(adjacent)
        lookup, summaries, retained = {}, [], set()
        for group in groups:
            code = 'S-' + digest([list(map(str,self.posts[i])) for i in group])[:16]
            for i in group:
                lookup[i] = (code,len(group))
            if len(group)>=6:
                retained.update(group)
            summaries.append(dict(componente=code, posiciones=len(group), conservado=len(group)>=6,
                                  ids_poste=[k for i in group for k in self.by_position[self.posts[i]]
                                             if self.rows[k]['tipo']=='POSTE']))
        results = {}
        for key,p in self.locations.items():
            if p is None:
                results[key] = dict(incluido=False,motivo='COORDENADA_INVALIDA')
                continue
            i = self.indices.get(p)
            ds = self.distances[p]
            nearest = min((ds[j],j) for j in retained) if retained else (None,None)
            nearest_id = next((k for k in self.by_position[self.posts[nearest[1]]]
                               if self.rows[k]['tipo']=='POSTE'),None) if retained else None
            post = self.rows[key]['tipo']=='POSTE'
            supported = nearest[0] is not None and within_radius(nearest[0],radius)
            ties = supported and any(abs(ds[j]-nearest[0])<=1e-8 and lookup[j]!=lookup[nearest[1]]
                                     for j in retained)
            included = i in retained if post else supported and not ties
            anchor = i if post else nearest[1]
            component,size = lookup.get(anchor,('',0))
            alerts = []
            if post and included:
                if len(adjacent[i])==1:
                    alerts.append('PUNTO_TERMINAL')
                if i in bridges:
                    alerts.append('PUENTE_ESPACIAL')
            results[key] = dict(incluido=included, componente=component, postes=size,
                motivo=('CONSERVADO' if included else 'MICROCOMPONENTE_ESPACIAL' if post else 'PENDIENTE_REVISION'),
                vecinos=len(adjacent[i]) if post else sum(within_radius(d,radius) for d in ds),
                distancia_vecino=min((d for j,d in enumerate(ds) if not post or j!=i),default=None),
                distancia_conservado=nearest[0], vecino_conservado_id=nearest_id, alertas=alerts,
                soporte=('POSTE' if post else 'EMPATE_COMPONENTES' if ties else
                         'POSTE_CONSERVADO_DENTRO_RADIO' if supported else 'SIN_SOPORTE_DENTRO_RADIO'))
        return results,summaries
