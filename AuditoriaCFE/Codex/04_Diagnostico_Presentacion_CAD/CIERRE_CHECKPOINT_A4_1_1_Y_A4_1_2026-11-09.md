# ACTA DE CIERRE — CHECKPOINTS A4.1.1 Y A4.1

**Proyecto:** Pipeline de Auditorías CFE / DATRA  
**Fecha de decisión:** 9 de noviembre de 2026 (Tijuana)  
**Documento:** Acta de decisión del owner, cierre de presentación y transferencia técnica A4.2  
**Estado:** **A4.1.1 CERRADO — A4.1 CERRADO POR ACEPTACIÓN DEL OWNER DE LA PRESENTACIÓN A 300 m**  
**Alcance de aprobación:** representación y presentación diagnóstica de Natura, Mirador y Otay–Florido; **no** aceptación FINAL de datos, conexiones, CRS, evidencia física ni plantilla maestra.  
**Decisión vinculante:** radio experimental de proximidad **300 metros** como **valor predeterminado elegido por el owner** para el filtrado cartográfico en las tres auditorías prioritarias. El sistema deberá persistir dicha política explícitamente y mantener la opción de sobrescribirla por auditoría, registrar el radio efectivo y conservar las exclusiones. La aprobación de la política no acredita todavía que el valor predeterminado esté implementado en el repositorio.

## 1. Antecedentes y línea de tiempo

El arnés original formalizó los procesos de preparación de fuentes XLSX, normalización y linaje; generación de dos XLSX de trazabilidad, dos SCR operativos y productos CAD sobre una copia de la plantilla DATRA. Los anteriores checkpoints A0–A3 diagnosticaron errores de encuadre, acoplamiento de escala y etiquetas densas. PR #1 incorporó mejoras técnicas de trazabilidad, control de custodia, XDATA y ejecución nativa.

**A4.1 — Presentación multipágina:** con ADR-002, se autorizó una A1 general y hojas de detalle dentro de un solo PDF por auditoría, símbolos menores, texto de coordenadas, un único Model Space y varios layouts de Paper Space. Se integró la fuente Bomberos dentro de Otay–Florido. Se generaron tres DWG y tres PDF auténticos con 16, 18 y 16 hojas (50 páginas), respectivamente. Las salidas se conservaron como PRELIMINARES. Checkpoint de referencia: `AuditoriaCFE/Codex/04_Diagnostico_Presentacion_CAD/A4_1_Presentacion_Rutas/CHECKPOINT_A4_1.md`, commit `acba0630d8be752877396113cf418ba3b706a376`.

**A4.1.1 — Depuración espacial experimental:** para investigar puntos aislados, encuadres dominados por extremos y páginas poco aprovechadas, el owner encargó 12 variantes independientes: 50, 100, 200 y 300 m en cada una de las tres auditorías. Se produjo un filtro no destructivo que determina visibilidad CAD, sin modificar las identidades ni convertir cercanía en conectividad de fibra. Implementación `0d478ac25c23b7677e39d4ea9b080dfdbd644818`, cierre de evidencia `be103b436c78ba5cba8d0896d3b00e7c0d131aa7`.

**Decisión posterior del owner:** comparadas las variantes de 200 y 300 m, ambas resultan satisfactorias para presentación y se **elige definitivamente 300 m como radio por defecto**. Con esta aceptación quedan cerrados A4.1.1 y el subproceso de legibilidad/paginación A4.1, sujeto a las reservas de información y de campo que se enumeran aquí. Se autoriza la transición al trabajo de A4.2, no la publicación FINAL ni la fusión de PR #1.

## 2. Metodología incorporada y reglas de conservación

