# Checkpoint de revisión — Codex, Proceso 1

Marcar cada ítem como `OK`, `NO`, `BLOQUEADO` y asociar prueba, comando o evidencia. **Ninguna casilla pasa por declaración del agente sin evidencia.**

| ID | Criterio | Evidencia esperada | Estado |
|---|---|---|---|
| R01 | No se modificó el histórico ni la DWT | Git diff; SHA-256 de muestra; rutas write revisadas | Pendiente |
| R02 | CLI por carpeta interactiva y `--auditoria`; lista XLSX antes de leer | Demo sintética y prueba CLI | Pendiente |
| R03 | Cuatro familias XLSX reconocidas sin nombres hardcodeados | Tests por adaptador | Pendiente |
| R04 | Filas XML con formato masivo e imágenes ignoradas de forma segura | Fixture 1,048,576 filas XML; memoria | Pendiente |
| R05 | Coordenadas estrictas, variaciones inequívocas, auxiliares y errores reportados | Unit tests NW; incidencias | Pendiente |
| R06 | `Registro` excluido; tipos canónicos correctos | Unit test + CSV | Pendiente |
| R07 | Duplicado exacto sin redondeo; un prevalente con todas las ocurrencias | Integración + linaje | Pendiente |
| R08 | Prioridad por lista explícita, no mtime o glob | Config inválida falla; corrida repetible | Pendiente |
| R09 | Maestro informativo, nunca filtro del plano individual | Fixture con mismo poste en maestro/individual | Pendiente |
| R10 | Baseline ausente = `NO_DETERMINADO` | `summary.csv` | Pendiente |
| R11 | `01_elementos_normalizados.csv` solo tres columnas y UTF-8 | Comparación exacta de encabezado y CSV escaping | Pendiente |
| R12 | Linaje, incidencias, asociaciones, resumen, manifiesto | Validadores de encabezado/esquema y conteos | Pendiente |
| R13 | Mirador 551 y Otay 969 reconstruidos en etapa cruda previa a limpieza (no exigir mismos totales finales) | Regresión lectura origen + histórico | Pendiente |
| R14 | CRS no validado impide CSV proyectado «válido» | Test de gating P-06 | Pendiente |
| R15 | CRS validado en fixture produce proyección correcta sin +11.5m | Test `pyproj always_xy` | Pendiente |
| R16 | Sin topología confirmada no se anuncian rutas confirmadas | Test de propuestas PENDIENTE_CONFIRMACION | Pendiente |
| R17 | No se crearon `.scr`, DWG, DWT, PDF ni cambios CAD | `git status`/revisión archivos | Pendiente |
| R18 | Reejecución determinista y recuperación ante interrupción | hashes CSV idénticos; no salida parcial | Pendiente |
| R19 | Código cubierto por pruebas, instrucciones reproducibles PowerShell | `pytest`/lint+README | Pendiente |
| R20 | Decisiones P-01..P-11 pendientes distinguidas de reglas aprobadas | Informe final de Codex | Pendiente |

## Aceptación del primer PR/lote

Solo dar visto bueno al código de Proceso 1 cuando R01–R20 cumplan o estén bloqueados **con razón correcta y sin falsear un producto**. En particular, R14 puede bloquear el CSV proyectado real mientras P-06 no tenga controles; eso **no** invalida el ETL 1A. No iniciar SCR ni CAD sin nuevo encargo.
