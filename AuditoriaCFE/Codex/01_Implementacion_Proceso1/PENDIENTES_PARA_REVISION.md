# Pendientes para revisión — Proceso 1

## Extensión CP-01 vigente

Código 0.2.0 y auditoría JS completados; **43 pruebas OK, sin fallos ni omisiones**. Los 29 del registro previo siguen intactos. CP-01 ya no queda oculto por P-03/P-06: 00 muestra 494/749 grupos históricos y5 de demo, sin aprobar CAD. Las clasificaciones inferiores siguen aplicando a las etapas indicadas, **no bloquean la exportación de grupos identificados a 00**.

| Pendiente de esta extensión | Clase | Decisión exacta del responsable |
|---|---|---|
|P-09, contrato de 00 | NO BLOQUEANTE | Revisar/ratificar las 12 columnas propuestas, estados IDENTIFICADO/admisión/apto_csv_01, conteos aditivos y vistas de grupos, conforme a EXTENSION_ETL_UNIFICADO.md. No convertir CP-01 en aprobación CAD. |
|Discrepancia JS frente aTO-BE:260 | NO BLOQUEANTE | Aprobar corrección documental separada: retorno al padre en ordenar.js, preorden con atajos entre ramas en trayectoria.js. La etapa afectada es futura generación CAD; no se replica ninguno como topología física ni se modifica norma aquí. |
|Organización CP-01..CP-04 | NO BLOQUEANTE | Revisar PROPUESTA_CHECKPOINTS_CP01_CP04.md para futura incorporación normativa; no cambia los dos procesos ni autoriza SCR en esta entrega. |
|P-01 producción | BLOQUEANTE | Fijar orden real de fuentes/hojas antes de CP-01 productivo. Las configuraciones de prueba no constituyen prioridad aprobada. |
|P-03/P-06 | BLOQUEANTE | Aportar perímetro para admisión de01 y controles reales DWG para 02; CP-01 puede completarse con ambos pendientes. |
|Entorno local previo | NO BLOQUEANTE | `.venv` apunta a un intérprete inaccesible; se conservó y se verificó con `.venv-cp01`. Opcionalmente reparar el entorno habitual fuera de este cambio. |
|README.md raíz preexistente | NO BLOQUEANTE | Archivo del usuario sin seguimiento conservado por hash y excluido del commit; decidir separadamente si desea versionarlo. |
|Dependencias de pruebas de auditoría | NO BLOQUEANTE | Node solo para reproducción de copias JS y Git con 7baa82c para oráculo de compatibilidad. Documentar instalación en otras máquinas si requiere ejecutar esas pruebas; el ETL no depende de Node. |

No hay fallos técnicos abiertos atribuibles a esta extensión. P-02/P-04/P-05/P-07/P-08/P-10/P-11 conservan alcance y decisión inferior; ninguna se aprobó por alcanzar43 tests. Siguiente checkpoint: revisar CSV 00 y propuestas, publicar manualmente el commit local tras revisión y resolver precondiciones de CP-02. CP-03/CP-04 requieren otro encargo.

## Registro y pendientes de la primera implementación

Fecha: 2026-11-04. Estado: **implementación y pruebas completadas; checkpoint de revisión**. Sin aprobación de reglas nuevas ni inicio de Proceso 2. No hay fallos automatizados abiertos (29 pruebas OK); estos pendientes delimitan aceptación operativa, evidencia o mejoras.

| Pendiente | Clase | Decisión requerida del responsable |
|---|---|---|
| P-01 | BLOQUEANTE para producción | Aprobar y declarar precedencia completa por auditoría y orden de hojas. Las listas Prueba-Historica-* solo reproducen controles técnicos. El programa falla sin lista completa; no elige autoridad por mtime ni directorio. |
| P-02 | NO BLOQUEANTE | Identificar fuente, fecha y auditoría de baseline; sin ella NO_DETERMINADO. |
| P-03 | BLOQUEANTE para admisión geográfica validada | Acreditar perímetro y tratamiento de ubicaciones remotas. Config admite límites rectangulares con evidencia; si se requiere polígono deberá precisarse antes de aceptar ese control. Sin perímetro los grupos quedan REVISAR: por ello los CSV dibujables reales de prueba contienen solo cabecera. No se promovió la ventana exploratoria [32,33]/[-118,-116] a regla aprobada. |
| P-04 | BLOQUEANTE para liberación final | Aprobar criterio de cierre de incidencias; lotes PRELIMINAR. |
| P-05 | NO BLOQUEANTE para ETL | Definir validación humana de aristas; topología propuesta vacía, sin conexiones inferidas. |
| P-06 | BLOQUEANTE para proyección real | Acreditar CRS del CAD, unidades y al menos dos controles no coincidentes, junto con responsable, fecha, evidencia archivada y tolerancia. CHECKPOINT_PLANTILLA_BASE_v1 y README Fase3B confirman que marco visual/UTM visible no resuelven esta validación. El módulo funciona en fixture; no hay 02 real. |
| P-07, P-08, P-10 | NO BLOQUEANTE para Proceso 1 | Resolver cajetín, legibilidad A1 y perfil AutoCAD en una etapa posterior. |
| P-09 | NO BLOQUEANTE para revisión de código; requiere aprobación antes de congelar integración | Revisar esquema auxiliar PROPUESTA, estados, escala decimal, IDs, comparación incompleta, conteos identificados/exportables, conservación literal de rutas y ubicación de manifiestos fuera de salida. Ratificar la política conservadora de recuperación (sin cachés de fórmula no acreditados, ni sustitución de magnitudes mundiales imposibles). No se cambió ADR/TO-BE. |
| P-11 | NO BLOQUEANTE | Conciliar clave y ámbito del conteo Mirador 56/58; no alterar histórico. |

