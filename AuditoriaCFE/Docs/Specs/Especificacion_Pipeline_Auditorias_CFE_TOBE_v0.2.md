# Auditorías CFE / DATRA — Especificación funcional y técnica del pipeline TO-BE

| Campo | Valor |
|---|---|
| Versión | **0.2 — consolidación previa a la plantilla CAD** |
| Fecha | 2026-11-04 |
| Estado | **Especificación de implementación propuesta, alineada con decisiones aprobadas; verificaciones técnicas aún abiertas** |
| Autoridad de decisiones | `AuditoriaCFE/Docs/ADRs/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md` |
| Versión anterior | `AuditoriaCFE/Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.1.md` |
| Evidencia de diagnóstico | `AuditoriaCFE/Codex/00_Diagnostico/` |
| Alcance | XLSX originales → CSV normalizado → CSV proyectado a CAD y topología validada → **dos SCR** → DWG y PDF A1 tras revisión |
| Próximo hito | **Fase 3: recuperación y construcción de la plantilla canónica DATRA**. Esta especificación no declara la plantilla terminada ni autoriza por sí sola la implementación. |

> **Precedencia documental:** ante cualquier contradicción, prevalecen las decisiones aceptadas en ADR-000. Las opciones nuevas de esta versión son propuestas técnicas, no sustituciones silenciosas de reglas de negocio. El histórico AS-IS y los JavaScript se conservan como evidencia de regresión, no como fuente de verdad geográfica o topológica.

## 1. Objetivo y definición de terminado

Construir una herramienta **local y reproducible** para elaborar auditorías de infraestructura aérea CFE para DATRA. Cada ejecución selecciona **una carpeta de auditoría** con uno o más XLSX originales, procesa sus elementos, registra exclusiones y duplicados, obtiene geometría cartográfica validada y genera únicamente los dos scripts que se ejecutan manualmente sobre una **plantilla base DATRA editable** ya abierta en AutoCAD convencional.

La ejecución satisfactoria debe ofrecer **cuatro artefactos principales de evidencia**, sin contar controles auxiliares:

1. `01_elementos_normalizados.csv`: **unificación/deduplicación** de coordenadas geográficas válidas, con el contrato mínimo aprobado `Ruta,Elemento de Red,Coordenadas`.
2. `02_elementos_proyectados.csv`: las mismas entidades únicas dibujables, ya convertidas a coordenadas **Este/Norte del CRS CAD aprobado** y acompañadas de identificadores estables para el dibujante.
3. `01_configurar_plano.scr`: ajuste y verificación del dibujo abierto desde la plantilla DATRA.
4. `02_dibujar_auditoria.scr`: inserción de símbolos, numeración, etiquetas, relaciones topológicas **confirmadas** y campos variables de la lámina.

La preparación genera además los reportes necesarios para el **`summary.csv`**, el linaje de ocurrencias, incidencias y topología. Estos archivos auxiliares **no son ejecuciones adicionales en AutoCAD**. El DWG y PDF A1 se guardan/exportan después de revisión humana en CAD; no se presentan como productos creados automáticamente fuera de ese entorno.

**Aclaración terminológica:** la conversión de coordenadas es a una *zona cartográfica UTM* (hipótesis EPSG:32611), **no a una zona horaria**. El CRS no queda aprobado hasta verificar el mapa DWG y puntos de control.

## 2. Alcance y gobierno

### 2.1 Auditorías

- Prioritarias: `Natura`, `Mirador`, `Otay-Florido`.
- Complementaria: `Tijuana-General`, inicialmente **solo** desde `Postes_CFE.xlsx`; una variante consolidada con ampliaciones verificadas se creará después y se distinguirá explícitamente.
- Una auditoría equivale a un contexto de ejecución y **una sola lámina A1 horizontal**, aunque contenga diferentes subrutas, libros, tramos o componentes desconectados.
- El plano individual muestra la **ruta completa actualizada**. La comparación con maestro y con una línea base histórica sirve **solo para información del summary**, no para omitir elementos del plano.

### 2.2 Exclusiones de alcance

