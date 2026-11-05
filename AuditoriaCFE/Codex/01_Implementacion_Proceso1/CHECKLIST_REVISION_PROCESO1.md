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