1. Se mantiene fija la línea base de **1,680 identidades canónicas**, distribuidas en Natura (438), Mirador (493) y Otay–Florido (749). Este total no se sustituye por la cantidad visualizada en cada variante.
2. Se analizan las **posiciones POSTE distintas** y las distancias geodésicas sobre WGS84, en metros. Se calcularon distancias al vecino más próximo, clases modales, media, mediana, percentiles y otros vecinos; la media no se usó como umbral automático.
3. A cada radio se construye un **grafo auxiliar de proximidad**. Los componentes con **seis o más posiciones POSTE** pueden representarse; componentes de una a cinco posiciones se catalogan como microcomponentes espaciales. Esta clasificación no prueba si un poste existe físicamente ni describe la topología del cable.
4. Los tipos CAJA_EMP y EXCEDENTE se evalúan con su contexto espacial y pueden quedar `PENDIENTE_REVISION`; no son usados para completar artificialmente seis postes.
5. `INCLUIDO`, `MICROCOMPONENTE_ESPACIAL` y `PENDIENTE_REVISION` son decisiones **de presentación experimental**. No equivalen a eliminación de la fuente, rechazo contractual P-03 ni corrección de la coordenada.
6. Cada variante conserva inventario, CSV, linaje, asociaciones, incidencias, los dos XLSX con hoja adicional `Decision_Visual`, scripts `01_configurar_plano.scr` y `02_dibujar_auditoria.scr`, dependencias LISP, manifiestos e índice de presentación. Los grupos no dibujados figuran en `COORDENADAS_DESCARTADAS_VISUALIZACION.csv`, `SUMMARY_COORDENADAS_DESCARTADAS.csv/.md` y matriz por ID.
7. La paginación se recalcula **después** de la selección espacial, sin modificar X/Y de los elementos conservados. El Model Space aloja una única representación física por identidad; los layouts comparten ese modelo. No se dibujan supuestas líneas por proximidad.
8. La línea base cartográfica, simbología y presentación A4.1 se mantuvo para comparar radios sin mezclar simultáneamente otros cambios de diseño.
9. Las fuentes privadas y productos DWG/PDF de las doce variantes permanecen fuera del repositorio público.

## 3. Resultado integral de las doce variantes

| Ruta | Radio (m) | Incluidas | No representadas / revisión | % no representado | Páginas A1 | Δ páginas respecto A4.1 |
|---|---:|---:|---:|---:|---:|---:|
| Natura | 50 | 41 | 397 | 90.64% | 4 | −12 |
| Natura | 100 | 360 | 78 | 17.81% | 11 | −5 |
| Natura | 200 | 432 | 6 | 1.37% | 14 | −2 |
| **Natura** | **300** | **438** | **0** | **0.00%** | **16** | **0** |
| Mirador | 50 | 269 | 224 | 45.44% | 7 | −11 |
| Mirador | 100 | 465 | 28 | 5.68% | 10 | −8 |
| Mirador | 200 | 472 | 21 | 4.26% | 10 | −8 |
| **Mirador** | **300** | **472** | **21** | **4.26%** | **10** | **−8** |
| Otay–Florido | 50 | 317 | 432 | 57.68% | 8 | −8 |
| Otay–Florido | 100 | 729 | 20 | 2.67% | 12 | −4 |
| Otay–Florido | 200 | 741 | 8 | 1.07% | 12 | −4 |
| **Otay–Florido** | **300** | **741** | **8** | **1.07%** | **12** | **−4** |

**Interpretación:** a 50 m Natura pierde más de 90% de su representación y no es apropiado como base general. De 200 a 300 m Mirador y Otay–Florido conservan exactamente los mismos IDs, aunque pueden variar los componentes del grafo auxiliar. Natura recupera seis POSTE adicionales a 300 m. **Los tres PDF elegidos suman 38 hojas A1** frente a las 50 de A4.1; la reducción de hojas se concentra en Mirador y Otay–Florido.

### Desglose exacto de la elección a 300 m, validado contra la matriz privada

| Auditoría | Identidades base | Incluidas | Microcomponentes no dibujados | Pendientes de revisión no dibujados | Tipos conservados POSTE / CAJA_EMP / EXCEDENTE |
|---|---:|---:|---:|---:|---|
| Natura | 438 | 438 | 0 | 0 | 438 / 0 / 0 |
| Mirador | 493 | 472 | 15 POSTE | 6 EXCEDENTE | 399 / 20 / 53 |
| Otay–Florido | 749 | 741 | 8 POSTE | 0 | 578 / 17 / 146 |
| **Total** | **1,680** | **1,651** | **23** | **6** | **1,415 / 37 / 199** |

Las **29 identidades no representadas** se mantienen en la matriz y en los datos de custodia. No deben rotularse indiscriminadamente «29 errores humanos» ni «29 postes»: son **23 postes identificados como microcomponentes y seis excedentes pendientes**. En particular, **Natura no excluye ninguna identidad a 300 m**; por ello su posible presencia de outliers o datos equivocados no queda descartada por este método.

