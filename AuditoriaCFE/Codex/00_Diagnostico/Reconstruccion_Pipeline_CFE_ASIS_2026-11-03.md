# Auditorías CFE — Reconstrucción documental del pipeline existente (AS-IS)

**Versión:** 0.1 — checkpoint técnico, sin cambios de arquitectura ni de reglas de negocio  
**Fecha de corte:** 3 de noviembre de 2026  
**Ámbito:** infraestructura aérea de fibra óptica (postes, cajas de empalme, excedentes) y preparación de planos para AutoCAD convencional.  
**Estado:** reconstrucción sustentada en historial del proyecto, inspección de CSV y scripts TXT, y revisión visual del PDF de referencia. **No es una certificación de exactitud de los DWG entregados.**

## 1. Objetivo y límites del checkpoint

Documentar cómo se llegó desde registros operativos en Excel hasta la representación en AutoCAD, precisar qué transformaciones se han usado y qué etapas no están automatizadas. Esta versión **no** rediseña el proceso, **no** implementa la generación de nuevas auditorías y **no** altera las decisiones históricas sin revisión con el responsable del proceso.

Conforme al historial reportado: se han entregado tres planos/auditorías, una de la infraestructura completa y dos de rutas añadidas. Se requieren tres auditorías adicionales para tres ampliaciones, dos de las cuales reciben más de un archivo de fuente. Las entregas previas no están disponibles aquí como DWG para inspección.

## 2. Evidencia disponible

| Evidencia | Contenido comprobable | Limitación |
|---|---|---|
| Cuatro conversaciones históricas: *Representar Excel en AutoCAD*, *Representar coordenadas en AutoCAD*, *Auditoría CFE AutoCAD*, *Plano de rutas Tijuana* | Decisiones y problemas de importación, georreferenciación, Map 3D → AutoCAD convencional, scripts de puntos, trayectorias y ramas | No constituye un repositorio versionado de scripts y resultados |
| `STD-MIRADOR.csv` | 554 filas físicas, 3 vacías; registros con nombres de ruta, tipo y coordenadas N/W; **no tiene encabezado** | No es el Excel original ni muestra todas sus columnas |
| `STD-OTAY-FLORIDO.csv` | 970 filas, una cabecera y 969 registros; tres nombres de subruta y varios tipos | No es el Excel original |
| `STD-MIRADOR.txt` | 533 comandos POINT, 533 etiquetas TEXT y capas | Archivo de comandos CAD, no código fuente del generador; **sin PLINE** |
| `STD-OTAY-FLORIDO.txt` | 965 comandos POINT, 965 etiquetas TEXT y capas | Archivo de comandos CAD, no código fuente del generador; **sin PLINE** |
| `PlantillaAuditoriaCFE.pdf` | Ejemplo visual A1: mapa, simbología, tabla, distancias, detalles, orientación, cajetín | El ejemplo pertenece a otra zona (Nezahualcóyotl) y no es una especificación validada de las tres auditorías |
| `Hallazgos_Checkpoint_CFE_2026-11-03.csv` | 29 filas de revisión puntual, con referencia al CSV y fila física | Informe de comparación, no corrección de la fuente |

**No disponibles:** los Excel crudos que dieron origen a estos CSV, el script generador original (.py/.js u otro), los tres archivos DWG entregados, el DWG/DWT de plantilla y un registro verificable de aceptación/revisión final de CFE. No se debe afirmar que esas partes se han auditado documentalmente.

## 3. Línea de tiempo reconstruida

1. **Septiembre–octubre 2025.** El alcance inicial fue trasladar información de postes documentada en hojas de cálculo/Google Earth a planos DWG, utilizando rutas, ubicación y coordenadas. El Excel original incluía además referencias de fotos y placas; se priorizaron los postes y sus coordenadas. Hubo un intento de importar CSV con `MAPIMPORT` en AutoCAD Map 3D, pero el selector de columnas no permitió la importación esperada. Se investigaron otras rutas, incluidos scripts `.scr` con `POINT`.
2. **Octubre 2025.** Se identificó la diferencia entre coordenadas geográficas en grados decimales y coordenadas planas en metros. La referencia elegida para Tijuana fue WGS84 / UTM zona 11N (EPSG:32611). Se migró el enfoque hacia AutoCAD convencional. El dibujo de puntos y etiquetas se consiguió visualizar, pero se documentaron ajustes pendientes de posición, escala/marco, simbología y líneas.
3. **Abril 2026.** Se trabajó sobre dos agrupaciones CSV: `STD-MIRADOR` y `STD-OTAY-FLORIDO`. Se generaron instrucciones de CAD que crean capas, puntos y etiquetas; se experimentó con ordenar trayectorias y conectar nodos. El usuario reportó saltos y trayectorias erróneas, por lo que se separó expresamente la fase de puntos de la de líneas. Se solicitó la regla de revisión espacial de 800 m, pero no hay una implementación de topología final verificable.
4. **Noviembre 2026.** Se abre este checkpoint de recuperación antes de procesar tres ampliaciones nuevas, con archivos múltiples para dos de ellas.

