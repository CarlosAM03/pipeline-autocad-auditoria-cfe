# 05. Contrato XLSX a CSV propuesto

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

## Propuesta sujeta a aprobación

Este documento define un contrato; no produce el CSV normalizado ni implementa el extractor. Los originales XLSX son la entrada. Los CSV históricos son controles de extracción y regresión. La especificación TO-BE v0.1 plantea una tabla canónica amplia; el encargo actual precisa separar el CSV mínimo de tres columnas del linaje y la calidad. Se propone conservar el modelo amplio en un lateral, sin perder esos requisitos.

## Familias verificadas y adaptadores mínimos

| Familia | Estructura | Libros |
| --- | --- | --- |
| F1_NOMBRE_ABC | Nombre/elemento/coordenandas completas en A/B/C; D/E numéricos, W positivo. | CFE FLO-OTAY-BOMBEROS.xlsx |
| F2_RUTA_ABC_FOTO_D | Ruta/Elemento de Red/Coordenadas en A/B/C; foto D; auxiliares E:H. | CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx |
| F3_NUMERO_BCD | Numero A; ruta B; tipo C; coordenada D; foto E; auxiliares F:I. Incluye la excepción D1 vacío de Canal 12. | CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx; CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx; CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx; CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx; CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx; Postes_CFE.xlsx |
| F4_DESPLAZADO_BCD | Ruta B; tipo C; coordenada D; foto E; auxiliares F:I. Sin Numero A en Natura. | CFE Natura  - Datra/Natura  - Datra.xlsx |

La familia se determina por encabezados, posiciones y muestras de valores, no por nombre de archivo. Todos los encabezados útiles están en fila 1. El importador deberá reconocer encabezados con espacios finales y grafías verificadas (`Nombre`, `Nombre ruta`, `coordenandas completas`), y bloquear cambios no reconocidos. En Canal 12 D1 vacío se admite únicamente mediante mapeo específico explícito; no se adivinarán columnas arbitrarias. Natura empieza en B y no tiene Numero en A. Las subvariantes de F3 incluyen K/L de resumen, J sin datos operativos, O de fórmulas auxiliares y coexistencia de valores/fórmulas en F:I.

Cada hoja debe reportar su decisión, incluida Sheet2 vacía. Una fila con solo J624=`.` se conserva como metadato no operativo, sin generar elemento. No se descartan candidatos por visibilidad ni duplicados. No se usa max_row, dimensión ni número de imágenes como número de registros.

## CSV objetivo exacto

Encabezado único, obligatorio y en este orden:

```csv
Ruta,Elemento de Red,Coordenadas
```

| Columna | Tipo y regla propuesta |
| --- | --- |
| Ruta | Texto UTF-8. Conservar nombre original; se permite trim exterior únicamente bajo regla aprobada y con original lateral. No cambiar mayúsculas, ortografía ni fusionar similares. Ruta vacía bloquea admisión. |
| Elemento de Red | Dominio exacto propuesto: POSTE, CAJA_EMP, EXCEDENTE. Se cambia expresamente la grafía histórica a códigos controlados. Tipos no aprobados permanecen REVISAR en lateral. |
| Coordenadas | Texto de grados decimales N/W: magnitud positiva de latitud, N, un espacio ASCII, magnitud positiva de longitud, W. Punto decimal; sin separadores de miles ni notación científica. Ejemplo: 32.529070N 116.983918W. |

Codificación propuesta: UTF-8 **sin BOM**; delimitador coma; finales de línea CRLF. CSV con reglas RFC 4180: entrecomillar cualquier campo con coma, comilla o salto de línea; duplicar comillas internas. No añadir índices, comentarios, imágenes, columnas auxiliares ni metadatos a este CSV. El CSV 03 es un documento de mapeo y no es una instancia del CSV objetivo.

