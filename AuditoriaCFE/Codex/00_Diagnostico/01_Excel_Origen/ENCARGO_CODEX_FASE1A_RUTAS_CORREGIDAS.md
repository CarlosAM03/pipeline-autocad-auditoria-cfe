# Encargo Codex — Auditorías CFE: Fase 1A, auditoría de los archivos XLSX crudos

**Estado:** Encargo de diagnóstico; no autoriza implementación productiva.
**Raíz del espacio de trabajo:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria` (abrir esta carpeta en VS Code/Codex).  
**Entrada fuente (solo lectura):** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`  
**Salida diagnóstica (única ubicación con permiso de escritura):** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen`  
**Fecha de referencia:** 2026-11-03/04.  
**Corrección de alcance:** `AuditoriaCFE` y `Auditorias-20261104T035633Z-1-001` son **directorios hermanos**; `postes` **NO** está dentro de `AuditoriaCFE`. **PROHIBIDO autoconfigurar, adivinar o corregir rutas**: validar exactamente las rutas suministradas y detenerse si alguna falta.

## Rutas exactas y límites del trabajo (OBLIGATORIO)

Definir estas rutas como únicas autoridades para el diagnóstico:

```text
WORKSPACE_ROOT = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria
PROJECT_ROOT   = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE
HISTORY_ROOT   = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001
RAW_XLSX_ROOT  = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes
HISTORY_CAD    = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Auditorias
SPEC_FILE      = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.1.md
ASIS_FILE      = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Reconstruccion_Pipeline_CFE_ASIS_2026-11-03.md
DIAG_OUTPUT    = C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen
```

Árbol relevante:

```text
PipeLineDeAuditoria/                        # raíz que debe abrirse en Codex
├── AuditoriaCFE/                            # proyecto nuevo, SOLO AQUÍ se escriben diagnósticos
│   ├── Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.1.md
│   └── 00_Diagnostico/01_Excel_Origen/      # carpeta que Codex puede crear
└── Auditorias-20261104T035633Z-1-001/      # insumos históricos, SOLO LECTURA
    ├── Auditorias/                         # DWG/PDF y CSV/TXT históricos
    ├── postes/                             # TODOS los XLSX crudos; recorrer recursivamente
    │   ├── CFE Natura  - Datra/
    │   ├── CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/
    │   │   ├── Mirador/
    │   │   └── Otay - Florido/
    │   ├── CFE FLO-OTAY-BOMBEROS.xlsx
    │   └── Postes_CFE.xlsx
    ├── postes.zip                          # NO EXTRAR NI MODIFICAR
    └── Reconstruccion_Pipeline_CFE_ASIS_2026-11-03.md
