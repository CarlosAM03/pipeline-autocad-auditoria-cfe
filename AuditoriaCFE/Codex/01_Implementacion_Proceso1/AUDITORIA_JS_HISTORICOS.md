# Auditoría técnica de JavaScript históricos

Estado: **AUDITORÍA COMPLETADA**, 2026-11-04. Extensión autorizada desde `7baa82c`, sin ejecutar MAIN ni generar SCR. Histórico solo lectura; reproducción de funciones en copias aisladas, con fs de escritura bloqueado. No se ejecutó AutoCAD y no se declara equivalencia con la geometría de un DWG.

Hallazgo confirmado por lectura: `ordenar.js:168-188` añade el padre al retorno (`recorrido.push(nodo)`); `trayectoria.js:157-176` realiza preorden sin añadir el padre. La atribución de retornos en TO-BE v0.2 está invertida respecto de estos archivos. Se documentará evidencia ejecutada y propuesta de corrección separada; no se modifica la especificación ni se replica el algoritmo como regla de negocio.

Custodia inicial: `README.md` raíz preexistente sin seguimiento; SHA-256 `3b10e8d9af43da5a1aa2b3e1002b6ed2694efe8bf422d74afa704a434bbcdba5`. Se conserva y no se incluirá en el commit. No hay modificaciones preexistentes a archivos versionados.

## Método ejecutado y huellas

Se leyeron exclusivamente los cinco archivos solicitados de ScriptsHistoricos y los dos TXT de Auditorias. Los CSV de ScriptsHistoricos coinciden en hash con sus referencias de extracción de Auditorias. `tests/audit_js_support.py` copia los cinco a un directorio temporal bajo `AuditoriaCFE/tests/_runtime/`; verifica copia idéntica, carga funciones anteriores a MAIN con `vm` y sustituye require(fs) por lectura exclusiva de las copias y escritura que siempre falla. No se invoca generarSCR, no se guarda texto SCR y no se ejecutan originales. Las copias se retiran al terminar. Los TXT se inspeccionan como texto, jamás mediante SCRIPT.

Reproducción ejecutada con Node **v22.16.0**. Cinco pruebas adicionales están en `test_js_historicos.py`; todas pasaron en la suite de 43. Si faltan fuentes exactas o Node en otra máquina, esa clase informa omisión explícita.

| Archivo relativo al histórico | SHA-256 antes/después (idéntico) |
|---|---|
| ScriptsHistoricos/generar.js | e3b01ad1b510ab14089d2e4e4e257ec8949fa85f1879c7cf4175cdc425af1851 |
| ScriptsHistoricos/ordenar.js | 153027203ab696ba20f06a163f414a8185e135b65a69cab95c8dc007cf86c73c |
| ScriptsHistoricos/trayectoria.js | 51caa4b0e14d547beb46aeaf2afd329cd691b012066d0096d72171d5acb799cc |
| ScriptsHistoricos/STD-MIRADOR.csv | 46c62d0670e715dae2e0b9a4a306e591c2cbf98a066797f6b8d9aa0d5e583a17 |
| ScriptsHistoricos/STD-OTAY-FLORIDO.csv | aa509d2928f9a51133f6b8e25d683411067ba7a1d97ed0cfbfa4c7a08510cf56 |
| Auditorias/STD-MIRADOR.txt | ac90e1e985ae76ed73f62184e800fae0f441cf458014999068d72da 019928133 |
| Auditorias/STD-OTAY-FLORIDO.txt | 5187e030e1f344c322e455bca7c53210cf79b85be2702f7149f2b00f5660942d |

Comando reproducible: `& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe AuditoriaCFE/tests/audit_js_support.py`.

## Extracción, proyección y símbolos