## 4. Descubrimientos y riesgos técnicos

### 4.1 Sensibilidad al radio

La distancia espacial de un poste a su vecino puede ser pequeña incluso cuando una posición es incorrecta; inversamente, un extremo o ramal legítimo puede quedar separado del resto. El filtro agrupa **cadenas de cercanía**, no segmentos confirmados de fibra, y podría conectar conceptualmente corredores independientes sin verificarlos físicamente. Se conserva el control humano sobre excepciones. El nuevo default de 300 m es una decisión de **presentación**, no una nueva regla de deduplicación ni una regla de red.

### 4.2 Distribución estadística y atípicos

Según los resultados de Codex, la clase modal al poste más cercano es **40–50 m en Natura**, **20–30 m en Mirador** y **30–40 m en Otay–Florido**. En Otay–Florido, mediana de vecino próximo **27.15 m** y media **5,725.93 m**, gravemente influida por extremos. La media global no debe convertirse en criterio de exclusión automática. Mantener reportes de distribución, vecinos próximos, componentes y puentes espaciales.

### 4.3 Cercanía y posible duplicación

Se registraron candidatos de fusión por cercanía: **23 pares Natura, 137 Mirador y 348 Otay–Florido**. Entre ellos, en Otay–Florido aparecen **24 pares exactamente coincidentes en 18 posiciones**, incluidos tipos distintos. Ninguno autoriza por sí mismo fusionar identidades: se requiere evidencia de que representan el mismo activo. Las 494 ocurrencias de la fuente Bomberos se conservaron en el linaje de Otay–Florido, incluyendo su precedencia histórica.

### 4.4 Territorio y cobertura

La geometría geoestadística municipal **AGEM Tijuana 02004** obtenida del INEGI se usó solo como contraste exploratorio. Se marcaron **14 identidades de Mirador** y **3 de Otay–Florido** fuera de ese polígono candidato; no se alteró por ello el filtro espacial. El ámbito oficial DATRA y la admisión P-03 siguen pendientes. No presentar un municipio, una capa candidata o el valor de radio como equivalentes a la delimitación comprobada de la red.

### 4.5 Legibilidad residual

Los tres PDF de 300 m muestran mejora notable en el aprovechamiento de hojas Mirador/Otay y eliminan varias vistas casi vacías causadas por microcomponentes. Persisten **bandas visuales de etiquetas** en sectores densos, especialmente Mirador (páginas 2–5, 8–10) y Otay–Florido (páginas 2–5, 7–12). El análisis de colisión **AABB=0** es una métrica computacional y **no prueba ausencia de cruces de líderes con calles o solapamiento perceptivo con el mapa**. La decisión del owner acepta esta presentación para cerrar A4.1, sin certificar la legibilidad física en impresión A1 ni eliminar la posibilidad de mejoras futuras no bloqueantes.

## 5. Evidencia reproducible y verificaciones independientes

**Evidencia de Codex, según actas y resultados públicos:** suite local de **101 pruebas aprobadas, cero fallidas, cero omitidas**; **12 ensayos CAD nativos** con ejecución de los dos SCR, repetición idempotente de SCR02, reapertura, XDATA, conteos y posición; **126 páginas** vectoriales A1 entre las doce variantes, verificadas con Poppler y PyMuPDF; 24 libros XLSX con hoja `Decision_Visual`; residuos XY máximos inferiores a 9.4×10⁻¹⁰ unidades Model. No se reportan pruebas en GUI ni impresión física A1 ejecutadas.

**Verificación independiente en esta revisión:**

