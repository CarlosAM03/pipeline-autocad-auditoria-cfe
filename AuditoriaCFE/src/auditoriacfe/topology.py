"""Diagnóstico de cercanía optativo; jamás autoriza conectividad."""
import math
from itertools import product
from collections import defaultdict


def nearby(records, threshold):
    if threshold is None:
        return []
    from pyproj import Geod
    geod = Geod(ellps="WGS84")
    buckets, pairs = defaultdict(list), []
    step = float(threshold)
    for r in records:
        lat, lon = float(r["latitud"]), float(r["longitud"])
        phi, lam = math.radians(lat), math.radians(lon)
        # ECEF sobre elipsoide: cuerda <= distancia geodésica; 27 celdas vecinas.
        n = 6378137 / math.sqrt(1 - 0.0066943799901413165 * math.sin(phi) ** 2)
        xyz = (n * math.cos(phi) * math.cos(lam), n * math.cos(phi) * math.sin(lam),
               n * (1 - 0.0066943799901413165) * math.sin(phi))
        cell = tuple(math.floor(v / step) for v in xyz)
        for delta in product((-1, 0, 1), repeat=3):
            for other in buckets[tuple(a + b for a, b in zip(cell, delta))]:
                if r["tipo_canonico"] != other["tipo_canonico"]:
                    continue
                _, _, distance = geod.inv(lon, lat, float(other["longitud"]), float(other["latitud"]))
                if 0 < distance <= step:
                    pairs.append([other["elemento_id"], r["elemento_id"], repr(distance), "REVISAR_NO_FUSIONAR"])
        buckets[cell].append(r)
    return pairs