- No se necesita cloud, backend, BD, UI gráfica, Map 3D, importación `MAPIMPORT` ni procesamiento de fotografías para la geometría.
- `Registro` corresponde a infraestructura **subterránea**, fuera de esta auditoría CFE; se registra como exclusión de alcance, no como error.
- No se inventan material del poste, transformadores, propiedad, longitudes reales de cable ni datos empresariales no acreditados.
- No se imputa ni corrige especulativamente una coordenada; no se dibujan aristas por mera proximidad.

### 2.3 Entradas inmutables y versiones

Los XLSX originales (con fotos, fórmulas, filas ocultas, esquemas heterogéneos y rangos sobredimensionados) son **solo lectura**. Registrar archivo relativo, SHA-256, hoja, fila, valor original, tipo y subruta. La prioridad entre versiones se determina por un **orden de fuentes explícito y reproducible**, pendiente de cerrar en P-01; no utilizar automáticamente fecha de modificación. Una copia antigua que se coloque en `entrada/` se procesa y se compara, sin duplicar entidades.

## 3. Organización real del repositorio y convención operativa

La raíz local del repositorio es:

```text
C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\
├── .gitignore
├── Auditorias-20261104T035633Z-1-001/       # histórico externo al proyecto, SOLO LECTURA, ignorado por Git
│   ├── Auditorias/                            # DWG/PDF/CSV/TXT históricos
│   ├── postes/                                # XLSX originales
│   ├── postes.zip
│   └── ScriptsHistoricos.zip
└── AuditoriaCFE/                              # proyecto versionado
    ├── Codex/00_Diagnostico/                  # diagnóstico ya ejecutado, versionable
    ├── Docs/ADRs/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md
    ├── Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.2.md
    ├── recursos/                              # FUTURO: DWT, mapa, bloques y recursos aprobados
    │   ├── Plantilla_Auditoria_CFE_Tijuana.dwt
    │   └── Mapa_Tijuana_Vectorial.dwg
    ├── auditorias/                            # FUTURO: carpetas seleccionables por CLI
    │   ├── Natura/
    │   │   ├── entrada/                       # originales copiados sin alterarlos; Git ignora el contenido
    │   │   ├── configuracion.json             # alcance/precedencia/baseline; contenido por aprobar
    │   │   ├── topologia_confirmada.csv        # si existe, vínculos revisados; NO es salida generada
    │   │   └── salida/                        # datos/SCR/reportes/DWG/PDF generados; Git ignora todo
    │   ├── Mirador/...
    │   ├── Otay-Florido/...
    │   └── Tijuana-General/...
    └── preparar_auditoria.py                 # FUTURO: CLI local y módulos, aún sin implementar
```

**No trasladar archivos históricos al árbol de código ni editar fuentes de `Auditorias-20261104T035633Z-1-001/`.** La estructura futura dentro de `AuditoriaCFE/` es convención de implementación; puede crearse por etapas. Los archivos de configuración y topología **se versionan fuera** de `entrada/` y `salida/`.

### 3.1 Uso esperado de la CLI

1. Buscar carpetas de auditoría bajo `AuditoriaCFE/auditorias/` (no explorar otras carpetas del escritorio).
2. Listarlas por nombre y permitir seleccionar una opción; disponer también de argumento CLI no interactivo para pruebas.
3. Enumerar recursivamente XLSX de la `entrada/` elegida, exhibir nombres y número antes de procesarlos, y respetar la precedencia aprobada.
4. Ejecutar ETL y reportar totales, duplicados, excluidos y coordenadas a revisar; producir CSV y `summary`.
5. Solo si el CRS del mapa está verificado, producir la proyección; solo dibujar **rutas** que cuenten con topología confirmada. Se permite generar dibujo preliminar de **puntos válidos** si faltan conexiones.
6. Generar los dos SCR y señalar **PRELIMINAR/REVISAR** cuando corresponda; no declarar entrega definitiva por la ejecución de la CLI.

## 4. Contratos de los cuatro archivos principales

Los nombres a continuación son propuestos para fijar interfaces. Su estructura detallada queda sujeta a aprobación en el contrato ETL P-09 sin alterar el mínimo de tres columnas de ADR-000.

### 4.1 `01_elementos_normalizados.csv` — salida de 1A