Precisión propuesta: interpretar mediante decimal exacto y conservar la escala decimal de cada token fuente, incluidos ceros finales; no imponer seis decimales ni redondear en la extracción. Sustituir solamente espacios sintácticos aprobados. El texto completo original se conserva íntegro aparte. La representación con signo para cálculos futuros es latitud positiva y longitud negativa por W, sin proyectar en esta fase. No usar auxiliares cuya magnitud parezca entera para insertar decimales.

Gramática de admisión propuesta para las fuentes observadas: dos tokens decimales no negativos con punto, seguidos explícitamente por N y W, en ese orden; se podrán tolerar espacios entre tokens o ausencia de espacio solo al aprobar esa regla. Serializar con un espacio único. Falta de hemisferio, `B`, No detectado y rangos imposibles no admiten corrección automática. Casos con signo contradictorio, coma decimal, S/E o sexagesimal no se habilitan por anticipado: se reportan como estructura no aprobada. Límites mundiales: 0≤lat≤90 y 0≤magnitudW≤180. El perímetro esperado debe suministrarse o aprobarse por separado.

### Catálogo de tipos propuesto

| Fuente literal observada | Salida propuesta | Decisión |
| --- | --- | --- |
| poste | POSTE | Aprobar equivalencia |
| cajadedmpalme | CAJA_EMP | Aprobar normalización controlada; conservar typo original |
| excedente | EXCEDENTE | Aprobar equivalencia |
| Registro | Sin salida automática | Definir significado; conservar en REVISAR |

Esta decisión afecta compatibilidad con consumidores que esperan `poste` o `cajadedmpalme`. La comparación de extracción histórica debe usar los textos originales; la comparación de salida canónica requiere la tabla de tipos versionada y aprobada. No perpetuar el typo para evitar decidirlo.

## Selección de fuentes y orden

Proponer un manifiesto explícito de libros y hojas por auditoría, en orden declarado. Dentro de cada hoja, conservar fila original ascendente, incluidas las ocultas. Si el manifiesto no especifica orden de archivos, fallar la ejecución productiva hasta definirlo; para una prueba técnica se podrá declarar expresamente el orden lexicográfico de ruta relativa. No ordenar por latitud, longitud, Numero ni nombre de ruta. No rellenar rutas por arrastre ni coordenadas por media o por fotos.

No incluir a la vez la copia de 181 y el STD de 204 sin decisión de alcance. No tratar FLO-OTAY-BOMBEROS, Natura ni Postes_CFE como rutas unitarias: contienen respectivamente 2, 14 y 70 nombres de ruta. No concatenar todas las fuentes para producir una auditoría general hasta resolver los solapes. El orden de captura conservado no autoriza conexiones entre elementos.

## Linaje y calidad laterales (solo diseño)

Propuesta: `linaje_y_calidad.jsonl`, un objeto por fila candidata, y un manifiesto JSON por lote. No se crean en esta fase. Cada objeto mantendrá al menos:

| Campo lateral | Contenido |
| --- | --- |
| registro_id | Identidad determinista de origen: SHA-256 del archivo + nombre de hoja + fila original; no identifica por sí sola un activo físico. |
| archivo_relativo, hoja, fila_original | Ruta relativa exacta a RAW_XLSX_ROOT, hoja exacta y número Excel desde 1. |
| celdas_originales / valor_original | Valores literales completos por celda, sin trim ni corrección; coordenada_original, ruta_original y tipo_original se conservan explícitamente. |
| tipo_celda, valor_xml, formula_xml, formula_compartida_si, cache | Distinguir texto resuelto, índice sharedString y número literal; retener fórmula y caché sin ejecutarlas; registrar ausencia o error. |
| numero_original, atributos_fuente, referencias_imagen | Numero y otros valores de origen; URI interna OOXML de medio y fila de ancla opcional, sin equiparar a foto certificada. |
| ruta_salida, tipo_normalizado, coordenada_salida | Transformaciones derivadas y versiones de reglas aprobadas, sin sobrescribir originales. |
| estado, motivos, resolucion | VALIDO / REVISAR / RECHAZADO; lista de motivos; decisión humana identificada y fechada. |
| csv_fila_salida | Número físico de salida, contando encabezado en fila 1, o null si no se exporta. |
| orden_fuente / orden_salida | Permitir reconciliar el orden de extracción y cualquier decisión de selección. |

