## Actualización del checklist — 2026-11-05

La sección original inferior conserva su fecha y evidencia; sus referencias a “futuro SCR”, P-09 propuesto o manifiestos fuera de salida fueron sustituidas por ADR-001/P-09 v1.

- OK: CP-01/02, revisión/manual por hash/fila, cuatro familias, dedup exacta/IDs, linaje y múltiples rutas, geofence y reader 02 v1/v2.
- OK: KMZ seguro y propuestas NO_CONFIRMADAS; aristas humanas verificables con ciclos/ramas y sin atajos DFS.
- OK técnico: dos SCR, LISP empaquetado, guard de copia, bloques/capas/etiquetas/ID, conteos reales, distancias confirmadas, A1, idempotencia; falta aceptación CAD física.
- OK: manifiestos v2 en salida, migración y fallos recuperables; CLI individual y batch independiente; 80 pruebas locales aprobadas, compile/lint/custodia.
- OK local: Natura/Mirador/Otay/General con 438/493/747/4131 grupos y hashes reproducibles; 01 sin admitidos y 02 real ausente por gates acreditables.
- PENDIENTE EVIDENCIA: P-03, P-06, aristas definitivas, impresión legible A1/DWT y aceptación humana. [Checklist CAD nativo](../02_Harness_Integral/CHECKLIST_CAD_NATIVO.md).
- CI/PR/protección y último intento nativo: resultado final en cierre del arnés; no marcar OK sin ejecución.


Cierre posterior: ensayo Core Console 2026 aprobado en fixture y cuatro auditorías, con repetición de SCR02, persistencia y cinco PDF de una A1. No acredita CRS real ni aceptación visual/productiva; General y Mirador presentan solapamientos por calidad geográfica y densidad. Detalles y gates vigentes: [cierre integral](../02_Harness_Integral/CIERRE_INTEGRAL_2026-11-05.md).

---

# Checkpoint de revisión — Codex, Proceso 1

Marcar cada ítem como `OK`, `NO`, `BLOQUEADO` y asociar prueba, comando o evidencia. **Ninguna casilla pasa por declaración del agente sin evidencia.**

| ID | Criterio | Evidencia esperada | Estado |
|---|---|---|---|
| R01 | No se modificó el histórico ni la DWT | 9 hashes XLSX antes/después +2 CSV contra diagnóstico; destinos limitados a auditorías; sin comandos CAD ni escrituras en recursos | OK |
| R02 | CLI por carpeta interactiva y `--auditoria`; lista XLSX antes de leer | test_dry_run_no_writes_and_cli_modes + CLI de tres corridas reales de prueba | OK |
| R03 | Cuatro familias XLSX reconocidas sin nombres hardcodeados | test_four_families_hidden_images_blank_sheet + test_nine_originals_four_families_and_7043_occurrences | OK |
| R04 | Filas XML con formato masivo e imágenes ignoradas de forma segura | 1,048,576 filas XML; pico Python 522,967 bytes; ZipFile.open monitorizado sin medios/drawings | OK |
| R05 | Coordenadas estrictas, variaciones inequívocas, auxiliares y errores reportados | test_strict_coordinates_and_exact_precision + test_recovery_auxiliary_and_conflicts | OK |
| R06 | `Registro` excluido; tipos canónicos correctos | test_scope_unknown_remote_empty_route_and_missing_geography + Demo-Sintetica + Otay real | OK |
| R07 | Duplicado exacto sin redondeo; un prevalente con todas las ocurrencias | test_exact_dedup_precedence_routes_types_and_nearby + tests de IDs + linaje real | OK |
| R08 | Prioridad por lista explícita, no mtime o glob | test_configuration_invalid_and_complete_inventory + inversión de orden y cambio de mtime | OK (precedencia productiva P-01 pendiente) |
| R09 | Maestro informativo, nunca filtro del plano individual | test_master_and_baseline_are_independent_and_not_filter; referencias reales declaradas | OK |
| R10 | Baseline ausente = `NO_DETERMINADO` | Tests de baseline + summary de las dos auditorías históricas de prueba | OK |
| R11 | `01_elementos_normalizados.csv` solo tres columnas y UTF-8 | test_csv_escaping_contract_counts_hashes_and_manifest_location; demo revisable | OK |
| R12 | Linaje, incidencias, asociaciones, resumen, manifiesto | Reconciliación y hashes en tests y tres corridas; manifiestos fuera de salida por AGENTS | OK (contrato auxiliar PROPUESTA P-09) |
| R13 | Mirador 551 y Otay 969 reconstruidos en etapa cruda previa a limpieza (no exigir mismos totales finales) | test_mirador_551_literal_and_56_repetitions + test_otay_969_one_spacing_difference_and_218_repetitions | OK |
| R14 | CRS no validado impide CSV proyectado «válido» | Tests de bloqueo; 02 ausente en datos reales | OK en código; producto real BLOQUEADO P-06 |
| R15 | CRS validado en fixture produce proyección correcta sin +11.5m | test_projection_gate_and_correct_always_xy; integral meridiana independiente; Demo 4/4 | OK (solo fixture) |
| R16 | Sin topología confirmada no se anuncian rutas confirmadas | topologia_propuesta vacía con razón en manifiesto; estado NO_CONFIRMADA; cercanía no crea aristas | OK |
| R17 | No se crearon `.scr`, DWG, DWT, PDF ni cambios CAD | Inventario de nuevos archivos y Git; recursos sin versionar preexistentes intactos | OK |
| R18 | Reejecución determinista y recuperación ante interrupción | Tests de rollback/estado de caída; Mirador y Otay byte a byte idénticos en dos corridas; verify OK | OK (simulación de interrupción; no apagado físico) |
| R19 | Código cubierto por pruebas, instrucciones reproducibles PowerShell | unittest: 29 OK, 0 omitidas; compileall OK; pip check OK; README con comandos | OK (sin linter ni porcentaje de cobertura declarado) |
| R20 | Decisiones P-01..P-11 pendientes distinguidas de reglas aprobadas | RESULTADO_IMPLEMENTACION, PRUEBAS_Y_VALIDACION y PENDIENTES_PARA_REVISION | OK |