Archivo UTF-8 con encabezado y CSV escapado correctamente:

```csv
Ruta,Elemento de Red,Coordenadas
STD HACIA CNAL 12,POSTE,32.52229449N 117.02010997W
```

La fila es **ilustrativa de formato**, no certificación de que esa coordenada sea un poste específico. La salida contendrá exclusivamente **entidades admitidas, geográficamente interpretables y únicas de la auditoría**. Los tipos canónicos nuevos son `POSTE`, `CAJA_EMP` y `EXCEDENTE`; un modo de exportación histórica puede representar `poste`, `cajadedmpalme` y `excedente` para regresión, pero no es el contrato principal.

Reglas:
- Dos ocurrencias con **mismo tipo normalizado + coordenadas normalizadas exactamente iguales** dentro de la auditoría representan un candidato duplicado; conservar una sola entidad, salvo excepción acreditada para equipos diferenciados por ID confiable.
- Duplicados de archivo/versiones y filas se preservan **en el linaje**, no se representan dos veces ni se pierden sin explicación.
- Coordenadas cercanas distintas generan advertencia, **no** fusión automática; una caja y un poste co-localizados no se fusionan.
- Conservar precisión de entrada; no usar `toFixed(6)` ni redondeos como clave de identidad.
- La comparación contra `Postes_CFE.xlsx` sucede **después** de consolidar la auditoría y no cambia las filas dibujables.
- Errores irrecuperables, registros fuera de ámbito y elementos fuera de alcance quedan trazados en el reporte lateral, con el estado apropiado.

### 4.2 `02_elementos_proyectados.csv` — salida cartográfica de 1B/1C

Este CSV **no reemplaza** al archivo geográfico de tres columnas: es un producto adicional consumido por el generador de SCR. Contrato técnico propuesto:

```csv
elemento_id,ruta_id,tipo,latitud,longitud,este_m,norte_m,crs
<id>,<ruta>,POSTE,32.52229449,-117.02010997,<E>,<N>,EPSG:32611
```

La fila usa marcadores `<E>/<N>` deliberadamente: los valores solo podrán emitirse **tras la verificación del CRS de la base CAD**. `elemento_id` es determinista y enlaza con la tabla de linaje y las aristas, sin depender exclusivamente de una coordenada redondeada. `tipo` pertenece al dominio aprobado; latitud/longitud decimales son valores numéricos y en AutoCAD se envía `X=Este`, `Y=Norte`.

- Proyectar **una sola vez**, con biblioteca geodésica estándar (preferencia técnica: Python `pyproj`, verificación obligatoria contra puntos de control).
- WGS84/UTM zona 11N (`EPSG:32611`) sigue siendo **hipótesis**. El `crs` usado debe registrarse explícitamente junto al lote y concordar con el DWG.
- No copiar la fórmula UTM abreviada de los JS históricos ni sumar/restar un desplazamiento artificial de aproximadamente 11.5 m.
- Si no se verifica el CRS, emitir diagnóstico y **no** entregar un CSV cartográfico rotulado como validado.
- El archivo mantiene cardinalidad y correspondencia 1:1 con las entidades exportadas a dibujo del CSV normalizado, excepto cambios de aptitud espacial explícitamente justificados en incidencia y marcados como preliminares.

### 4.3 `01_configurar_plano.scr` — primer script ejecutado en CAD

**Precondición:** dibujo NUEVO abierto a partir de `Plantilla_Auditoria_CFE_Tijuana.dwt`, que ya contiene el marco, el mapa vectorial de Tijuana, su presentación A1 y los recursos estáticos DATRA/CFE.

Responsabilidades:
- Verificar el estado del dibujo, unidades en metros, UCS/WCS, orientación, capas, estilos, bloques, espacio modelo y layout A1.
- Asegurar que el mapa base y el marco estén presentes **sin insertarlos una segunda vez**; configurar propiedades necesarias para el dibujo.
- Ajustar solo configuraciones reproducibles y compatibles con comandos de AutoCAD convencional y su idioma probado. Si una verificación no se puede realizar de forma fiable con un `.scr` puro, declararla como **precondición comprobada o control manual** y no fingir automatización.
- Evitar `ZOOM EXTENTS` indiscriminado si hay puntos aberrantes. No ejecutar `MAPIMPORT`.
- **No insertar postes o rutas en este script.**