- El archivo `A4_1_1_REVISION_PRIVADA.zip` contiene 7 entradas; CRC ZIP íntegro y 5/5 hashes explícitos de `SHA256SUMS.txt` coincidentes. SHA-256 del ZIP **`3b4fe1bd7c3dc356e09a8b76bb930a659dc4d2e2dd7b48d1135bdb9015094a1c`**.
- `MATRIZ_INCLUSION_EXCLUSION.csv` contiene **1,680 filas**, sin perder las identidades en la comparación; estados por auditoría y por tipo recalculados para 300 m como muestra la tabla anterior.
- Los tres PDF adjuntos abren mediante **Poppler/pdfinfo y PyMuPDF**; páginas **16 Natura, 10 Mirador, 12 Otay–Florido**, todas **2384×1684 pt**, A1 horizontal. Los PDF contienen gráficos vectoriales y elementos heredados; la extracción de texto convencional no recupera todos los rótulos CAD (no sirve como prueba de legibilidad).
- En GitHub, PR #1 `CarlosAM03/pipeline-autocad-auditoria-cfe` sigue **abierto, sin fusionar** en el SHA `be103b436c78ba5cba8d0896d3b00e7c0d131aa7`. El workflow del commit, **run 42604526678**, terminó en `success` con cuatro jobs aprobados: Ubuntu 3.10/3.12 y Windows 3.10/3.12.

**Alcance de la verificación:** no se reejecutó AutoCAD Core Console desde este entorno ni se inspeccionaron los doce DWG locales; esos ensayos se apoyan en las actas, pruebas y hashes producidos por Codex. Los tres PDF de 300 m y la matriz privada sí fueron accesibles directamente.

## 6. Decisiones formalizadas para el siguiente ciclo

**DEC-A4.1.1-001 — radio base:** el owner **aprueba 300 m por defecto** para Natura, Mirador y Otay–Florido, no 200 m. Mantener configurable un override explícito por auditoría y dejar registrada en los manifiestos la versión de política y el radio efectivo. La política se introduce como **enmienda adicional a ADR-002**, sin reescribir ADR-000/001 ni asumir que el código ya cambió su default.

**DEC-A4.1.1-002 — ámbito de la exclusión:** una identidad fuera de la visualización se conserva íntegra con evidencia y motivo en CSV, summary, XLSX, linaje e índice de auditoría; la fuente no se modifica. No promover un diagnóstico a descarte contractual, fusión física ni corrección irreversible de coordenada.

**DEC-A4.1.1-003 — presentación aceptada:** el owner acepta el resultado de 200/300 m como satisfactorio y elige **300 m como criterio de cierre** de la presentación A4.1. Un PDF multipágina A1 por auditoría, con la vista general y los detalles sectorizados, sigue siendo el contrato visual.

**DEC-A4.1.1-004 — prioridad:** los **tres planos de ruta** son el producto prioritario, Bomberos queda integrado en Otay–Florido. El cuarto plano `Tijuana-General`, proveniente de `Postes_CFE.xlsx`, permanece pendiente como entregable posterior y no se declara concluido.

**DEC-A4.1.1-005 — transición:** queda autorizada la **preparación de A4.2** para recuperar los componentes constructivos originales CFE y consolidar la plantilla maestra DATRA **sin reabrir automáticamente el radio o el sistema de paginación**.

## 7. Checklist de cierre A4.1.1 / A4.1

| Control | Estado | Alcance |
|---|---|---|
| Tres auditorías y Bomberos bajo Otay–Florido | CERRADO | No se creó una ruta autónoma Bomberos |
| 12 variantes independientes 50/100/200/300 m | CERRADO | 12 DWG/PDF, 24 XLSX y documentación reportados |
| Regla de microcomponentes y criterio de seis posiciones | CERRADO COMO EXPERIMENTO | No acredita conectividad física |
| Linaje, IDs y coordenadas sin eliminación | CERRADO | Matriz privada de 1,680 identidades comprobada |
| Summary y CSV de exclusiones por variante | CERRADO EN EVIDENCIAS DE CODEX | Recuperables desde las carpetas privadas |
| Contraste territorial AGEM | DIAGNÓSTICO CERRADO | P-03 no acreditado |
| Calibración de símbolos y escala A4.1 | ACEPTADA POR OWNER | Escala y parámetros de presentación actuales |
| Un PDF A1 por auditoría, con secciones | ACEPTADO | 16, 10 y 12 páginas con 300 m |
| 300 m como decisión predeterminada | APROBADA | **Pendiente confirmar su codificación/configuración efectiva** |
| Pruebas automatizadas y nativas | EVIDENCIADAS | 101 locales, 12 nativas; CI 4/4 |
| Etiquetas sin errores perceptivos en papel físico | NO ACREDITADO | GUI/impresión física pendientes |
| Fusiones por proximidad | NO AUTORIZADAS | 23 / 137 / 348 pares a revisar |
| P-03 geofence, P-05 conexiones, P-06 CRS/control | BLOQUEANTES DE FINAL | No se aprueban con esta acta |
| Detalles constructivos izquierdos | DIFERIDO A A4.2 | Fuente histórica editable disponible |
| Plano Tijuana-General | PENDIENTE | Cuarto producto posterior |
| PR #1 merge a main | NO AUTORIZADO | Sigue abierto |