```

**Preflight obligatorio (antes de inventariar):**
1. Comprobar que `WORKSPACE_ROOT`, `PROJECT_ROOT`, `HISTORY_ROOT`, `RAW_XLSX_ROOT` y `HISTORY_CAD` existen, tienen las relaciones padre-hijo indicadas y apuntan a los directorios **exactos** (sin búsquedas sustitutivas).
2. Verificar que `SPEC_FILE` y `ASIS_FILE` existen; si no, reportar el archivo faltante y **detenerse**, sin crear reemplazos.
3. Confirmar que `RAW_XLSX_ROOT` contiene por lo menos un `.xlsx` de los esperados (p. ej., `Postes_CFE.xlsx` y `CFE FLO-OTAY-BOMBEROS.xlsx`). Si no, detenerse.
4. Asegurar que el directorio de salida creado/resuelto se encuentre **dentro de `PROJECT_ROOT`** y **fuera de `HISTORY_ROOT`**, teniendo en cuenta symlinks/junctions; si no se puede verificar, detenerse.
5. No ejecutar `git init`, no cambiar directorios de trabajo ni crear archivos temporales dentro de los XLSX o de `HISTORY_ROOT`. Usar la salida autorizada para los reportes.

**Regla de lectura:** descubrir libros mediante búsqueda recursiva exclusivamente bajo `RAW_XLSX_ROOT`. Leer `STD-MIRADOR.csv` y `STD-OTAY-FLORIDO.csv` (ambos ubicados en `HISTORY_CAD`) exclusivamente desde `HISTORY_CAD`. Los PDF, DWG y TXT de `HISTORY_CAD` se pueden usar como contexto de solo lectura, pero **la Fase 1A no los analiza ni los modifica**. Leer los dos documentos de contexto en las rutas exactas indicadas. No inspeccionar otras carpetas del escritorio, de `Datra` o de `CFE`.

**Regla de escritura:** únicamente los siete entregables listados más adelante, bajo `DIAG_OUTPUT`. Para todos los reportes, usar rutas relativas a `RAW_XLSX_ROOT` cuando se registre el origen de un XLSX y señalar la raíz explícitamente en los encabezados. No escribir nada en `HISTORY_ROOT`.

## Objetivo y distinción obligatoria

La **entrada real** del futuro pipeline son los **libros Excel XLSX originales** de levantamiento de infraestructura. Los XLSX pueden contener fotografías, formatos dispares, columnas auxiliares, fórmulas, múltiples rutas y espacios vacíos con formato. Los archivos `STD-MIRADOR.csv` y `STD-OTAY-FLORIDO.csv` (ambos ubicados en `HISTORY_CAD`) son **resultados históricos ya normalizados**; sirven para comparar el **contrato de salida objetivo** y realizar regresión, **nunca** para deducir que los originales son CSV ni para reemplazar el análisis de los XLSX.

El pipeline futuro será XLSX crudos (uno o varios) → extracción y limpieza auditables → modelo de datos intermedio y CSV normalizado → validación de topología → dos scripts `01_configurar_plano.scr` y `02_dibujar_auditoria.scr`. **En esta fase examinar únicamente las fuentes XLSX y la especificación XLSX→CSV.** No realizar aún proyección geográfica, generación de scripts CAD, reconstrucción de DWG/DWT ni trazado de rutas.

El propósito de esta primera fase es obtener **evidencia verificable** para diseñar un importador simple y robusto para todos los libros de `RAW_XLSX_ROOT`, que se reutilizará para las tres nuevas auditorías y, preferentemente, para regenerar la auditoría general y las dos rutas históricas.

## Muestras ya revisadas (contrastar con archivos locales, no asumir que representan a todos)

Estos hallazgos provienen de una inspección de estructura OOXML, en modo lectura, de tres XLSX compartidos:

| Muestra | Tamaño observado | Registros de datos con valores | Fotos internas | Estructura |
|---|---:|---:|---:|---|
| `CFE FLO-OTAY-BOMBEROS.xlsx` | 25 KB aprox. | 494 (más encabezado) | 0 | A `Nombre`, B `elemento`, C `coordenandas completas`, D `Coordenadas N`, E `Coordenadas W` |
| `ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx` | 9.0 MB aprox. | 44 (más encabezado) | 45 | A `Ruta`, B `Elemento de Red`, C `Coordenadas`, D `Foto`; E–H auxiliares; 176 celdas con fórmulas |
| `Ruta canal 12 level antes 2014 Completo.xlsx` | 111 MB aprox. | 347 (más encabezado) | 606 | A `Numero`, B `Ruta`, C `Elemento de red`, D coordenada completa (encabezado D1 no poblado), E `Foto`; F–I auxiliares; 324 celdas con fórmulas |

Puntos específicos:
- El archivo FLO-OTAY-BOMBEROS **mezcla dos rutas**: 287 registros `RUTA flo-otay FO96` y 207 registros `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran`; son 494 postes en esta muestra. No inferir `archivo = ruta`.
- La muestra Vía Rápida contiene 38 postes, 5 excedentes y 1 caja de empalme (`cajadedmpalme`).
- La muestra Canal 12 contiene 331 postes, 14 excedentes y 2 cajas (`cajadedmpalme`).
- **Peligro de rendimiento:** en Canal 12, `xl/worksheets/sheet1.xml` registra **1,048,576 filas** por el área/formato de hoja, pero solamente **348** filas tienen valores y el último registro con valor está en la fila 351. No interpretar `max_row` ni dimensiones de Excel como cantidad de registros; evitar procesar imágenes y millones de filas como si fueran datos.
- Las columnas auxiliares de coordenadas pueden derivar de fórmulas y presentar representaciones o precisiones diferentes. Conservar el valor original completo y contrastar explícitamente los auxiliares; **no confiar ciegamente en números que parecen coordenadas sin separador decimal**.
- Las fotografías no forman parte del CSV objetivo: registrar su existencia y, solo si es útil, una referencia a hoja/fila/imagen; no es necesario descomprimir cada imagen ni cargarla en memoria para procesar datos.

## Contrato CSV histórico de referencia

`STD-OTAY-FLORIDO.csv` en `HISTORY_CAD` usa encabezado `Ruta,Elemento de Red,Coordenadas` y filas como:

```csv
Ruta,Elemento de Red,Coordenadas
ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72,poste,32.529070N 116.983918W
```

`STD-MIRADOR.csv` en `HISTORY_CAD` contiene las mismas tres clases de datos pero **no tiene encabezado**. Ambas son variantes de salida histórica, no razones para perpetuar inconsistencias. Proponer un único CSV normalizado de tres columnas (con encabezado y codificación/convenciones explicitadas) y un **registro de linaje y calidad aparte**. El tipo observado `cajadedmpalme` requiere normalización controlada, sin perder el texto fuente. No reproducir valores geográficos defectuosos simplemente porque figuren en los CSV anteriores.

## Restricciones obligatorias

1. **Solo lectura** en toda la carpeta original. Prohibido modificar, abrir/guardar con reparación, sobrescribir, renombrar o mover XLSX, imágenes, DWG, PDF, CSV, TXT, ZIP, logs u otros originales.
2. Crear archivos nuevos únicamente bajo `DIAG_OUTPUT` (ruta absoluta definida arriba). No escribir código de producción, no generar CSV normalizado definitivo, SCR, DWG ni DWT durante esta fase.
3. No extraer `postes.zip` (unos 500 MB) si `RAW_XLSX_ROOT` ya existe. Comparar solo el inventario de nombres si hay sospechas de fuentes faltantes.
4. No descomprimir todas las imágenes. Primero usar metadatos del ZIP XLSX (archivo OOXML) para contar medios, relaciones/drawings y su tamaño. Si se requiere relación imagen→fila, inspeccionar anclas de dibujo de forma limitada y documentada.
5. Usar **procesamiento de memoria acotada** para XLSX grandes. Separar inventario OOXML (ZIP + XML streaming) de lectura de celdas. No cargar simultáneamente libros completos ni confiar en `max_row` como límite efectivo para iteración ingenua. Se permite usar herramientas de lectura segura y solo lectura según conveniencia y disponibilidad local.
6. No ejecutar macros ni enlaces externos, no descargar nada, no compartir datos fuera de la máquina; no instalar dependencias grandes sin autorización.
7. Preservar nombre exacto del archivo, hoja, número de fila, valor original de coordenadas, ruta y tipo. No imputar coordenadas ni deduplicar sin reglas explícitas.
8. Tratar nombre de ruta y tipo de elemento como datos de origen; no fusionar rutas por similitud de nombres sin una tabla de equivalencias aprobada.
9. Distinguir **hecho comprobado**, **inferencia** y **regla pendiente de validar**; cada conteo debe indicar su criterio (filas XML vs filas con valor vs registros válidos).
10. No iniciar la implementación productiva por cuenta propia. Parar al entregar diagnóstico y propuesta de contrato para la Fase 1B.

## Tareas secuenciales

### 1. Inventario local de XLSX
- Detectar recursivamente todos los `.xlsx` y `.xls` en `RAW_XLSX_ROOT`, sus rutas relativas, tamaños, hash SHA-256 cuando sea viable, y hoja(s). Detectar originales idénticos y posibles versiones con nombres similares.
- Identificar libros particularmente grandes y por qué: fotografías, otras partes del ZIP, exceso de filas formateadas, etc.
- Verificar si aparecen casos que no estén en las tres muestras previas, especialmente `Postes_CFE.xlsx`, `Natura - Datra.xlsx` y los libros restantes de Mirador y Otay–Florido.

### 2. Perfil por libro y hoja
Para cada hoja, determinar:
- Encabezados **reales**, posiciones, filas inicial/final **con valores** y filas vacías intercaladas; cantidad de registros candidatos.
- Relación de columnas con: ruta, tipo de elemento, coordenada completa, N/W auxiliares, identificador, orden/numero, fotografías, fórmulas, observaciones y otros atributos disponibles.
- Tipos reales de celda y fórmulas relevantes; valor original literal vs valor calculado, indicando cuando no está disponible caché de fórmula.
- Conteo de imágenes (medios + anclas) sin cargarlas ni extraerlas todas; si una misma fila tiene varias, documentar.
- Diversidad de nombres de ruta y de categorías de elemento; variantes, errores ortográficos y valores no reconocidos.
- Cardinalidad de registros con campo de coordenadas, vacíos, patrones no estándar, rangos imposibles y duplicados exactos **sin modificar nada**.

### 3. Comparación de estructuras y mapeo
- Agrupar los XLSX por **familias de esquema** verificadas (no forzar un esquema universal basado solo en nombre de archivo).
- Construir una tabla `archivo,hoja,columna_fuente,campo_destino,transformacion,confianza,ejemplo`, con `Ruta`, `Elemento de Red`, `Coordenadas` como salida histórica mínima.
- Identificar reglas compartidas vs adaptadores específicos para encabezados desplazados, celdas vacías, imágenes, fórmulas, varios libros por ruta, varias rutas por libro.
- Identificar cualquier dato que sea necesario en el dibujo CFE pero que **no esté presente** en Excel; no inventarlo.

### 4. Calidad y trazabilidad
- Diseñar categorías `VALIDO`, `REVISAR`, `RECHAZADO` y motivos para errores de coordenadas, tipo desconocido, ruta vacía, duplicado o campos inconsistentes.
- Definir cómo conservar el linaje: `archivo_relativo,hoja,fila_original,valor_original` y, en un manifiesto, hash del archivo.
- Diferenciar CSV objetivo simple de un CSV/JSON lateral para incidencias y metadatos; especificar encabezado, UTF-8, formato de coordenadas N/W, separador, escape de comas y regla de orden de filas.
- Investigar si el orden de filas del Excel refleja levantamiento / trayectoria real. **No asumir** que el orden de captura prueba conectividad y no realizar aún inferencia de topología.

### 5. Validación contra salidas históricas
- Comparar los campos y algunos registros de cada fuente candidata con `STD-MIRADOR.csv` y `STD-OTAY-FLORIDO.csv` (ambos ubicados en `HISTORY_CAD`), citando ruta, archivo, hoja y fila; priorizar casos donde el origen pueda identificarse sin ambigüedad.
- Determinar hasta dónde puede reconstruirse el XLSX→CSV histórico; registrar coincidencias, exclusiones y discrepancias **sin atribuir causas no demostradas**.
- Documentar qué CSV de 2026 resulta útil como prueba de regresión para cada familia de Excel y qué cobertura falta para `AuditoriaCFE` general.

## Entregables obligatorios — solo diagnóstico

Crear exclusivamente bajo `PROJECT_ROOT` (no bajo `HISTORY_ROOT`):

```
AuditoriaCFE/
  00_Diagnostico/
  01_Excel_Origen/
    01_inventario_xlsx.md
    02_perfiles_hojas.md
    03_familias_y_mapeo_columnas.csv
    04_calidad_y_anomalias.md
    05_contrato_XLSX_a_CSV_propuesto.md
    06_regresion_con_csv_historicos.md
    07_checkpoint_para_aprobacion.md