### 4.4 `02_dibujar_auditoria.scr` — segundo script ejecutado en CAD

Responsabilidades:
- Insertar **un símbolo de bloque por entidad física única**, de acuerdo con `tipo`, con atributos/etiquetas de **abreviatura, número generado y coordenada**.
- Numeración determinista del plano independiente del número de Excel. Prever distribución de textos para reducir colisiones sin eliminar información obligatoria.
- Dibujar troncales y ramificaciones **solo a partir de conexiones confirmadas**; distinguir componentes desconectados y no volver sobre un ramal trazando falsamente la misma arista.
- Presentar distancias **planas entre postes efectivamente conectados** y no confundirlas con longitud física real de cable.
- Llenar campos variables del título y resumen impreso de **POSTE, CAJA_EMP y EXCEDENTE** con conteos realmente dibujados; excluir `Registro`.
- Ajustar la visualización del layout sin alterar las coordenadas geográficas y sin crear láminas A1 adicionales por decisión unilateral.
- Producir dibujo **PRELIMINAR** cuando falten datos o conexiones; no afirmar aprobación automática ni exportación PDF sin pasar por CAD.

**Secuencia inalterable:** DWT abierta → Script 01 → Script 02 → revisión visual → guardar DWG → exportar PDF A1.

## 5. Archivos auxiliares obligatorios y estados

La evidencia de cuatro productos principales **no sustituye** la trazabilidad interna:

| Recurso auxiliar sugerido | Función / contenido mínimo |
|---|---|
| `summary.csv` | Registro por componente único o incidencia verificable con ruta/subruta, tipo, estado, conteo/flag de novedad frente a línea base y coincidencia informativa con maestro. El **esquema final está pendiente (P-09)**. |
| `linaje_y_calidad.csv` o `.jsonl` | Una entrada por ocurrencia de origen con archivo/hoja/fila/hash, valor crudo, interpretación, ID prevalente, estado (`VALIDO`, `REVISAR`, `RECHAZADO`, `DUPLICADO`, `FUERA_ALCANCE`) y motivo. |
| `reporte_incidencias.csv` | Coordenadas imposibles, discrepancias auxiliares, posiciones remotas, duplicados candidatos, ID conflictivos, errores de lectura; referencia al origen. |
| `asociaciones_elemento_ruta.csv` | Relación entre `elemento_id` y cada subruta a la que pertenece, para conservar **todas** las asociaciones de un poste compartido aunque se dibuje una sola vez. |
| `topologia_propuesta.csv` | Conexiones candidatas por análisis espacial y sus motivos, marcadas **NO CONFIRMADAS**; no permitir que el dibujante las trate como definitivas. |
| `topologia_confirmada.csv` | Archivo de **entrada/configuración** de aristas validadas con pares de `elemento_id`, pertenencia de ruta, tramo y orden cuando aplique; mantiene la autoridad humana. |
| `resumen_conteos.csv` o resumen equivalente | Conteos de ocurrencias, únicas, duplicadas, excluidas, revisables, dibujadas y desgloses de postes/cajas/excedentes; se reconcilian con dibujo y tabla A1. |
| `manifiesto_ejecucion.json` | Archivos de entrada y hashes, versiones de programa/dependencias, CRS, advertencias, configuración y resultados para reproducción. |

**Política de calidad:** A07 permite seguir y generar preliminar con elementos válidos aunque existan coordenadas inválidas, siempre con incidencia específica en `summary`. La política de liberación **final** sigue abierta (P-04). La comparación con maestro y la detección de “nuevo” respecto a una auditoría anterior **son ejes distintos**: su línea base histórica sigue pendiente P-02.

## 6. Etapas del proceso 1: preparación fuera de AutoCAD

### 6.1 ETL 1A — XLSX originales → `01_elementos_normalizados.csv`

