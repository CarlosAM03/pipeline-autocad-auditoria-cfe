# 07. Checkpoint para aprobación

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

## Estado del encargo

Fase 1A documental terminada. Este checkpoint solicita decisiones para una fase futura y no autoriza ejecutarla. No se implementó ETL, no se produjo CSV normalizado de elementos ni se generaron CAD/SCR/DWG/DWT. Los siete documentos son la única salida.

## Totales y criterio

| Métrica | Total | Definición |
| --- | --- | --- |
| Archivos XLSX / XLS | 9 / 0 | Recursión solo en RAW_XLSX_ROOT |
| Hojas / con candidatos / vacías | 10 / 9 / 1 | Definidas en workbook.xml |
| Filas XML | 1,058,886 | row físicos, incluidos formatos vacíos |
| Filas con valores | 7,053 | Al menos una celda con valor o caché no vacío |
| Candidatos | 7,043 | Algún valor de ruta/tipo/coordenada después de cabecera; sin deduplicación |
| Medios internos | 9,563 | Partes ZIP xl/media; bytes no extraídos |
| Anclas de dibujo | 10,003 | Objetos de drawing; pueden reutilizar medios |
| Fórmulas / caché ausente | 6,175 / 0 | Sin ejecución; caché no garantiza actualización |
| Nombres de ruta literales distintos | 72 | Sin equivalencias |
| Tipos fuente | 6,694 poste; 292 excedente; 56 cajadedmpalme; 1 Registro | Incluye versiones/solapes |
| Coordenadas fuera de rango mundial | 10 | Ocurrencias, sin reparar |
| Coordenadas no interpretables | 13 | 11 No detectado; B incorrecta; W ausente |
| Variantes N/W con rango mundial válido | 3 | Dos sin espacio, una con espacio doble |
| Repeticiones adicionales en hojas | 558 | Triples literales por hoja; no identidad de activos |

No sumar candidatos como activos únicos: hay versiones y fuentes solapadas. 5,177 triples globales distintos tampoco son activos identificados. Los 7,020 campos interpretables en rango mundial incluyen 13 ocurrencias fuera de una ventana geográfica exploratoria amplia y otros casos que requieren control local. No se declara un total final de VALIDO antes de aprobar reglas.

## Hallazgos prioritarios

1. Las tres muestras del encargo se confirmaron; los otros seis XLSX añaden desplazamiento horizontal, hoja vacía, filas ocultas, resúmenes auxiliares y varias rutas por libro.
2. Natura tiene 507 candidatos y 14 rutas; Postes_CFE 4,341 candidatos y 70 rutas. No debe suponerse archivo = ruta.
3. Canal 12 tiene 1,048,576 filas XML y solo 347 candidatos. Cargar un rectángulo max_row introduce trabajo y memoria innecesarios.
4. Los medios no equivalen a filas ni activos: 9,563 partes se usan en 10,003 anclas, algunas múltiples por fila y dos ancladas al encabezado.
5. Hay 10 coordenadas mundialmente imposibles, 13 no interpretables y ubicaciones atípicas aun con rango mundial válido. No se corrigió ni descartó nada.
6. Hay auxiliares sin decimal y errores #VALUE!; 1,203 filas muestran alguna señal al contrastarlos, incluidas 484 con solo diferencia pequeña de precisión. El texto completo debe ser la autoridad propuesta.
7. La copia STD de 181 filas es subconjunto del STD de 204, y las nueve huellas de archivo son distintas. Seleccionar versiones es una decisión de alcance.
8. Mirador se reproduce en campos y secuencia 551/551; Otay–Florido 968/969 literales y 969/969 al unificar un espacio doble. Los históricos conservan datos defectuosos.
9. Numero no demuestra secuencia de campo ni ID individual. Conservar orden no prueba conectividad.
10. No hay referencia histórica integral en los dos CSV para Natura ni la auditoría general. El AS-IS reporta 58 duplicados adicionales en Mirador y el conteo literal local da 56; requiere reconciliar criterio, no alterar fuentes.

## Familias y requisitos mínimos

| Familia | Requisito |
| --- | --- |
| F1_NOMBRE_ABC | Nombre/elemento/coordenandas completas en A/B/C; D/E numéricos, W positivo. |
| F2_RUTA_ABC_FOTO_D | Ruta/Elemento de Red/Coordenadas en A/B/C; foto D; auxiliares E:H. |
| F3_NUMERO_BCD | Numero A; ruta B; tipo C; coordenada D; foto E; auxiliares F:I. Incluye la excepción D1 vacío de Canal 12. |
| F4_DESPLAZADO_BCD | Ruta B; tipo C; coordenada D; foto E; auxiliares F:I. Sin Numero A en Natura. |

El futuro extractor debe seleccionar fuentes mediante manifiesto, mapear cabeceras verificadas, conservar fila exacta y valores originales, distinguir datos/resúmenes/objetos y registrar toda incidencia. Debe admitir múltiples archivos por auditoría y múltiples rutas por hoja, preservar filas ocultas y controlar versiones.

## Tratamiento eficiente recomendado

Usar ZIP y XML streaming con Python estándar, leyendo un libro a la vez y liberando cada row. Inventariar medios mediante tabla central y resolver únicamente relaciones/anclas cuando se necesite referencia. No leer imágenes, no abrir con reparación, no ejecutar macros/enlaces ni recalcular fórmulas. SharedStrings observado: máximo 375,601 bytes, frente a libros de 100–200 MB dominados por medios. Establecer un límite y estrategia acotada para futuros sharedStrings mayores. Recorrer el XML real de Canal 12 sin materializar un millón de filas; no tomar sus dimensiones como conteo ni el último registro actual como límite permanente. No se midió RSS máximo, por lo que aún no se promete una cifra de memoria.