## 4. Pipeline existente observado (AS-IS)

```text
Excel operativo crudo
     │  (no disponible para auditar su estructura real)
     ▼
Selección/filtrado de filas y columnas por ruta y elemento
     │  (existe resultado; no se conserva implementación de origen)
     ▼
CSV intermedio: ruta, tipo, coordenadas geográficas N/W
     │
     ▼
Lectura + parsing + validación/filtrado parcial
     │  (no completamente determinista ni con reporte de descarte)
     ▼
Clasificación P / C / E + proyección hacia coordenadas planas
     │
     ▼
Texto de comandos AutoCAD: UNITS, INSUNITS, -LAYER,
     │                       PDMODE, PDSIZE, POINT, TEXT, ZOOM
     ▼
Ejecución en AutoCAD convencional mediante .SCR
     │
     ▼
Puntos georreferenciados y etiquetas por tipo
     │
     ▼
Ajustes manuales de mapa/plano y formato final
     │   (pasos exactos y DWG finales no disponibles)
     ▼
DWG entregado (3 según informe del responsable)
```

**La trayectoria principal, ramificaciones, cotas interpostales y llenado de la plantilla NO forman parte de los dos scripts TXT verificados.**

## 5. Matriz de etapas, cobertura y brechas

| Etapa | Insumo → salida | Cobertura actual verificable | Estado |
|---|---|---|---|
| 0. Recepción y custodia | Excel original → fuente conservada | Está documentada históricamente la recepción; archivos Excel originales ausentes en el checkpoint | Histórica / sin evidencia de automatización |
| 1. Selección de alcance | Excel → registros de rutas, postes, cajas, excedentes | Los dos CSV muestran el resultado de la selección; no es posible reconstruir el filtro exacto sobre las columnas originales | Resultado existente; lógica no recuperada |
| 2. Normalización de esquema | Columnas heterogéneas → tres columnas | CSV presentes; uno sin cabecera y otro con ella, por lo que aún no hay contrato único | Parcial |
| 3. Estandarización de tipo | `poste`, `excedente`, `cajadedmpalme` → P/E/C | Las etiquetas y capas hacen esa clasificación; `Registro` no se representa | Implementada para tres tipos; incompleta |
| 4. Parsing de coordenadas | Texto N/W → latitud y longitud numéricas | Se observa conversión N/W a longitud negativa y etiquetas decimales; hay formatos problemáticos y casos descartados | Parcial |
| 5. Reglas de calidad | Registros → válidos/anómalos | Existen omisiones compatibles con filtrado, y se solicitó umbral 800 m; no hay bitácora de descartes ni validación exhaustiva | Parcial, no auditable |
| 6. Proyección | Lat/lon → Este/Norte plano | Los TXT contienen magnitudes UTM zona 11N; discrepancia de ~11.5 m en Norte vs referencia EPSG:32611 | Operativa, requiere verificación |
| 7. Generación CAD | Registros proyectados → POINT/TEXT y capas | Los dos archivos TXT lo hacen | Implementada y recuperable |
| 8. Reconstrucción topológica | Nodos desordenados → secuencia y ramas | Hubo propuestas y pruebas, sin resultado aceptado verificable | Pendiente |
| 9. Trayectoria y distancias | Nodos ordenados → PLINE y cotas | 0 comandos PLINE/LINE en los TXT | No implementada en los artefactos verificados |
| 10. Maquetación | Geometría → marco, escala, norte, tablas, simbología y cajetín | Existe PDF de referencia; no hay automatización visible ni DWG del marco | Manual / por comprobar |
| 11. Verificación y entrega | DWG → plano aceptado | Entregas reportadas; no se incluyen reportes de conteo ni DWG finales | Resultado histórico, verificación no reproducible |