1. Inventario de archivos seleccionados, esquema de cada hoja y precedencia determinista, sin abrir libros con reparación ni procesar fotografías.
2. Extracción mediante lectura en memoria acotada de celdas con contenido real, incluso filas ocultas; no confundir `max_row` con registros.
3. Mapeo de las cuatro familias de esquema halladas en Fase 1A; conservar ruta, tipo, coordenada completa, N/W auxiliares cuando existan, ubicación exacta de fuente y posibles IDs.
4. Parseo N/S/E/W completo y estricto; recuperación mediante N/W auxiliares solo si inequívoca (A08), sin reescrituras especulativas de números.
5. Normalización de tipos; `Registro` fuera de alcance; valores desconocidos a revisión.
6. Comprobación de rango mundial y ámbito geográfico local (P-03), duplicados exactos, duplicados cercanos, excepciones con ID acreditado.
7. Deduplicación local por fuente prioritaria (A04–A06), conservación integral del linaje y tablas de conteos.
8. Exportación reproducible a UTF-8 de CSV mínimo y reportes; después comparación informativa con maestro y baseline histórica si está disponible.

**Restricciones:** no deduplicar entre auditorías como prohibición de dibujado; no ordenar según latitud/longitud para suponer trayectorias; no descartar silenciosamente elementos aislados.

### 6.2 Topología y geodesia 1B — preparación espacial

1. Verificar mediante CAD el sistema de referencia, unidades, origen, orientación, escala y puntos de control contra la base Tijuana; hasta entonces `EPSG:32611` es hipótesis.
2. Proyectar lat/lon al CRS aceptado y producir `02_elementos_proyectados.csv`.
3. Mantener **grafo de infraestructura distinto de la lista de entidades**. Solo `POSTE` constituye estructura de soporte por defecto; asociar cajas/excedentes sin convertirlos en conectores físicos sin respaldo.
4. Obtener sugerencias espaciales para extremos, troncales y ramales; conservar alertas de distancia y componentes separados. La distancia no acredita una arista.
5. Exigir topología confirmada para producir **polilíneas finales**. Sin ella, permitir SCR preliminar de puntos, no inventar rutas.
6. Calcular distancias planas de aristas acreditadas y advertir sobre tramos inverosímiles, ciclos y ramas; la regla “troncal con más postes” solo es diagnóstico.

### 6.3 Generación 1C — CSV proyectado/topología → dos `.scr`

- Generar exactamente los dos scripts operativos de las secciones 4.3 y 4.4, más reportes asociados.
- Mantener los comandos CAD dentro de perfiles reproducibles (idioma, unidades, variables, estilos y bloques). Probar secuencias completas con AutoCAD 2026/instalación real antes de liberar.
- No incluir en el script rutas absolutas de la máquina de desarrollo si un recurso relativo/versionado funciona; configurar rutas de soporte sin sobrescribir historia.
- No generar entidades múltiples para duplicados; una misma entidad puede recibir conexiones de varias subrutas.

## 7. Proceso 2: presentación CAD desde plantilla canónica

La plantilla **se construye una vez**, se mantiene como recurso aprobado y está **abierta antes** de ejecutar scripts de una auditoría. La apertura de la DWT es una acción del operador, no un tercer script.

- **Model Space:** mapa base vectorial Tijuana y componentes en coordenadas planas reales (metros), separando capas de mapa, clases de elementos, troncal, ramales, cotas y anotaciones.
- **Paper Space:** **una sola lámina A1 horizontal (841 × 594 mm)** con marco CAD de auditorías Mirador/Otay–Florido adaptado a DATRA, composición próxima a la plantilla PDF CFE, simbología aplicable, tabla de elementos, orientación, zona cartográfica y cajetín editable.
- **Símbolos:** bloques por categoría, no dependencia de `PDMODE` como identificación por entidad. `POSTE` sin material usa símbolo genérico provisional; evitar afirmar material.
- **Información visible:** identificador de componente abreviado, número generado, coordenada y, para líneas validadas, distancia planar; resumen de postes, cajas y excedentes únicos. Otras estadísticas exclusivamente en summary interno.
- **No inferir elementos constructivos:** solo añadir detalles de cable/herrajes si hay respaldo de aplicación real; no trasladar ubicación, responsables o cantidades del ejemplo de otra ciudad.
- **Regla A1:** si todas las etiquetas no caben de forma legible, emitir incidencia de diseño y solicitar revisión. No ocultar etiquetas obligatorias ni crear páginas adicionales sin nuevo ADR.
- **Entregas:** revisar geometría y texto, guardar DWG y producir PDF A1 desde AutoCAD; el generador de CSV/SCR por sí mismo **no** produce un DWG final validado.