```

En `07_checkpoint_para_aprobacion.md` incluir:
1. Total de archivos, hojas, registros y medios analizados, con metodologías de conteo.
2. Familias de esquema identificadas y requisitos mínimos del importador.
3. Recomendación de cómo manejar eficientemente los XLSX de 100–200 MB y el caso de un millón de filas formateadas, manteniendo dependencias mínimas.
4. Contrato exacto propuesto de las **tres columnas del CSV objetivo**, preservando linaje y calidad en documentos laterales.
5. Resultados de comparación con CSV históricos, sin suponer equivalencia total.
6. Lista breve de decisiones pendientes: clasificación de tipos, rutas equivalentes, duplicados, tratamiento de coordenadas inválidas, orden de ruta y demás reglas de negocio.
7. Siguiente paso implementable tras aprobación: prototipo del **extrac­tor XLSX→CSV**, con pruebas de las tres muestras y después todos los originales. **No escribir ese prototipo en esta fase**.

## Criterio de finalización

Al terminar, entregar un resumen ejecutivo con 5–10 hallazgos prioritarios, rutas exactas de los siete archivos producidos, límites de lo inspeccionado y decisiones que requieren aprobación. **Detenerse.** No abordar aún análisis CAD, DWT, planos, trayectorias, limpieza productiva o nuevas auditorías.