## Contrato exacto propuesto

```csv
Ruta,Elemento de Red,Coordenadas
```

Tres columnas en ese orden, encabezado obligatorio, UTF-8 sin BOM, coma, CRLF y escape CSV de comillas/comas/saltos de línea. Ruta preservada sin fusionar nombres. Tipos propuestos POSTE / CAJA_EMP / EXCEDENTE; Registro queda pendiente. Coordenada decimal con punto, N, un espacio y W, conservando escala fuente sin redondear. Solo normalizaciones inequívocas aprobadas; no insertar decimales ni corregir dígitos. Detalle vinculante propuesto en 05.

Linaje y calidad separados en un futuro JSONL y manifiesto: hash, archivo_relativo, hoja, fila_original, valores literales, fórmulas/caché, atributos, referencias opcionales de imagen, estado/motivos/resolución y fila de CSV. No se crean esos laterales ahora. Exportar solo registros admitidos; todo rechazo/revisión conserva evidencia.

## Decisiones que requieren aprobación

| Decisión | Recomendación para aprobar o ajustar |
| --- | --- |
| Tipos de elemento | Aprobar poste→POSTE, cajadedmpalme→CAJA_EMP y excedente→EXCEDENTE. Definir Registro; mantenerlo REVISAR hasta entonces. |
| Versión y alcance por auditoría | Designar fuentes/hojas y orden mediante manifiesto. Para regresión de Mirador usar STD de 204 y Canal 12, manteniendo la copia de 181 como versión de prueba separada. No consolidar todos los libros automáticamente. |
| Equivalencias de rutas | Aprobar una tabla explícita si se necesitan fusiones. Conservar nombres literales y espacios/caracteres defectuosos en el linaje; definir si trim exterior se admite en salida. |
| Duplicados | Conservar ocurrencias y marcar grupos. Resolver identidad de activos y pertenencia a rutas antes de deduplicar; no usar coordenadas como ID. |
| Coordenadas y ámbito | Bloquear valores fuera de rango/no disponibles. Aprobar tolerancia de espacios N/W y perímetro esperado; resolver valores atípicos con evidencia, sin reparar dígitos. |
| Auxiliares | Priorizar coordenada completa; registrar diferencias, errores y precisión. Aprobar qué diferencias pequeñas se consideran informativas en lugar de bloqueantes. |
| Orden | Preservar fila fuente y orden de manifiesto para extracción. Confirmar por separado si existe orden de levantamiento; no autorizar conectividad por conservación de filas. |
| Contrato y regresión | Aprobar tres columnas y tipos controlados con laterales. Aceptar históricos como pruebas de extracción que incluyen fallos conocidos, no como verdad geográfica. Reconciliar 56 vs 58 duplicados del AS-IS. |

## Siguiente paso tras aprobación, sin ejecutarlo

Prototipo local del extractor XLSX→CSV con las reglas aprobadas, primero FLO-OTAY-BOMBEROS, Vía Rápida y Canal 12 y después los nueve libros. Verificar conteos, linaje, variantes, fórmulas/caché y memoria sin cargar medios; contrastar las dos regresiones separando extracción literal y validación de calidad. Ese prototipo no fue escrito. La etiqueta Fase 1B del encargo se refiere al siguiente trabajo del extractor; en TO-BE v0.1 1B nombra topología. Debe aclararse la nomenclatura para que la autorización del extractor no autorice topología ni CAD.

## Entregables y límites

- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\01_inventario_xlsx.md`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\02_perfiles_hojas.md`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\03_familias_y_mapeo_columnas.csv`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\04_calidad_y_anomalias.md`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\05_contrato_XLSX_a_CSV_propuesto.md`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\06_regresion_con_csv_historicos.md`
- `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen\07_checkpoint_para_aprobacion.md`

Inspección completa de estructura/celdas de los nueve XLSX y dos CSV autorizados; no inspección visual de imágenes. No se analizaron ZIP histórico, DWG, PDF ni TXT. Sin geoproyección, trazado, ETL productivo ni auditorías nuevas. No se descargó ni compartió información ni se instalaron dependencias. Se utilizaron lectores diagnósticos efímeros en memoria, sin guardar scripts. Detener aquí hasta recibir las decisiones y autorización del siguiente alcance.

## Verificación final de custodia y salida

Verificación posterior al guardado: **13/13 fuentes leídas conservan SHA-256 y tamaño** (9 XLSX, 2 CSV y 2 documentos de contexto). La fecha de última modificación también coincide al comparar con resolución de milisegundos; no se usa el tiempo de último acceso como prueba de integridad. Las huellas XLSX están en 01 y las de CSV en 06. La carpeta contiene exactamente los siete nombres autorizados. Textos UTF-8 sin BOM. CSV de mapeo: 87 filas, 9 columnas y encabezado.

Se verificaron reconciliación de totales, multiplicidades, estructura del mapeo y nueve referencias críticas XLSX a fila física CSV, además de las secuencias completas de 551 y 969 registros. La lectura se realizó con codificación UTF-8 explícita, conservando Conexión florido con su tilde. No se afirma inspección visual de imágenes ni ejecución nativa de Excel. No hay autorización aplicada a una fase posterior.