## 8. Fase 3 inmediata — recuperación y aprobación de la plantilla DATRA

**Objetivo:** crear una base CAD editada y reutilizable que permita a cada auditoría comenzar con el mapa y marco correctos, sin repetir configuración manual.

**Insumos autorizados, solo lectura:**
- `Auditorias-20261104T035633Z-1-001/Auditorias/Auditoria-STD-MIRADOR.dwg`
- `Auditorias-20261104T035633Z-1-001/Auditorias/Auditoria-STD-OTAY-FLORIDO.dwg`
- `Auditorias-20261104T035633Z-1-001/Auditorias/AuditoriaCFE.dwg` (comparativo, si aporta recursos)
- `Auditorias-20261104T035633Z-1-001/Auditorias/PlantillaAuditoriaCFE.pdf` (referencia visual, **no** editable)
- `ADR-000`, esta especificación y diagnóstico Codex (sin modificar fuentes).

**Inspección requerida antes de editar CAD:**
1. Inventario comparativo de `Model Space` / `Paper Space`, layouts, tamaños de papel, capas, bloques, textos/atributos, estilos, tablas, referencias externas e imágenes enlazadas; revisar si falta algún recurso para abrir correctamente.
2. Determinar dónde están realmente el **mapa vectorial de Tijuana** y el **marco DATRA existente**, evitando atribuir a un DWG contenido que solo está en una referencia externa no disponible.
3. Verificar unidades, escala, UCS/WCS, orientación, coordenadas de al menos **dos puntos de control no coincidentes**, origen de la cartografía y CRS. Si no se puede acreditar, documentar el bloqueo: no asumir EPSG:32611 por el aspecto de números UTM.
4. Seleccionar justificadamente el DWG donador del mapa y el del marco (pueden ser distintos), conservando copias inmutables de originales.
5. Reconstruir/depurar recursos editables: capa mapa, geometría estática, estilos, bloques de postes/cajas/excedentes, identificaciones, A1, marco, cajetín y tablas sin valores ficticios.
6. Crear `AuditoriaCFE/recursos/Mapa_Tijuana_Vectorial.dwg` y `AuditoriaCFE/recursos/Plantilla_Auditoria_CFE_Tijuana.dwt`, con una sola referencia activa del mapa (embebido o XREF administrada), y abrir en una instalación AutoCAD de prueba.
7. Validar ploteo A1, apertura sin archivos faltantes, no duplicación del mapa, edición de cajetín, visualización de un conjunto pequeño de puntos de control y espacio útil para etiquetado.

**Criterios de aceptación de fase 3:**
- DWT crea dibujo nuevo con marco y mapa reutilizables sin posicionamiento manual, en A1 horizontal.
- El mapa se sitúa en el sistema de coordenadas documentado y no requiere corrección arbitraria de 11.5 m.
- El plano está separado correctamente entre geometría modelo y presentación de papel.
- Existen bloques editables/aplicables para clases aprobadas y campos del cajetín DATRA sin valores inventados.
- `01_configurar_plano.scr` queda especificado contra recursos de plantilla verificados, no contra suposiciones.
- Se registra cualquier limitación que impida una sola hoja A1 legible, para decidir antes de declarar versión canónica final.

**No ejecutar aún los scripts de producción ni insertar las rutas completas durante esta etapa.** Una prueba pequeña de recursos/coordenas es suficiente para aprobar la base; la generación ETL 1A/1B/1C inicia tras el encargo correspondiente a Codex.

## 9. Revisión de código histórico: aprendizaje reutilizable, no trasplante

Tres archivos recuperados `generar.js`, `ordenar.js`, `trayectoria.js` y los CSV normalizados `STD-MIRADOR.csv`, `STD-OTAY-FLORIDO.csv` explican parte de las salidas 2026:

| Hallazgo técnico observado | Tratamiento nuevo |
|---|---|
| `generar.js` clasifica `poste/excedente/cajadedmpalme`, interpreta N/W y emite `-LAYER`, `POINT`, `TEXT`. | Conservar intención y pruebas históricas; migrar parsing/validación y generación SCR a Python con contratos separados y bloques CAD. |
| `generar.js` descarta aislados por vecino menor a **500 m**, sin informe por registro. | **No** filtrar ni omitir por distancia en silencio. Los aislados son alerta, no exclusión automática. |
| `parseCoord` exige un espacio entre coordenadas y no valida límites geográficos. | Parser tolerante a separadores inequívocos, validador geográfico estricto y trazabilidad del error. |
| `latLonToUTM` usa una fórmula aproximada/truncada, asociada a error sistemático Norte cercano a **+11.5 m** frente a la transformación EPSG:32611. | Usar biblioteca geodésica validada y puntos de control; **no** reutilizar esa fórmula ni aplicar compensaciones ciegas. |
| Cambios de `PDMODE` antes de cada `POINT`. | `PDMODE` es variable global, no símbolo independiente por poste; reemplazar con **bloques CAD**. |
| CSV leído con `split(',')`; se ignora el primer campo en ciertos recorridos. | Usar lector CSV real; preservar ruta, ID y procedencia. |
| `ordenar.js` construye grafo por distancia menor a **120 m**, usa componentes y DFS sin separación robusta entre ramificaciones. | Reutilizar estructuras de grafo como técnica, pero con **aristas confirmadas**; no asumir conectividad por vecindad. |
| `trayectoria.js` vuelve al nodo padre dentro de una sola `PLINE`. | Mantener DFS **solo como algoritmo de exploración**, no como secuencia dibujable con retrocesos artificiales. Dibujar aristas/tramos independientes sin duplicar segmentos. |
| Los scripts de trayectoria consumen coordenadas de todos los tipos sin modelar adecuadamente la estructura de soporte. | Construir red entre postes y relaciones explícitas para cajas/excedentes. |

**Compatibilidad:** se conservan pruebas de extracción y conteos históricos para demostrar que los nuevos rechazos/omisiones tienen **motivo**. **No** exigir que los nuevos SCR sean byte a byte iguales a los históricos: esas salidas contenían anomalías y símbolos/recorridos insuficientes. El análisis de código se incorpora aquí como **restricción técnica de implementación**, sin agregar un documento autónomo ni modificar el ADR-000.

## 10. Pruebas de aceptación y trazabilidad de etapas

| Prueba | Condición mínima |
|---|---|
| ETL reproducible | Mismos XLSX + orden de fuentes/configuración + versión → mismos CSV y reportes, sin modificar fuentes. |
| Heterogeneidad XLSX | Cuatro familias, varias hojas, imágenes, fórmulas, filas ocultas y millones de filas XML no bloquean o disparan carga de medios. |
| Integridad por ocurrencia | Cada fila operativa clasificada y explicada: aceptada, duplicada, fuera de alcance, rechazable o revisable; sin descartes silenciosos. |
| Deduplicación | Exactitud tipo+coordenada sin redondear y excepción documentada de caja multi-equipo; un símbolo por entidad física única. |
| Contraste maestro | El summary informa presencia/diferencia frente a `Postes_CFE.xlsx`; nunca excluye del plano individual por existir en el maestro. |
| Delta histórico | “NUEVO” solo contra baseline declarada; si falta baseline se expresa **NO DETERMINADO**, no se infiere a partir del maestro. |
| Geodesia | Transformación estándar al CRS aprobado, puntos de control verificados, sin desviación heredada de UTM abreviado. |
| Topología | Sin aristas aprobadas no se dibujan líneas físicas; ramas y desconexiones no producen saltos ni retrocesos falsos. |
| SCR 01/02 | Se ejecutan en ese orden sobre DWT probada, sin pasos CAD adicionales ni dependencias ocultas. |
| Una hoja A1 | Etiquetas por componente + tabla de tres tipos legibles; si es imposible se reporta, no se alteran reglas sin autorización. |
| Entrega | DWG guardado y PDF ploteado a A1 tras revisión; los conteos coinciden con elementos CAD realmente insertados. |
| Git / custodia | Se versionan código, Docs y diagnósticos; no se versionan XLSX operativos, ZIP históricos ni salidas generadas de auditorías. |