Discrepancia documental: el contrato propuesto enumera manifiesto entre salidas; AGENTS.md exige manifiestos fuera de entrada/salida. Se aplica la autoridad superior: `manifiestos/` por auditoría. Decisión requerida: ratificar esta ubicación al aprobar P-09.

## Incidencias de origen pendientes

| Caso | Clase | Evidencia | Decisión exacta requerida |
|---|---|---|---|
| Longitud STD `11702014028W` | BLOQUEANTE para incorporar ese componente | Diagnóstico y regresión: STD fila 2, también copia y maestro. Se rechaza, sin insertar punto decimal. | Proporcionar corrección corroborada en una nueva fuente/versionado o resolución documentada; no autorizar una conjetura de dígitos. |
| Otay latitud `432.464440N` | BLOQUEANTE para incorporar esas ocurrencias | FLO-OTAY final filas 198/604; 2 rechazos. | Corroborar la ubicación del elemento y entregar dato corregido con evidencia; el programa no lo aproxima. |
| Posiciones mundiales válidas pero remotas | BLOQUEANTE para admisión local final | Ejemplos `2.52867353N`, `177.083774W` y alerta diagnóstica `116.48565W`. Sin perímetro todo el lote interpretable queda REVISAR. | Aprobar área y corroborar casos remotos o excluirlos expresamente con razón de negocio. |
| Auxiliares discrepantes/enteros/errores y cachés | NO BLOQUEANTE para texto primario válido | Linaje y reporte mantienen fórmulas, valores y discrepancias; nunca reparan escala. | Definir si se desea revisión selectiva de cachés y qué evidencia acredita vigencia; no hace falta para usar primaria válida dentro de área aprobada. |
| Identificadores de equipos | NO BLOQUEANTE para deduplicación por defecto | No hay ID confiable automáticamente extraído de Numero; se probó mecanismo de evidencia por ocurrencia. | Aportar IDs y evidencia de dos cajas físicas distintas para activar la excepción; confirmar ámbito/nomenclatura de IDs antes de usar datos reales. |

## Limitaciones técnicas y mejoras

| Pendiente | Clase | Impacto y siguiente acción requerida |
|---|---|---|
| SharedStrings XML >16 MiB | MEJORA | Falla explícita y preserva corrida anterior; nueve libros reales están debajo del límite. Responsable: decidir si futuros casos justifican índice en disco. No es bloqueo observado. |
| Consumo proporcional a registros útiles | MEJORA | El lector limita XML/formato/medios; consolidación/reportes conservan ocurrencias reales. Medición 522,967 bytes de Python en lector sintético, sin promesa de RSS para millones de activos. Responsable: fijar presupuesto de memoria si crece el volumen útil. |
| Durabilidad ante caída física | MEJORA | Se probaron KeyboardInterrupt y estados de renombrado simulados, no apagado real. El activo se actualiza al final; consumidor debe verificar hashes y reejecutar si no coinciden. Responsable: definir si requiere journal/fsync o prueba de corte eléctrico antes de automatización desatendida. |
| Topología propuesta sin aristas | BLOQUEANTE | Bloquea únicamente rutas finales P-05; no bloquea ETL ni puntos. Está permitido producir archivo vacío con razón explícita. Responsable: proporcionar mecanismo y evidencia de validación física, no autorizar DFS/proximidad como conectividad. |
| Cercanía sin umbral operativo | NO BLOQUEANTE | Reporte optativo implementado; sin cercanos_m se informa NO_EVALUADA, no se decide un umbral automáticamente. Responsable: seleccionar umbral diagnóstico si desea ese reporte en corridas reales. |
| Referencia maestra con casos no comparables | NO BLOQUEANTE | Manifest conserva casos inválidos del maestro; ausencia de coincidencia puede quedar NO_DETERMINADO. Responsable: resolver calidad del maestro si necesita acreditar ausencias. |
| Alias Windows python | NO BLOQUEANTE | Entorno .venv funcional creado desde Thonny; README incluye comando exacto. Responsable: opcionalmente configurar Python estándar para su operación cotidiana. |

## Recomendación del siguiente checkpoint

1. Revisar `RESULTADO_IMPLEMENTACION.md`, `PRUEBAS_Y_VALIDACION.md`, checklist R01–R20 y los CSV de Demo-Sintetica. Aceptar o ajustar la propuesta P-09 sin modificar reglas aprobadas silenciosamente.
2. Declarar fuentes/hojas productivas P-01 y perímetro/evidencia P-03 para cada auditoría. Definir baseline P-02 si requiere novedad; nunca usar ausencia en maestro como sustituto.
3. Resolver coordenadas rechazadas/remotas en fuentes nuevas o resoluciones acreditadas, definir liberación P-04 y aportar evidencia CAD P-06. Reejecutar Proceso 1 y verificar hashes/conteos.
4. Autorizar expresamente el siguiente proceso solo tras ese checkpoint; no iniciar SCR/AutoCAD/DWG/PDF con esta entrega.

No se requiere una decisión del responsable para corregir código o ejecutar las pruebas ya realizadas. Los bloqueos anteriores corresponden a autoridad funcional/evidencia real, no a trabajo técnico abandonado.