## 6. Esquema intermedio real

Los CSV almacenan **tres valores** por registro: `Ruta`, `Elemento de Red`, `Coordenadas`. `STD-OTAY-FLORIDO.csv` trae ese encabezado; `STD-MIRADOR.csv` comienza directamente con los datos, por ejemplo:

```csv
STD HACIA CNAL 12,cajadedmpalme,32.52229449N 117.02010997W
```

El generador interpreta `32.52229449N` como latitud positiva y `117.02010997W` como longitud negativa. Clasificación de los archivos TXT:

| Tipo del CSV | Capa CAD | Color de capa documentado | Etiqueta |
|---|---|---:|---|
| `poste` | `POSTES` | ACI 1 | `P(lat,lon)` |
| `excedente` | `EXCEDENTE` | ACI 3 | `E(lat,lon)` |
| `cajadedmpalme` (grafía histórica) | `CAJAS` | ACI 5 | `C(lat,lon)` |
| Texto de todas las entidades | `TEXTO` | ACI 2 | Etiqueta a 3 m Este y 3 m Norte del punto |

`PDMODE` cambia por tipo de punto (`36`, `35`, `34`, respectivamente), `PDSIZE=20`; los archivos usan `INSUNITS=6` (metros), altura de texto 2 y `ZOOM E` al final. No se generan identificadores P1/P2 secuenciales: se preserva la geografía en etiquetas redondeadas a seis decimales. En los TXT **no se almacena el nombre de la ruta en la entidad CAD** ni se crean capas distintas para cada subruta.

Ejemplo extraído del primer TXT: coordenada `32.52229449N 117.02010997W` aparece con coordenadas CAD aproximadas `X=498111.3523, Y=3598342.1729` y etiqueta `C(32.522294,-117.020110)`.

**Criterio de compatibilidad:** estos son comandos de AutoCAD convencional. Los ficheros se entregaron con extensión `.txt`; para ejecutarlos mediante el comando `SCRIPT` deben guardarse/renombrarse como `.scr` conservando contenido y saltos de línea aceptados por la versión usada. La versión exacta de AutoCAD no está comprobada.

## 7. Inspección cuantitativa de los artefactos

| Métrica | Mirador | Otay–Florido |
|---|---:|---:|
| Registros de datos no vacíos | 551 | 969 |
| Filas de cabecera | 0 | 1 |
| Filas vacías | 3 | 0 |
| Postes declarados en CSV | 470 | 745 |
| Excedentes declarados en CSV | 61 | 200 |
| Cajas de empalme declaradas en CSV | 20 | 23 |
| Otros tipos (`Registro`) | 0 | 1 |
| Puntos `POINT` encontrados en TXT | **533** | **965** |
| Etiquetas `TEXT` encontradas en TXT | 533 | 965 |
| Postes encontrados en TXT | 456 | 742 |
| Excedentes encontrados en TXT | 57 | 200 |
| Cajas encontradas en TXT | 20 | 23 |
| Registros del CSV no representados en TXT | **18** | **4** |
| Comandos de polilínea `PLINE` | **0** | **0** |

Los registros omitidos no implican automáticamente errores de la entrega: podrían incluir datos intencionalmente descartados por calidad, pero **no hay constancia individual del motivo**. La bitácora CSV anexa referencia los 29 registros con omisión, blanco o anomalía espacial relevante.

### Agrupaciones de ruta que hoy conviven en cada archivo

- **Mirador:** `STD HACIA CNAL 12` (204 registros) y `Ruta canal 12 level antes 2014` (347 registros).
- **Otay–Florido:** `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` (44), `RUTA flo-otay FO96` (622), `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` (303).

Por tanto, **un archivo CSV no equivale necesariamente a una sola ruta o una sola trayectoria continua**. Es especialmente importante para las dos próximas ampliaciones que estarán distribuidas entre varios archivos fuente.

### Otros hallazgos