## 11. Decisiones aún abiertas (remisión a ADR-000)

No se asume que estén aprobadas por estar documentadas en esta especificación:

- **P-01** precedencia determinista de archivos (primer archivo analizado).
- **P-02** baseline histórica para marcar nuevo/existente.
- **P-03** perímetro geográfico y política de ubicaciones remotas.
- **P-04** criterio de liberación final ante incidencias abiertas.
- **P-05** mecanismo para validar inicios/extremos y aristas/rutas sin documentación formal.
- **P-06** elección del DWG donador, comprobación del CRS y resolución geográfica (**bloquea la plantilla canónica y la proyección**).
- **P-07** datos DATRA y detalles constructivos aprobados del cajetín.
- **P-08** legibilidad de auditorías extensas en una sola hoja A1.
- **P-09** esquema exacto de summary/linaje y formato de exportaciones.
- **P-10** perfil verificado de AutoCAD 2026, idioma, comandos y ploteo.
- **P-11** discrepancia de conteos históricos de duplicados Mirador 56/58, por definición de clave y ámbito.

### Pendientes que afectan específicamente al hito inmediato (fase 3)

`P-06` y `P-10` deben resolverse mediante inspección/ensayo del DWG y AutoCAD. `P-07` y `P-08` definen la composición final A1. **No** adelantar una DWT supuestamente aprobada antes de esas comprobaciones. Las decisiones P-01/P-02/P-09 pueden cerrarse al diseñar las pruebas del ETL posterior.

## 12. Secuencia de trabajo y límites de autorización

| Hito | Estado | Resultado |
|---|---|---|
| 1. ADR-000 y reglas A/B/C/D | **Cerrado documentalmente** | Decisiones base aprobadas, con pendientes específicos identificados. |
| 2. Análisis de JS/CSV históricos | **Realizado en conversación** | Algoritmos útiles, errores y pruebas de regresión; sin documento independiente. |
| **3. Plantilla canónica DATRA** | **Siguiente, pendiente** | Inspección DWG, selección de recursos, verificación CRS, mapa y marco DWT A1 reutilizables. |
| 4A. Codex — ETL | Pendiente de encargo | XLSX→CSV canónico + resumen/linaje. |
| 4B. Codex — geometría/red | Pendiente, después de 4A y CRS | CSV proyectado + topología propuesta/confirmada. |
| 4C. Codex — CAD | Pendiente, después de DWT | Dos scripts SCR; pruebas en AutoCAD, DWG/PDF. |

**No autorizar etapas 4A/4B/4C por inferencia a partir de esta especificación.** Cada implementación requerirá un encargo delimitado con sus criterios de aceptación y las decisiones aplicables. No modificar archivos históricos sin permiso.

## 13. Control de cambios de v0.1 a v0.2

- Se incorporan como **aprobadas** las decisiones ADR-000 A01–A14, B01–B07, C01–C10, D01–D02 y ARQ-01–ARQ-15.
- Se cambia la deduplicación de “solo reportar” a **una entidad única dibujable por componente**, con todas las ocurrencias conservadas en el linaje.
- Se fija la operación desde plantilla **ya abierta** y el orden obligatorio de los dos SCR; no se insertará dos veces el mapa.
- Se agregan formalmente las **cuatro evidencias principales**: CSV normalizado, CSV proyectado, SCR 01 y SCR 02.
- Se delimita `summary.csv` como registro interno de cambios/comparaciones/incidencias, pendiente de esquema definitivo.
- Se incorporan aprendizajes verificables de JavaScript 2026: eliminación silenciosa de aislados, UTM abreviada, `PDMODE` global, grafo por umbral y DFS con falsos retornos.
- Se actualizan carpetas a la **estructura real** con `AuditoriaCFE/Codex/`, `AuditoriaCFE/Docs/` y raíz Git `PipeLineDeAuditoria`.
- Se convierte la **recuperación de la plantilla canónica** en el próximo hito, antes del encargo de código.

---

**Fin de la especificación TO-BE v0.2.**