## 8. Handoff obligatorio a A4.2 — Plantilla maestra DATRA/CFE

### Condición de entrada resuelta

El owner aprobó la presentación a 300 m para los **tres planos prioritarios**. **A4.2 puede iniciar** según el encargo previamente preparado; no es necesario volver a solicitar el radio ni rediseñar los tres PDF. A4.2 seguirá requiriendo aceptación expresa de la **plantilla final** y de cualquier contenido técnico CFE que se pretenda oficializar.

### Fuentes CFE existentes y usos previstos

En la raíz local `Auditorias-20261104T035633Z-1-001/` constan:

- `AuditoriaCFE2.dwg`: referencia **editable histórica v0.0.1**, fuente principal para inventariar bloques/detalles constructivos de la columna lateral izquierda.
- `AuditoriaCFE_0_0_1.PDF`: referencia visual del primer prototipo.
- `Plantilla (3)-ejemplo.pdf`: referencia de la plantilla original CFE, para cotejar geometría, diagramas, medidas y paneles.
- `tijuana.dwg`: recurso cartográfico histórico **solo como referencia**, nunca reemplaza silenciosamente la plantilla DATRA vigente.

Estas fuentes históricas son **solo lectura**. Copiar a entorno de trabajo, registrar hashes y unidades reales; no publicar materiales del cliente en GitHub.

### Entregable A4.2

Consolidar el marco DATRA basado en la plantilla vigente identificada por SHA, recuperando en copias los **cinco paneles izquierdos** (tensión, suspensión, derivación, empalme, otros), con trazabilidad hasta capas/bloques/handles originales. Validar unidades, cotas y contenido técnico; no inventar componentes si falta evidencia. Conservar mapa, orientación, simbología, cajetín, branding, layouts multipágina, escalas aprobadas, XDATA y procedimiento operatorio.

**Secuencia operativa que no debe cambiar:** (1) copiar la plantilla maestra a la carpeta de la auditoría; (2) abrir esa copia en AutoCAD 2026; (3) ejecutar `01_configurar_plano.scr`; (4) ejecutar `02_dibujar_auditoria.scr`; (5) revisar CAD y layouts; (6) producir un único PDF A1 multipágina por auditoría. Las dependencias LISP pueden cargarse automáticamente; no exigir un tercer SCR manual.

### Lista técnica al iniciar A4.2

1. Verificar el HEAD vigente y leer esta acta, ADR-002 y checkpoints A4.1/A4.1.1.
2. Convertir **300 m** en el **default efectivo** de la política de filtrado experimental usada por la presentación, con opción explícita de override; agregar tests de default, trazabilidad, recompilación e invariantes. No modificar retroactivamente los 12 ensayos anteriores.
3. Revisar que el default solo actúe sobre **visibilidad cartográfica diagnóstica**; mantener estados contractuales P03/P05/P06 y posibilidad de inspección/recuperación manual de excluidos.
4. Validar fuentes históricas, permisos, bloques, capas, unidades y hashes antes de migrar los cinco detalles.
5. Crear plantilla DATRA maestra versionada como **propuesta**, sin sobrescribir la original, sin incorporar postes de ensayos anteriores y sin duplicar el mapa.
6. Ensayar con un fixture y una copia de cada auditoría; comprobar persistencia DWG, atributos del cajetín, legibilidad, compatibilidad con dos SCR, PDF único y regresiones.
7. Generar evidencia de comparativa anterior/posterior de los cinco paneles y registrar los detalles faltantes sin inventarlos.
8. Conservar toda la evidencia privada y seguir usando `verificar_publicacion.py --staged` antes de cualquier push.
9. Documentar las decisiones de diseño o derechos de utilización de recursos CFE no resueltas, sin interpretarlas como aprobación automática.
10. No declarar planos FINAL, CRS acreditado ni PR listo para merge hasta cerrar los gates independientes.

