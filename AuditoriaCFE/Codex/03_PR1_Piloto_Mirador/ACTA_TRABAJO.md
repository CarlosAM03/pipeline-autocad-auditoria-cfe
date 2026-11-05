# Piloto PR #1 — registro de trabajo

Referencia inicial: `97731f5b71d52e9a17db447d2e229359fa4c73cb`.
Rama: `codex/etl-unificado-auditoria-js`. PR #1 abierto y sin merge.

Se conservaron cinco archivos no rastreados del owner (tres del arnés,
encargo y revisión independiente). README_ENTREGA_Y_PASOS.md está restaurado
desde la fase anterior. No requiere nueva restauración.

Revisión independiente: `CODE_REVIEW_PR1_PIPELINE_CFE_2026-11-05.md`, SHA-256
`6ccc4c4b098e609dca56c73e90cd865e221174f9ad32db10d6ad3e9a60fae442`.
Encargo: `ENCARGO_CODEX_PR1_PILOTO_MIRADOR_EVIDENCIAS_v1.md`, SHA-256
`4d58837d938f90789fb3cb368fa3c1cfe7707076584fc23cfb2fcccc54919861`.
Ambos leídos, conservados sin cambios y excluidos del staging de la entrega.

Baseline ejecutado: **81 pruebas aprobadas, 0 fallidas, 0 omitidas**.
H01 reproducido semánticamente: una ruta global ajena a los extremos era aceptada.
H02 reproducido: bootstrap recibía cero argumentos y preparaba todas las auditorías.
Logs privados bajo `tests/_runtime/pr1_piloto/`; no se publican coordenadas.

Cambios en curso: pertenencias por extremo, preparación seleccionada, habilitación
integral independiente de CSV02, recuperación conservadora, verificación nativa
separada y libros aditivos. Inspección Core Console sobre copia nueva del marco.
Los ensayos reales se limitan a Mirador; snapshot inicial de 161 archivos en
las otras tres auditorías permite comprobar ausencia de escrituras.

Suite posterior: **92 pruebas aprobadas, 0 fallidas y 0 omitidas** en local;
incluye históricos disponibles y conserva las 43 originales. Compileall,
Ruff E9/F821/F822/F823, pip check y guardia de publicación ejecutados.
El ajuste final de viewport/atributos pasó nuevamente la suite completa:
92/92 en 109.737 s. No quedaron fallos unitarios sin resolver.

Mirador: 732 ocurrencias, 493 identificados (414 POSTE, 20 CAJA_EMP,
59 EXCEDENTE), 236 duplicados y 3 rechazos. 493 pendientes de admisión;
CSV01 con encabezado sin registros; CSV02 productivo ausente; diagnóstico
493 filas, cero aristas reales. Las cifras no cambian respecto al corte 493.
Dos corridas del mismo perfil comparadas por manifiesto/bytes, incluidos XLSX.

Core Console 2026 ejecutado en copias: Mirador 493/0 y fixture ficticio 6/5
(bloques/aristas), doble SCR02 y reapertura. Longitudes del fixture 30,30,40,50,50 m;
se verifican directamente desde entidades nativas, con tolerancia técnica 1e-6 m
para esta prueba analítica, sin acreditar tolerancia física del DWG DATRA.
Rollback de redibujado completo ensayado tras corregir el fallo del mecanismo UNDO.
El driver exige los tres atributos nativos del cajetín con sus conteos.

Las 13 hojas XLSX se importaron y renderizaron con Artifact Tool, sin fórmulas.
No se declara apertura interactiva Excel. AutoCAD GUI arrancó, pero el diálogo
no ofreció foco accesible verificable; no se introdujeron rutas ni comandos
y no se declara ensayo GUI de dibujo. Core Console sí ejecuta AutoCAD nativo.

Inspección visual de PDF: Mirador presenta conglomerados severos de etiquetas,
ámbito incierto y cinco paneles vacíos. El encabezado heredado de detalles
aprobados no constituye acreditación de paneles. El fixture permite comprobar
geometría sin inferir red real. Se corrigió margen de viewport tras detectar
recorte de texto extremo; los PDF definitivos se inspeccionaron nuevamente.
Ambos: una página, aproximadamente 841.022×594.078 mm, cero anotaciones,
Poppler y PyMuPDF OK. El PDF histórico sigue con 27128 anotaciones y Poppler
informa dimensiones 0×0 aunque devuelva exit0; no se considera validado.

Ejecución privada del ensayo previo al ajuste CI:
`cc71f3375580f366ce6491d77730a9923849b27ba502dbf5ac7ab38b1de32ded`.
Runtime nativo comprobado:
`9b78d7dcc4e442cf7f95b3d6933860f0ae8f63364433f75c50926a796d468693`.
La verificación final cotejó contratos, 13 hojas, 9 recursos originales y las
161 entradas de las otras auditorías. El paquete privado registra SHA del
commit y archivos; no se sube ni se incorporan datos de campo al staging.

| CP | Resultado del piloto |
|---|---|
| CP01 | COMPLETADO_TECNICO: 00, revisión, trazabilidad y linaje reconciliados |
| CP02 | PENDIENTE_EVIDENCIA: sin admisión productiva ni CRS real; diagnóstico separado |
| CP03 | COMPLETADO_TECNICO: compilación y ejecución Core en copia; GUI/plantilla pendientes |
| CP04 | PRELIMINAR: 493 puntos reales diagnósticos/0 líneas; fixture 6/5 solo ficticio |

CI remoto se verifica para el SHA que contenga esta acta; los históricos locales
no forman parte del clon público. Publicación restringida a código, tests y
documentación genérica, PR #1 abierto sin merge. No hay aprobación humana.

Regresión CI posterior al primer commit de revisión (073d17f): la suite pasó,
pero falló el benchmark de 100000 filas/1000 elementos. El grafo completo se
había serializado en una celda de Resumen_Gates y excedía 32767 caracteres.
Se reprodujo localmente, se sustituyó por estado + referencia al JSON íntegro
con hash, sin truncar datos ni cambiar topología, y se agregó una prueba con
10000 identidades ficticias. Benchmark corregido ejecutado: 3.165 s de pipeline
y verificación, RSS pico 45969408 bytes; es una medición local, no SLA.
La nueva suite completa pasó **93/93 en 85.716 s**, cero fallidas/omitidas.
Se conserva 073d17f y se publica un commit correctivo adicional, sin reescribir
historia. Los resultados CI del SHA exacto y el lote actualizado quedan en la
entrega y en el manifiesto del ZIP privado; no se extrapola el éxito local a CI.

Un runner Windows/Python3.12 reveló después un fallo del fixture H02: TEMP usa
el alias 8.3 RUNNER~1 y el guardia de escritura lo rechazó correctamente.
El fixture resuelve su raíz temporal a ruta canónica antes de crear el árbol.
No se relajó la protección de rutas de producción ni se omitió el caso.

Estados físicos sin cambio: P03/P05/P06/P07/P08/P04 pendientes. No hay
aceptación humana ni liberación FINAL. Los resultados nativos y paquete privado
se registrarán al ejecutarse, nunca a partir de expectativas.