1. En **Mirador** la primera fila contiene `11702014028W` (longitud sin separador decimal) y no aparece en el TXT. La fila física 80 contiene coordenadas N/W sin espacio (`32.52417096N117.03452398W`) y no aparece en el TXT. Hay 18 omisiones totales y tres filas vacías.
2. En **Otay–Florido** dos filas de excedente (físicas **242** y **648**) contienen `432.464440N 116.863542W`, fuera del intervalo válido de latitud, y **sí se representaron** en el TXT con Norte cercano a **48,032,635 m**, contaminando `ZOOM E`.
3. En **Otay–Florido** dos filas de poste (**135** y **540**) repiten `32.476223N 116.485650W`; también aparecen en el TXT. Se ubican muy lejos de la concentración principal y requieren validación contra fuente, no eliminación automática.
4. El criterio de «ningún poste aislado a más de 800 m», propuesto en el historial, **no basta por sí solo**: dos errores duplicados pueden estar a distancia cero entre ellos y pasar una prueba de vecino próximo. Es necesario además revisar rango y agrupación de ruta.
5. Hay duplicados exactos de triples *(ruta, tipo, coordenada)*: **58 repeticiones adicionales** en Mirador y **218** en Otay–Florido. No se debe aplicar `drop_duplicates` indiscriminadamente: las coincidencias entre tipos distintos y registros redundantes requieren semántica de activos y revisión.
6. **Proyección:** en etiquetas geográficamente plausibles de ambos TXT, comparar las coordenadas proyectadas contra WGS84→UTM 11N (EPSG:32611), con el redondeo de las etiquetas, produce una diferencia sistemática aproximada de **+11.5 m en Y/Norte**, mientras X/Este coincide dentro del redondeo. Esto es un **hallazgo por investigar**, no una autorización para desplazar automáticamente el dibujo ni para reproyectar planos entregados. Deben compararse el generador original, el sistema de coordenadas de la base cartográfica y un punto de control real.

## 8. Diferenciar procesamiento de datos y dibujo

### Transformaciones de datos que ya se observan

- Reducción del Excel operacional a los campos que consume la representación (a través de CSV intermedio).
- Selección y agrupación de rutas (con varias subrutas en cada conjunto).
- Interpretación de coordenadas geográficas N/W y cambio de signo Oeste → longitud negativa.
- Categorización en P, C y E, conservando atributos textuales de coordenadas a precisión gráfica.
- Obtención de coordenadas cartesianas compatibles con un entorno CAD en metros (sujeta a verificación geodésica).
- Generación textual de instrucciones reproducibles `POINT` y `TEXT`, capas y encuadre por extensión.

### Procesos todavía no probados como automatizados

- Leer cualquier Excel heterogéneo sin preparación previa y generar un CSV canónico con trazabilidad completa.
- Hacer limpieza verificable sin omitir filas silenciosamente, corrección fiable de coordenadas y manejo definido de duplicados.
- Consolidar varios Excels/CSV sin perder archivos, subrutas, IDs o filas origen.
- Ordenar puntos por trazado real, determinar inicio/fin, distinguir troncal y ramas; comparar longitudes de nodos y regresar a bifurcaciones según la lógica histórica solicitada.
- Generar polilíneas con segmentos correctos, distancias interpostales, numeración por secuencia e indicadores de ramificación.
- Aplicar la plantilla final en un layout acotado y escalado, incluyendo simbología, tabla y cajetín, y exportar el DWG/entregable final sin interacción manual.

## 9. Estado del layout/plantilla

La plantilla PDF es una lámina visual con: marco del plano, mapa de fondo/calles, ruta de fibra, postes numerados y distancias, tabla de coordenadas, simbología, orientación, mapa llave, resúmenes de estructura, ficha de cable, detalles constructivos y bloque de firmas/responsables. **Los TXT verifican solo una parte inicial: elementos puntuales y anotaciones.** La inclusión del marco y del resto de componentes se hizo fuera de estos scripts o sigue pendiente de comprobar.

La plantilla contiene nombres y datos ilustrativos de Nezahualcóyotl. **No replicar** sus cantidades, distancias, responsables, coordenadas ni concesionario en una auditoría de Tijuana. Su texto dice «grados decimales» junto a números de aspecto UTM; esto no sustituye una definición de CRS.

## 10. Reglas de operación que NO quedan aprobadas automáticamente

Requieren validación del responsable antes de reconstruir el ejecutor para las nuevas ampliaciones:

1. ¿Qué filas entran en la auditoría y qué se hace con los elementos distintos de poste/caja/excedente, por ejemplo `Registro`?
2. ¿Qué errores de coordenadas se pueden corregir con certeza, cuáles requieren revisión humana y cuándo se permite excluir un registro?
3. ¿La ruta tiene identificador único por subruta y/o existe una numeración de postes de origen que deba conservarse?
4. ¿Cuál es la fuente de verdad para el recorrido y sus ramas: un orden de captura de campo, un trazo existente, una secuencia de postes, o solamente coordenadas?
5. ¿El mapa base y el DWG existente usan realmente EPSG:32611 y qué punto de control se utilizará para despejar el desplazamiento Norte observado?
6. ¿Qué campos exige CFE en la lámina final y cuáles provienen de la plantilla en lugar del Excel?

**No debe inferirse la topología de una red solamente ordenando latitud y longitud ni uniendo por el vecino más cercano.** Esa estrategia produjo las líneas con saltos que se descartaron históricamente.

## 11. Checkpoint propuesto para reutilizar lo existente, sin reescritura inmediata

**Congelar como referencia:** los cinco archivos fuente del proyecto y los tres entregables históricos si se recuperan, sin modificar su contenido. Mantener las versiones TXT actuales como evidencia, no tratarlas como fuente de verdad cartográfica.

**Recuperar antes de modificar:** a) un Excel crudo de una auditoría ya hecha; b) el generador real que produjo `STD-MIRADOR.txt` y `STD-OTAY-FLORIDO.txt` (si existe); c) un DWG satisfactorio y su plantilla/base cartográfica; d) la versión concreta de AutoCAD.

**Prueba mínima de regresión previa a las ampliaciones:** procesar un dataset ya conocido y verificar que conteos, clasificación y posición reproduzcan el dibujo aceptado; además, registrar filas rechazadas, discrepancia de proyección y duplicados, sin cambios silenciosos.

**Evolución mínima posterior, sujeta a la reconciliación:** una entrada por auditoría que acepte una lista de archivos Excel/CSV, una tabla canónica con trazabilidad (`archivo`, `hoja`, `fila`, `ruta`, `tipo`, `lat`, `lon`, `Este`, `Norte`, `estado`) y la salida de comandos CAD. Mantener el trazado de trayectorias y maquetación como módulos o etapas opcionales hasta estar verificados. Esto describe una dirección para discusión, **no es arquitectura aprobada**.

## 12. Criterio de cierre de esta fase

Se considera cerrada la **reconstrucción documental preliminar AS-IS** cuando se conserve este documento, el inventario de artefactos y el registro de anomalías. Se considera cerrada la **reconciliación técnica completa** solamente al comprobar con al menos una auditoría histórica el Excel original → generación TXT/SCR → ejecución AutoCAD → DWG, incluyendo las razones de exclusión y el CRS real. No es necesario rehacer el dibujo si el archivo final anterior permite usarlo como control de regresión.

## Apéndice A. Huellas SHA-256 de evidencia local

```text
7623af1db238f8bf6af8fca525e54dd3f3a2efdee63d9a2bb0f3a5fab29977da  PlantillaAuditoriaCFE.pdf
46c62d0670e715dae2e0b9a4a306e591c2cbf98a066797f6b8d9aa0d5e583a17  STD-MIRADOR.csv
aa509d2928f9a51133f6b8e25d683411067ba7a1d97ed0cfbfa4c7a08510cf56  STD-OTAY-FLORIDO.csv
ac90e1e985ae76ed73f62184e800fae0f441cf458014999068d72da019928133  STD-MIRADOR.txt
5187e030e1f344c322e455bca7c53210cf79b85be2702f7149f2b00f5660942d  STD-OTAY-FLORIDO.txt
```

## Apéndice B. Fuentes de la reconstrucción

- Conversaciones históricas disponibles en el contexto del proyecto: representación desde Excel, elección de proyección y alternativas de `MAPIMPORT`/SCR, ajuste del plano convencional y recuperación de trayectorias.
- Dos CSV, dos TXT y plantilla PDF adjuntos al proyecto.
- Comparación automatizada local realizada para este checkpoint: recuentos de comandos, etiquetas, clasificación, cotejo registro-a-etiqueta, comprobación de datos fuera de ámbito y contraste numérico de proyección con `pyproj`.

**Nota de responsabilidad:** los resultados describen datos y archivos, no constituyen una aprobación de reglas de operación de CFE ni de exactitud geodésica para permisos.