| Evidencia directa | Comportamiento y consecuencia | Tratamiento |
|---|---|---|
| generar.js:90–121; ordenar.js:64–86; trayectoria.js:75–97 | readFileSync completo, split por newline y split por coma. No reconoce comillas ni saltos embebidos. Una ruta entrecomillada con coma desplaza columnas y pierde la fila: prueba sintética devuelve 0 puntos en los tres. Ruta y linaje se ignoran. Cabecera/BOM se toleran incidentalmente al no casar tipo/coordenada. Mirador sin cabecera no pierde su primera fila por un skip automático. | REEMPLAZAR por csv real + extracción OOXML/linaje ya implementados. |
| parseCoord en los tres | Regex no anclada, `[\\d\\.]+`, parseFloat y espacio obligatorio. Omite N/W sin espacio; admite latitud 432.464440; `32..5N 117W` se convierte en 32; admite prefijo/sufijo basura. Soporta signos por hemisferio S/W, sin validar rangos. | REEMPLAZAR por parser estricto Decimal y estados de calidad actuales. No rehabilitar errores para igualar TXT. |
| generar.js:55–62 clasificar | Busca subcadenas; `no-es-un-poste` se clasifica P. Registro se descarta silenciosamente por no casar. | REEMPLAZAR por catálogo exacto actual y FUERA_ALCANCE explícito. Conservar solo intención de tres clases. |
| latLonToUTM, generar.js:24–49 (misma fórmula en los otros) | Elipsoide WGS84 y zona 11 fijos; arco meridiano truncado sin términos completos de e⁴/e⁶; Este hasta A³ y Norte hasta A². No prueba CRS, unidades o área de uso, ni trata hemisferio sur correctamente como UTM sur. | REEMPLAZAR con pyproj y controles P-06 ya implementados. No reutilizar fórmula ni ajustar offset. |
| generar.js:77–85 y 199 | Retiene si existe otro punto a distancia estrictamente menor que 500 m. O(n²). No distingue clase/ruta, ni explica exclusión. Dos puntos co-localizados se salvan mutuamente, aunque sean duplicados o inválidos. | DESCARTAR como filtro. Mantener distancia solo como diagnóstico configurado, sin borrado. |
| generar.js:103–117 y 193–201 | Inventario P/E/C se suma antes del filtro; el conteo anunciado no coincide con los puntos emitidos. No deduplica. | REEMPLAZAR con conteos reconciliados por estado/grupo/admisión de Python. |
| generarSCR:127–181 | UNITS/INSUNITS, capas POSTES(color1), EXCEDENTE(3), CAJAS(5), TEXTO(2); PDSIZE20; PDMODE36/35/34; POINT; TEXT desplazado +3,+3, altura2 y rotación0; etiqueta P/E/C con lat/lon a seis decimales; ZOOM E. | CONSERVAR separación de tipos/capa, unidades explícitas e intención de etiqueta como interfaces; REEMPLAZAR valores/protocolo por perfil verificado, bloques, numeración y etiquetas aprobadas. |

La diferencia medida en latitud 32.5, longitud−117 es **ΔEste=0 y ΔNorte=+11.479314342 m**, frente a EPSG:32611 de pyproj. En el ejemplo Mirador lat 32.52229449/lon −117.02010997, la fórmula produce `498111.3523069956,3598342.172855437`, exactamente el primer POINT del TXT. La magnitud ~11.5 m coincide con el diagnóstico como observación del algoritmo; no constituye una compensación universal ni acredita el DWG.