### Riesgos abiertos que A4.2 no debe ocultar

- **Seis excedentes de Mirador** siguen `PENDIENTE_REVISION` bajo el filtro a 300 m; no deben desaparecer de los reportes por omisión.
- **Quince POSTE de Mirador y ocho POSTE de Otay–Florido** quedan sin representación a 300 m; requieren conservar evidencias y eventual revisión de excepciones.
- **Natura conserva 438/438:** 300 m no elimina todos los posibles datos malos y debe evitarse afirmar que los errores de captura han sido resueltos exhaustivamente.
- El contraste INEGI detectó 17 identidades fuera del AGEM candidato entre Mirador/Otay; no equivale a validación de cobertura DATRA.
- Los sectores densos siguen mostrando dificultades perceptibles de anotación aunque el motor no reporte cruces de cajas.
- El mapa y los componentes constructivos del DWG histórico pueden tener escala, unidades, derechos y procedencia diferentes.

## 9. Inventario de referencias y custodia de continuidad

**Repositorio público:** `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe`  
**PR #1:** `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/pull/1`  
**Rama:** `codex/etl-unificado-auditoria-js`  
**Commit de cierre de ensayos:** `be103b436c78ba5cba8d0896d3b00e7c0d131aa7`  
**CI verificada:** `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/actions/runs/42604526678`  
**Directorio versionado de actas:** `AuditoriaCFE/Codex/04_Diagnostico_Presentacion_CAD/A4_1_1_Depuracion_Espacial/`  
**Raíz de lotes privados:** `AuditoriaCFE/auditorias/_comparativa_A4_1_1/`  
**Matriz privada:** `MATRIZ_INCLUSION_EXCLUSION.csv`  
**ZIP evidencial:** `A4_1_1_REVISION_PRIVADA.zip`, SHA-256 `3b4fe1bd7c3dc356e09a8b76bb930a659dc4d2e2dd7b48d1135bdb9015094a1c`  
**PDF seleccionados:** `Natura_A4_1_1_300m.pdf`, `Mirador_A4_1_1_300m.pdf`, `Otay-Florido_A4_1_1_300m.pdf` (el archivo de Mirador recibido para esta revisión tiene sufijo local `(1)`, que no cambia su identidad documental).  
**Fuente territorial:** INEGI AGEM 02004 GeoJSON, SHA declarado `f2d46e03f5843b5443cc89e36d2e15364e8d88ea6d506116a2f6e6521cfa78b2` (hash de la capa original, no del archivo de procedencia ZIP).

**Conservación:** las pruebas privadas y los XLSX fuente no deben agregarse a Git. La carpeta local de evidencia A3 untracked, si continúa existiendo, tampoco debe incorporarse indiscriminadamente. Los históricos permanecen intactos. El presente acta es un documento de decisión y revisión; no constituye evidencia de inspección de campo.

## 10. Dictamen de cierre

**Se aprueba y cierra la estrategia de presentación A4.1/A4.1.1 con radio predeterminado de 300 m.** Las doce variantes permiten comparar el efecto de filtrar microcomponentes y retener íntegra la evidencia de exclusiones. El conjunto seleccionado contiene **1,651 identidades visibles de 1,680 originales**, repartidas en tres PDF A1 horizontales de **16, 10 y 12 hojas**. La aceptación comprende presentación diagnóstica, no validez física de cada activo ni topología de fibra.

**Siguiente checkpoint autorizado: A4.2**, centrado en inventario y recuperación constructiva desde `AuditoriaCFE2.dwg` y las dos referencias PDF, formalización del default 300 m y entrega de una plantilla DATRA maestra verificable. La firma de la plantilla v1.0.0, la ejecución física/manual, la admisión de puntos, la verificación CRS y las conexiones quedan sujetas a sus aprobaciones independientes.

---

**Responsable de decisión:** Owner del proyecto (decisión explícita comunicada el 9 de noviembre de 2026).  
**Preparación del acta:** Revisión técnica asistida, sobre documentación Codex, GitHub, ZIP de evidencias, matriz privada y PDF de 300 m.  
**Publicación recomendada:** versionar el acta **sin incorporar** la matriz, el ZIP, los PDF o datos geográficos privados; antes de publicarla aplicar el guardia de custodia y revisar que las referencias agregadas sean aptas para un repositorio público.