Manifiesto: raíces absolutas declaradas, lista ordenada de fuentes/hojas, tamaño y SHA-256 de cada original, fecha con zona horaria, contrato y reglas versionadas, configuración de ámbito y equivalencias, hash de salidas y resumen por archivo/hoja/ruta/tipo/estado. Preservar cadenas Unicode tal como existen, incluido U+FFFD; cualquier reparación exige regla y evidencia.

La igualdad de coordenadas no identifica el activo ni autoriza eliminarlo. Registrar grupo de duplicado y posición de todas sus ocurrencias; resolver alcance y semántica antes de consolidar. Un activo compartido por dos rutas necesita identidad de negocio adicional.

## Política propuesta de exportación y reconciliación

Exportar solo filas VALIDO o con resolución explícita documentada que las vuelva admisibles. REVISAR y RECHAZADO no desaparecen: permanecen en lateral con csv_fila_salida=null. Un lote con coordenadas sin resolución no se declara apto para entrega final. Generar un subconjunto diagnóstico en una fase futura requeriría etiquetarlo y aprobar alcance.

Invariantes de aceptación futuras: candidatos = VALIDO + REVISAR + RECHAZADO; todas las hojas decididas; cada fila de salida tiene una referencia de linaje; no hay duplicación por columnas auxiliares o anclas; fuentes con SHA-256 inalterado. Comparar ocurrencias, no solo conjuntos únicos. Las cuentas deben separar filas XML, valores, candidatos, aprobados y activos cuando su identidad se defina.

## Requisitos de rendimiento y dependencias

Python estándar (`zipfile`, `xml.etree.ElementTree.iterparse`, `hashlib`, `csv`, `decimal`, `json`, `pathlib`) resulta suficiente para las capacidades verificadas; no se requieren dependencias nuevas ni Excel automatizado. Hacer primero inventario ZIP, luego abrir secuencialmente solo XML de celdas y relaciones. Liberar cada row al terminar; sharedStrings observado ocupa como máximo 375,601 bytes sin comprimir. Registrar y limitar su tamaño, y recurrir a lectura indexada/disco autorizado si un libro futuro lo exige, sin cargar un workbook completo.

Canal 12 requiere recorrer el XML existente para demostrar qué filas tienen contenido, pero no crear 1,048,576 objetos de fila ni iterar rectángulos vacíos con max_row. No usar el último valor conocido de este diagnóstico como corte permanente: una versión futura puede agregar registros. No cargar imágenes ni recalcular fórmulas; usar texto completo y reportar inconsistencias auxiliares. XL/BIFF `.xls` no apareció: una futura entrada .xls debe fallar de forma explícita o usar un adaptador aprobado, no renombrarse a .xlsx.

## Campos necesarios para una fase CAD que Excel no acredita

No hay conectividad desde/hasta, material/propiedad/transformador, especificación técnica completa de cable/herrajes/reservas, responsables/concesionario, logos aprobados ni inicio/fin confirmado. El CRS de la base y la escala de lámina requieren fuentes adicionales. No derivar esos atributos de nombres de ruta ni de similitud geográfica. Su obtención se agenda después, sin análisis CAD en esta fase.

## Pruebas propuestas después de aprobar, sin código en esta fase

Probar las tres muestras del encargo y después todos los libros. Casos mínimos: cabecera D1 ausente, Natura desplazado, Sheet2 vacía, filas ocultas, fila J624 no operativa, fórmula compartida con caché de entero o #VALUE!, tres vacíos intercalados, medios reutilizados, duplicado literal y versiones solapadas, dos rutas en un libro, No detectado, hemisferio incorrecto/ausente y 432.464440N. Medir memoria durante Canal 12 y los libros grandes; documentar un presupuesto antes de fijar un umbral de aceptación. No se ha medido pico RSS en esta fase.