`PDMODE` y `PDSIZE` son variables guardadas en el dibujo y la regeneración cambia la apariencia de puntos existentes; asignarlas antes de cada POINT no fija una simbología propia por entidad. Véase [PDMODE, Autodesk 2026](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Core/files/GUID-82F9BB52-D026-4D6A-ABA6-BF29641F459B.htm) y [PDSIZE](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Core/files/GUID-826CA91D-704B-400B-B784-7FCC9619AFB9.htm). Además, el prompt Height de TEXT depende del estilo activo; la secuencia literal altura/rotación no es universal ([TEXT, Autodesk](https://help.autodesk.com/view/ACD/2026/ENU/?caas=caas%2Fdocumentation%2FACDLT%2F2014%2FENU%2Ffiles%2FGUID-D1C664DD-63D9-467E-8EC1-2F5A1777A924-htm.html)). No se ensayó su ejecución CAD, idioma ni ploteo.

Faltan controles de UCS/WCS, estilos, bloques, plantilla ya abierta, recursos existentes, anotación, cajetín, layout A1, conteos realmente insertados, permisos de topología y perfil de comandos. `INSUNITS=6` expresa intención métrica del script; no demuestra escala/origen/unidades reales de toda la cartografía. ZOOM E sin control de calidad puede encuadrar posiciones aberrantes. Las etiquetas pierden precisión visible con toFixed(6), no contienen número propio del pipeline ni ruta, y no resuelven solapamientos.

## Retornos, ramas y troncales: verificación directa

**ordenar.js** construye un Map índice→array de vecinos por distancia <120 m (91–110), componentes mediante stack/Set (115–141) y elige un supuesto extremo por máxima suma de distancias al resto del componente (146–162). Es una heurística espacial, no un extremo de campo acreditado. El DFS de 168–189 agrega nodo al entrar **y otra vez al volver de cada hijo** (184). generarSCR serializa todo ese recorrido en una PLINE por componente (196–220), aun para componente de un nodo. Cada arista del árbol DFS se recorre en ambos sentidos; las demás aristas de ciclos del grafo se omiten. No se distingue troncal de ramal ni se calcula longitud real de cable.

**trayectoria.js** incorpora filtro de aislados <1000 m (62–70, llamado en 225); luego usa vecinos <120 m (102–121) y componentes (126–152). ordenarTramo toma el primer nodo de grado 1, o el primero del componente si no hay extremos (157–176). Su DFS agrega cada nodo **solo al entrar**, sin agregar el padre al retorno. generarSCR convierte ese preorden en una PLINE, omitiendo componentes de menos de dos nodos (182–207). Al cambiar de rama puede unir directamente hojas sin arista entre ellas. Son atajos falsos incluso respecto de su propio grafo propuesto.

Fixture de bifurcación con aristas `{0–1,1–2,1–3}`:

- ordenar.js: **0,1,2,1,3,1,0**. Cada transición pertenece al grafo, pero duplica segmentos por retorno.
- trayectoria.js: **0,1,2,3**. La transición 2→3 no es una arista: salta entre ramas.

En los CSV históricos, ordenar tiene 0 transiciones sin arista del grafo de proximidad, pero ese grafo sigue sin autoridad física. trayectoria tiene **13 transiciones sin arista en Mirador y 15 en Otay**. La crítica debe separar la invención del grafo por distancia del error adicional de serializar ramas. La TO-BE v0.2:260 atribuye a trayectoria el retorno al padre; se observa en ordenar, no en trayectoria. **No se implementa la atribución incorrecta ni se modifica la norma:** se presenta propuesta de corrección en PROPUESTA_CHECKPOINTS_CP01_CP04.md. La regla superior sigue siendo dibujar únicamente aristas confirmadas.

| Función / estructura | Reutilización técnica |
|---|---|
| Map/Set, componentes y stack | CONSERVAR concepto para análisis de un grafo con aristas aportadas/confirmadas; separar diagnóstico del dibujo. |
| distancia Euclídea | CONSERVAR operación una vez que puntos comparten CRS métrico acreditado; parametrizar alertas. No usarla como evidencia física ni filtro destructivo. |
| grafo completo de pares a <120 | DESCARTAR como red real automática; si hay futuras propuestas, etiquetarlas no confirmadas y no usarlas en CAD sin validación. |
| extrema por suma o primer grado 1 | REEMPLAZAR por inicios/extremos con autoridad humana P-05. Solo podrían ser sugerencias explícitas. |
| DFS | CONSERVAR como exploración/prueba de componentes; DESCARTAR secuencia DFS como instrucción PLINE. Enumerar aristas/tramos confirmados una sola vez. |
| Troncal/ramal | No existe modelo explícito en esos archivos: comparten capa RUTA. REEMPLAZAR por clasificación declarada y verificada; B06 será alerta, no regla que cambie la red. |
| Mensajes y nombres `_MAPA.scr`, `_RUTA.scr` | REEMPLAZAR por los dos productos aprobados CP-03/CP-04. No adaptar sus MAIN que escriben junto al CSV y se sobrescriben mutuamente `_RUTA.scr`. |

## Contraste cuantitativo con TXT y Python

| Algoritmo reproducido | Mirador | Otay–Florido |
|---|---:|---:|
| CSV histórico, ocurrencias de datos | 551 | 969 |
| generar: parseadas/clasificadas antes del filtro | 550 (P469/E61/C20) | 968 (P745/E200/C23) |
| generar: tras filtro <500 | **533** (P456/E57/C20) | **965** (P742/E200/C23) |
| TXT: POINT / TEXT / PLINE | **533 /533 /0** | **965 /965 /0** |
| Error máximo por posición de secuencia de POINT, fórmula histórica vs TXT | **0 m** | **0 m** |
| Repeticiones tipo+posición entre puntos filtrados, sin deduplicar | 56 | 218 |
| Coordenadas mundialmente imposibles que sobreviven al filtro | 0 | **2** |
| ordenar: parseadas/sin filtro, componentes, vértices del recorrido | 550 /24 /1076 | 969 /16 /1922 |
| trayectoria: tras filtro <1000, componentes, vértices del recorrido | 540 /14 /540 | 966 /13 /966 |
| trayectoria: transiciones sin arista del propio grafo | 13 | 15 |
| Python CP-01 sobre selección histórica sin copia | 494 grupos identificados | 749 grupos identificados |

Los 533/965 son puntos sin deduplicar que sobrevivieron a selección sintáctica y cercanía, **no componentes únicos ni calidad aprobada**. Mirador pierde 1 coordenada N/W sin espacio y17 por el filtro 500; Otay omite Registro por clasificación y3 por el filtro. Las dos latitudes 432 se repiten y se conservan mutuamente por distancia 0. Los TXT no contienen PLINE, así que no prueban cuál de los scripts de trayectoria se aplicó al DWG. No se infiere conectividad ni se inspecciona un DWG para suplir esa ausencia.

El ETL Python ya reemplaza lectura CSV ingenua, interpretación/validación, tipos, exclusión explícita, precedencia, identidad exacta, reportes, comparación maestra/baseline y geodesia con gate. CP-01 aporta ahora filas visibles antes de P-03/P-06. La corrida local Mirador con copia tiene 732 ocurrencias, pero sigue con494 grupos, añadiendo 180 duplicados interpretables y 1 rechazo frente al bloque 551. Otay:969=749 grupos+217 duplicados+2 rechazos+1 fuera de alcance. No se fuerza compatibilidad con inventarios inflados o posiciones erróneas.

## Interfaces propuestas para el futuro generador Python

Propuesta técnica P-09/P-05/P-06/P-10, **no implementada**:

1. `load_prepared(auditoria, manifiesto)` verifica hashes, versión de contrato, 01↔02 por IDs/cardinalidad y controles CRS; 00 solo aporta contexto, nunca habilita dibujo por sí mismo.
2. `validate_template(perfil, recursos_aprobados)` exige DWT abierta, CRS/unidades/UCS, mapa/marco sin duplicación, bloques por tipo y estilos/protocolo del AutoCAD concreto. Reporta precondiciones manuales cuando SCR no pueda verificarlas.
3. `load_confirmed_topology(archivo_versionado, elemento_ids)` exige origen/destino válidos, evidencia/responsable, ruta/tramo y clasificación cuando exista. Falta de aristas permite solo puntos preliminares. No deriva vecinos del orden de Excel ni de 00.
4. `compile_configuration(perfil)` producirá únicamente `01_configurar_plano.scr`: capa/estilo/verificaciones aprobadas, sin insertar puntos, marco ni mapa duplicados.
5. `compile_audit(elementos_admitidos, aristas_confirmadas, presentacion)` producirá únicamente `02_dibujar_auditoria.scr`: un bloque por ID físico, numeración estable independiente de Excel, abreviatura+número+coordenada, aristas únicas sin retrocesos y distancias planas, cajetín/conteos realmente insertados. Sin inferir material ni longitud real de cable.

Pruebas propuestas para esa futura etapa: comandos y prompts del perfil en AutoCAD real; variación de altura fija/estilo; nombres/quotes y recursos sin dependencia de rutas temporales; punto compartido por subrutas con un solo bloque; bifurcación y ciclo con aristas una vez; componentes desconectados sin puentes; ausencia de topología sin líneas; conteos por bloque/etiqueta/distancias y exclusión Registro; CRS no acreditado bloquea geometría; capa y orden de los dos SCR; una A1 legible y ploteo. No se declaran ejecutadas esas pruebas CAD.