## Aceptación del primer PR/lote

Solo dar visto bueno al código de Proceso 1 cuando R01–R20 cumplan o estén bloqueados **con razón correcta y sin falsear un producto**. En particular, R14 puede bloquear el CSV proyectado real mientras P-06 no tenga controles; eso **no** invalida el ETL 1A. No iniciar SCR ni CAD sin nuevo encargo.

Corte de ejecución: 2026-11-04. Estados anteriores corresponden a evidencia técnica ejecutada, **no al visto bueno del responsable ni cierre de P-01..P-11**. La admisión geográfica real también está BLOQUEADA por P-03; los grupos se conservan en REVISAR. Evidencia detallada y comandos: [PRUEBAS_Y_VALIDACION.md](PRUEBAS_Y_VALIDACION.md).

## Extensión CSV 00 y auditoría JS desde 7baa82c

Los controles R01–R20 continúan vigentes y las 29 pruebas anteriores pasan sin modificarlas. Suite ampliada:43 OK,0 fallos,0 omitidas. CP-01 es un resultado adicional; no cierra bloqueos de CP-02 ni aprueba P-xx.

| ID | Criterio adicional | Evidencia ejecutada | Estado |
|---|---|---|---|
|E01|00 funciona sin P-03/P-06|test_pending_p03_p06_identified_is_not_admitted; Mirador494/Otay749|OK|
|E02|Una fila por ID identificado, sin inventar identidad para rechazos/ambigüedades|test_ids_and_unidentifiable_records_not_invented; invariantes y linaje real|OK|
|E03|Precisión, precedencia, subrutas e IDs acreditados preservados|test_exact_identity_precision_subroutes_and_prevalence; tests de cajas originales y nuevos|OK|
|E04|No promoción automática a 01/02, ni filtros de aislados|tests de estados/ámbito/aislados; demo5/4/4, reales494/0 y749/0|OK|
|E05|Compatibilidad con artefactos anteriores|Oráculo reporting.py de 7baa82c y snapshot local de tres lotes; solo conteos y manifiestos ampliados|OK|
|E06|00 integrado en hashes/conteos/verificador|43 tests + validar_extension_local.py, dos corridas idénticas por lote|OK|
|E07|533/965 TXT y algoritmos JS verificados directamente|test_js_historicos.py; copias + fs restringido, nunca MAIN/generarSCR|OK|
|E08|Retornos y ramas auditados sin perpetuar error documental|ordenar padre; trayectoria sin retorno; 13/15 atajos respecto de grafo; propuesta separada|OK|
|E09|CP-01..CP-04 explícitos, sin alterar ADR/TO-BE|PROPUESTA_CHECKPOINTS_CP01_CP04 y manifest checkpoints; CP-03/04 futuros|OK|
|E10|Commit local exclusivo, sin outputs/datos/recursos ajenos|Lista explícita de 18 archivos revisados; cierre por git diff --cached/git show y git status; README raíz ajeno excluido|OK en alcance; identidad de commit en cierre Git|
