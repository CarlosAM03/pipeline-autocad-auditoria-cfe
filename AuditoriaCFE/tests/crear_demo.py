"""Crea exclusivamente Demo-Sintetica para revisión de productos sin datos reales."""
import json
from support import AUDITS, GEO, record, xlsx
from auditoriacfe.pipeline import run
from auditoriacfe.util import within


def main():
    audit = within(AUDITS / "Demo-Sintetica", AUDITS)
    audit.mkdir(parents=True, exist_ok=True)
    entry = within(audit / "entrada", audit)
    xlsx(entry / "demo.xlsx", rows=[
        (2, record(route='Demo "A", tramo 1'), False),
        (3, record(route="Demo B"), True),
        (4, record(typ="cajadedmpalme"), False),
        (5, record(typ="excedente", coord="32.50001N 117W"), False),
        (6, record(typ="Registro", coord="No detectado"), False),
        (7, record(coord="432.464440N 116.8W"), False),
        (8, record(coord="2.5N 117W"), False),
        (9, record(coord="No detectado", extras={"F": "32.50002N", "G": "117W", "H": "32.50002", "I": "-117"}), False),
    ], images=True)
    doc = within(audit / "CONTROLES_SINTETICOS.txt", audit)
    doc.write_text("FIXTURE SINTETICO. Controles analíticos sobre meridiano central UTM 11. No acredita cartografía ni autorización CAD real.\n", encoding="utf-8")
    cfg = dict(auditoria=audit.name, fuentes_en_orden=["demo.xlsx"], geografia_permitida=GEO,
               crs_candidato="EPSG:32611", crs_validado=True, cercanos_m=5,
               evidencia_crs=dict(archivo=doc.name, aprobado_por="FIXTURE SINTETICO", fecha="2026-11-04",
                                  crs="EPSG:32611", unidades="m", tolerancia_m=0.01,
                                  controles=[dict(id="C1", latitud=0, longitud=-117, este_m=500000, norte_m=0),
                                             dict(id="C2", latitud=1, longitud=-117, este_m=500000, norte_m=110530.15880237566)]))
    (audit / "configuracion.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run(audit, readonly_root=entry)


if __name__ == "__main__":
    main()
