"""Identidad exacta y prevalencia en orden declarado; ninguna arista inferida."""
from collections import defaultdict
from decimal import Decimal
from .util import decimal_key, digest


def key(record):
    return (record["tipo_canonico"], decimal_key(Decimal(record["latitud"])),
            decimal_key(Decimal(record["longitud"])))


def consolidate(records, audit):
    groups = defaultdict(list)
    for r in records:
        eligible = (r["estado"] in ("VALIDO", "REVISAR") and
                    r["tipo_canonico"] in ("POSTE", "CAJA_EMP", "EXCEDENTE") and
                    r["latitud"] is not None and r["ruta_salida"].strip() and
                    not any(i["codigo"] in ("FORMULA_PRIMARIA", "HEMISFERIO_NO_NW") for i in r["incidencias"]))
        if eligible:
            groups[key(r)].append(r)
    # Un ID acreditado en posiciones diferentes no prueba cuál es la correcta.
    positions = defaultdict(set)
    for k, group in groups.items():
        for r in group:
            if r.get("id_confiable"):
                positions[r["id_confiable"]["id"]].add(k)
    uniques = []
    for k, group in groups.items():
        ids = {r["id_confiable"]["id"] for r in group if r.get("id_confiable")}
        if any(len(positions[i]) > 1 for i in ids):
            for r in group:
                r["estado"] = "REVISAR"
                r["incidencias"].append(dict(codigo="ID_POSICIONES_CONFLICTIVAS", severidad="ERROR",
                                             motivo="Mismo ID confiable en tipos/posiciones diferentes"))
            continue
        # A06 solo acredita excepción multi-equipo para cajas.
        split = k[0] == "CAJA_EMP" and len(ids) > 1
        partitions = defaultdict(list)
        for r in group:
            identity = r.get("id_confiable", {}).get("id")
            if split and not identity:
                r["estado"] = "REVISAR"
                r["incidencias"].append(dict(codigo="ID_EQUIPO_AMBIGUO", severidad="ERROR",
                                             motivo="Varias cajas acreditadas; ocurrencia sin ID no asignable"))
            else:
                partitions[identity if split else None].append(r)
        for identity, occurrences in partitions.items():
            prevalent = occurrences[0]
            prevalent_state = prevalent["estado"]
            element = "E-" + digest(["identidad-v1", audit, *k, identity])
            if prevalent_state == "VALIDO":
                uniques.append(prevalent)
            for i, r in enumerate(occurrences):
                r.update(elemento_id=element, prevalente_id=prevalent["ocurrencia_id"],
                         estado=prevalent_state if i == 0 else "DUPLICADO")
                if i:
                    r["incidencias"].append(dict(codigo="DUPLICADO_EXACTO", severidad="INFO",
                                                 motivo="A04-A06: prevalece primera ocurrencia según fuentes/hojas/filas declaradas"))
    # Orden de salida por ocurrencia prevalente, sin orden geográfico.
    order = {r["ocurrencia_id"]: i for i, r in enumerate(records)}
    return sorted(uniques, key=lambda r: order[r["ocurrencia_id"]])
