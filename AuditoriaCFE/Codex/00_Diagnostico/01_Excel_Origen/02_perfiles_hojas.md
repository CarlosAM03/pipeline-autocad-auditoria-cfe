# 02. Perfiles por libro y hoja

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

## Definiciones de conteo

Fila XML: elemento `<row>` existente, aunque solo tenga formato. Fila con valor: al menos una celda con valor literal o caché no vacío. Candidato: fila posterior al encabezado con algún valor en ruta, tipo o coordenada según el mapeo verificado. No equivale a registro válido ni activo único. Los candidatos incluyen filas ocultas y duplicados. Hoja vacía se documenta pero no aporta candidatos.

Se encontraron 7,053 filas con valor = 7,043 candidatos + 9 encabezados + 1 fila auxiliar (J624 de FLO-OTAY final). Hay 1,058,886 filas XML en total. No se encontraron encabezados desplazados verticalmente, celdas combinadas ni hojas ocultas; sí desplazamiento horizontal en Natura y un encabezado de coordenadas ausente en Canal 12.

Tipos OOXML: `s` cadena compartida; `str` cadena/caché de fórmula; `n` numérico; `e` error. Se conservó la cadena XML numérica literal para no ocultar precisión. Todas las 6,175 celdas con fórmula tienen caché presente; eso no prueba que esté actualizado. Las fórmulas compartidas se reconocen por `si`; no se interpretó su ausencia de texto en celdas dependientes como ausencia de fórmula.

## CFE FLO-OTAY-BOMBEROS.xlsx — Sheet1

| Métrica | Valor |
| --- | --- |
| Familia | F1_NOMBRE_ABC |
| Dimensión declarada | No declarada |
| Filas XML / última fila XML | 495 / 495 |
| Filas con valor / primera / última | 495 / 1 / 495 |
| Candidatos / intervalo | 494 / 2:495 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 1487; `n`: 988 |
| Fórmulas / caché ausente | 0 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 0 / 0 |
| Filas de anclaje / con varias imágenes / máximo | 0 / 0 / 0 |
| Números A poblados / distintos (texto XML) | 0 / 0 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Nombre` | 495 | `s`: 495 | 0 | A2 = `RUTA flo-otay FO96` |
| B | `elemento` | 495 | `s`: 495 | 0 | B2 = `poste` |
| C | `coordenandas completas` | 495 | `s`: 495 | 0 | C2 = `32.483333N 116.850692W` |
| D | `Coordenadas N` | 495 | `s`: 1; `n`: 494 | 0 | D2 = `32.483333` |
| E | `Coordenadas W` | 495 | `s`: 1; `n`: 494 | 0 | E2 = `116.850692` |

Mapeo verificado: route ← A; type ← B; coord ← C; aux_lat ← D; aux_lon ← E. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `RUTA flo-otay FO96` | 287 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | 207 |

Tipos: `poste`: 494.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 494 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 494. Repeticiones adicionales de triples literales dentro de esta hoja: 92 en 90 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 92. No se removió ninguna.

Auxiliares: 150 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 150 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 0 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

## CFE Natura  - Datra/Natura  - Datra.xlsx — Sheet1

| Métrica | Valor |
| --- | --- |
| Familia | F4_DESPLAZADO_BCD |
| Dimensión declarada | B1:J508 |
| Filas XML / última fila XML | 508 / 508 |
| Filas con valor / primera / última | 508 / 1 / 508 |
| Candidatos / intervalo | 507 / 2:508 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 2538; `n`: 1015 |
| Fórmulas / caché ausente | 0 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 842 / 848 |
| Filas de anclaje / con varias imágenes / máximo | 507 / 292 / 38 |
| Números A poblados / distintos (texto XML) | 0 / 0 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| B | `Ruta` | 508 | `s`: 508 | 0 | B2 = `RUTA LA GLORIA - RED7 RADIOBASE LAZARO CARDENAS FO24` |
| C | `Elemento de red` | 508 | `s`: 508 | 0 | C2 = `poste` |
| D | `Coordenadas` | 508 | `s`: 508 | 0 | D2 = `32.43927N 117.00122W` |
| E | `Foto` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| F | `` | 507 | `s`: 506; `n`: 1 | 0 | F2 = `32.43927N` |
| G | `` | 507 | `s`: 507 | 0 | G2 = `117.00122W` |
| H | `` | 507 | `n`: 507 | 0 | H2 = `32.43927` |
| I | `` | 507 | `n`: 507 | 0 | I2 = `-117.00122` |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `RUTA LA GLORIA - RED7 RADIOBASE LAZARO CARDENAS FO24` | 33 |
| `GPON` | 43 |
| `colinas mty alestra` | 107 |
| `RUTA flo-otay FO96` | 61 |
| `Ruta canal 12 level antes 2014` | 32 |
| `ruta comercial platech1-blvr heroes de independencia (frente OPA2) FO 24` | 10 |
| `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | 21 |
| `rute interc via rapida - siglo 21 FO48` | 34 |
| `ruta la gloria-barceloma-entronque blvr garcia / delicias fo48` | 36 |
| `ruta stdrio-ros-colinas rbase red 7 FO24` | 5 |
| `Ruta siglo21 - parque col reforma FO24` | 1 |
| `ruta libramiento sur talleres municipal R3` | 8 |
| `MTY alestra` | 34 |
| `Ruta a Natura` | 82 |

Tipos: `poste`: 507.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 507 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 507. Repeticiones adicionales de triples literales dentro de esta hoja: 3 en 3 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 69. No se removió ninguna.

Auxiliares: 0 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 0 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: twoCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 88 | 38 |
| 48 | 3 |
| 330 | 3 |
| 360 | 3 |
| 364 | 3 |
| 381 | 3 |
| 398 | 3 |
| 408 | 3 |

Muestras: `xl/drawings/drawing1.xml` fila 2, columna 5 → `xl/media/image1.png`; `xl/drawings/drawing1.xml` fila 3, columna 5 → `xl/media/image2.png`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx — Sheet1

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | No declarada |
| Filas XML / última fila XML | 977 / 977 |
| Filas con valor / primera / última | 182 / 1 / 182 |
| Candidatos / intervalo | 181 / 2:182 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 44 |
| Tipos de celda no vacía | `s`: 550; `n`: 542; `str`: 364 |
| Fórmulas / caché ausente | 724 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 196 / 196 |
| Filas de anclaje / con varias imágenes / máximo | 181 / 7 / 7 |
| Números A poblados / distintos (texto XML) | 181 / 1 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 182 | `s`: 1; `n`: 181 | 0 | A2 = `12.0` |
| B | `Ruta` | 182 | `s`: 182 | 0 | B2 = `STD HACIA CNAL 12` |
| C | `Elemento de red` | 182 | `s`: 182 | 0 | C2 = `poste` |
| D | `Coordenadas` | 182 | `s`: 182 | 0 | D2 = `32.52231521N 11702014028W` |
| E | `Foto` | 2 | `s`: 2 | 0 | E74 = `v` |
| F | `` | 181 | `str`: 181 | 181 | F2 = `32.52231521N` |
| G | `` | 181 | `str`: 181 | 181 | G2 = `11702014028W` |
| H | `` | 181 | `n`: 180; `str`: 1 | 181 | H2 = `32.52231521` |
| I | `` | 181 | `n`: 180; `str`: 1 | 181 | I2 = `-11702014028` |
| K | `Cajas de Empalme` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| L | `18.0` | 1 | `n`: 1 | 0 | Solo encabezado/resumen |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `STD HACIA CNAL 12` | 181 |

Tipos: `poste`: 137; `excedente`: 31; `cajadedmpalme`: 13.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 181 candidatos; vacíos 0. Patrones: `FUERA_RANGO`: 1; `NW_ESTANDAR`: 179; `NW_VARIANTE`: 1. Repeticiones adicionales de triples literales dentro de esta hoja: 0 en 0 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 0. No se removió ninguna.

Auxiliares: 158 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 156 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 2 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| F2 | `IF(ISERROR(FIND(" ", D2)), D2, LEFT(D2, FIND(" ", D2)-1))` | `32.52231521N` | F2:F182 |
| G2 | `IF(ISERROR(FIND(" ", D2)), D2, RIGHT(D2, LEN(D2)-FIND(" ", D2)))` | `11702014028W` | G2:G182 |
| H2 | `IF(RIGHT(F2,1)="N", VALUE(LEFT(F2,LEN(F2)-1)), -VALUE(LEFT(F2,LEN(F2)-1)))` | `32.52231521` | H2:H182 |
| I2 | `IF(RIGHT(G2,1)="E", VALUE(LEFT(G2,LEN(G2)-1)), -VALUE(LEFT(G2,LEN(G2)-1)))` | `-11702014028` | I2:I182 |

Errores textuales tipados `e` o `str`: H58 (str: #VALUE!), I58 (str: #VALUE!). Un valor `#VALUE!` de tipo `str` también es incidencia; contar solo tipo `e` la ocultaría.

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 3 | 7 |
| 5 | 3 |
| 6 | 3 |
| 8 | 3 |
| 4 | 2 |
| 7 | 2 |
| 26 | 2 |

Muestras: `xl/drawings/drawing1.xml` fila 4, columna 5 → `xl/media/image8.jpg`; `xl/drawings/drawing1.xml` fila 4, columna 5 → `xl/media/image21.jpg`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx — Sheet2

Hoja visible vacía: 0 filas XML, 0 valores, 0 candidatos, 0 fórmulas, 0 anclas. Sin mapeo de datos.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx — Hoja1

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | A1:I1048576 |
| Filas XML / última fila XML | 1048576 / 1048576 |
| Filas con valor / primera / última | 348 / 1 / 351 |
| Candidatos / intervalo | 347 / 2:351 |
| Filas vacías intercaladas con respecto a valores | 64, 136, 186 |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 1577; `n`: 1040; `str`: 162 |
| Fórmulas / caché ausente | 324 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 606 / 606 |
| Filas de anclaje / con varias imágenes / máximo | 348 / 187 / 5 |
| Números A poblados / distintos (texto XML) | 346 / 1 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 347 | `s`: 1; `n`: 346 | 0 | A3 = `5` |
| B | `Ruta` | 348 | `s`: 348 | 0 | B2 = `Ruta canal 12 level antes 2014` |
| C | `Elemento de red` | 348 | `s`: 348 | 0 | C2 = `poste` |
| D | `` | 347 | `s`: 347 | 0 | D2 = `32.519300N 117.102513W` |
| E | `Foto` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| F | `` | 347 | `s`: 266; `str`: 81 | 81 | F2 = `32.519300N` |
| G | `` | 347 | `s`: 266; `str`: 81 | 81 | G2 = `117.102513W` |
| H | `` | 347 | `n`: 347 | 81 | H2 = `32.519300000000001` |
| I | `` | 347 | `n`: 347 | 81 | I2 = `-117.102513` |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `Ruta canal 12 level antes 2014` | 347 |

Tipos: `poste`: 331; `excedente`: 14; `cajadedmpalme`: 2.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 347 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 347. Repeticiones adicionales de triples literales dentro de esta hoja: 56 en 56 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 56. No se removió ninguna.

Auxiliares: 0 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 0 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| F271 | `IF(ISERROR(FIND(" ", D271)), D271, LEFT(D271, FIND(" ", D271)-1))` | `32.504260N` | F271:F334 |
| G271 | `IF(ISERROR(FIND(" ", D271)), D271, RIGHT(D271, LEN(D271)-FIND(" ", D271)))` | `117.054727W` | G271:G334 |
| H271 | `IF(RIGHT(F271,1)="N", VALUE(LEFT(F271,LEN(F271)-1)), -VALUE(LEFT(F271,LEN(F271)-1)))` | `32.504260000000002` | H271:H334 |
| I271 | `IF(RIGHT(G271,1)="E", VALUE(LEFT(G271,LEN(G271)-1)), -VALUE(LEFT(G271,LEN(G271)-1)))` | `-117.054727` | I271:I334 |
| F335 | `IF(ISERROR(FIND(" ", D335)), D335, LEFT(D335, FIND(" ", D335)-1))` | `32.498277N` | F335:F351 |
| G335 | `IF(ISERROR(FIND(" ", D335)), D335, RIGHT(D335, LEN(D335)-FIND(" ", D335)))` | `117.035215W` | G335:G351 |

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 11 | 5 |
| 25 | 5 |
| 3 | 4 |
| 4 | 4 |
| 6 | 4 |
| 13 | 4 |
| 14 | 4 |
| 15 | 4 |

Muestras: `xl/drawings/drawing1.xml` fila 1, columna 10 → `xl/media/image1.jpeg`; `xl/drawings/drawing1.xml` fila 1, columna 10 → `xl/media/image2.jpeg`.

Anclas fuera de filas candidatas: `1`: 2. No se inspeccionó visualmente ninguna imagen.

Excepción comprobada: D1 no está poblada, aunque D2:D351 contiene coordenadas completas. A tiene el rótulo Numero y un único valor repetido en 346 candidatos; no es secuencia de recorrido. Filas 64, 136 y 186 están vacías entre datos. Hay dos imágenes ancladas en la fila 1.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx — Sheet1

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | No declarada |
| Filas XML / última fila XML | 1000 / 1000 |
| Filas con valor / primera / última | 205 / 1 / 205 |
| Candidatos / intervalo | 204 / 2:205 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 619; `n`: 611; `str`: 410 |
| Fórmulas / caché ausente | 816 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 206 / 206 |
| Filas de anclaje / con varias imágenes / máximo | 204 / 2 / 2 |
| Números A poblados / distintos (texto XML) | 204 / 1 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 205 | `s`: 1; `n`: 204 | 0 | A2 = `12.0` |
| B | `Ruta` | 205 | `s`: 205 | 0 | B2 = `STD HACIA CNAL 12` |
| C | `Elemento de red` | 205 | `s`: 205 | 0 | C2 = `poste` |
| D | `Coordenadas` | 205 | `s`: 205 | 0 | D2 = `32.52231521N 11702014028W` |
| E | `Foto` | 2 | `s`: 2 | 0 | E97 = `v` |
| F | `` | 204 | `str`: 204 | 204 | F2 = `32.52231521N` |
| G | `` | 204 | `str`: 204 | 204 | G2 = `11702014028W` |
| H | `` | 204 | `n`: 203; `str`: 1 | 204 | H2 = `32.52231521` |
| I | `` | 204 | `n`: 203; `str`: 1 | 204 | I2 = `-11702014028` |
| K | `Cajas de Empalme` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| L | `18.0` | 1 | `n`: 1 | 0 | Solo encabezado/resumen |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `STD HACIA CNAL 12` | 204 |

Tipos: `poste`: 139; `cajadedmpalme`: 18; `excedente`: 47.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 204 candidatos; vacíos 0. Patrones: `FUERA_RANGO`: 1; `NW_ESTANDAR`: 202; `NW_VARIANTE`: 1. Repeticiones adicionales de triples literales dentro de esta hoja: 0 en 0 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 0. No se removió ninguna.

Auxiliares: 180 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 178 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 2 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| F2 | `IF(ISERROR(FIND(" ", D2)), D2, LEFT(D2, FIND(" ", D2)-1))` | `32.52231521N` | F2:F205 |
| G2 | `IF(ISERROR(FIND(" ", D2)), D2, RIGHT(D2, LEN(D2)-FIND(" ", D2)))` | `11702014028W` | G2:G205 |
| H2 | `IF(RIGHT(F2,1)="N", VALUE(LEFT(F2,LEN(F2)-1)), -VALUE(LEFT(F2,LEN(F2)-1)))` | `32.52231521` | H2:H205 |
| I2 | `IF(RIGHT(G2,1)="E", VALUE(LEFT(G2,LEN(G2)-1)), -VALUE(LEFT(G2,LEN(G2)-1)))` | `-11702014028` | I2:I205 |

Errores textuales tipados `e` o `str`: H81 (str: #VALUE!), I81 (str: #VALUE!). Un valor `#VALUE!` de tipo `str` también es incidencia; contar solo tipo `e` la ocultaría.

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 5 | 2 |
| 49 | 2 |

Muestras: `xl/drawings/drawing1.xml` fila 12, columna 5 → `xl/media/image35.jpg`; `xl/drawings/drawing1.xml` fila 13, columna 5 → `xl/media/image40.jpg`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx — Hoja1

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | No declarada |
| Filas XML / última fila XML | 1684 / 1684 |
| Filas con valor / primera / última | 624 / 1 / 624 |
| Candidatos / intervalo | 622 / 2:623 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | 624 |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 1873; `n`: 1636; `str`: 1682 |
| Fórmulas / caché ausente | 2923 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 523 / 782 |
| Filas de anclaje / con varias imágenes / máximo | 622 / 152 / 3 |
| Números A poblados / distintos (texto XML) | 395 / 1 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 396 | `s`: 1; `n`: 395 | 0 | A2 = `31.0` |
| B | `Nombre ruta` | 623 | `s`: 623 | 0 | B2 = `RUTA flo-otay FO96` |
| C | `Elemento de Red` | 623 | `s`: 623 | 0 | C2 = `poste` |
| D | `Coordenadas ` | 623 | `s`: 623 | 0 | D2 = `32.500317N 116.860817W` |
| E | `Fotos` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| F | `` | 622 | `str`: 622 | 622 | F2 = `32.500317N` |
| G | `` | 622 | `str`: 622 | 622 | G2 = `116.860817W` |
| H | `` | 622 | `n`: 622 | 622 | H2 = `32500317` |
| I | `` | 622 | `n`: 618; `str`: 4 | 622 | I2 = `-116860817` |
| J | `` | 1 | `s`: 1 | 0 | J624 = `.` |
| K | `` | 1 | `s`: 1 | 0 | K2 = `Cajas de Empalme` |
| L | `` | 1 | `n`: 1 | 1 | L2 = `16` |
| O | `` | 434 | `str`: 434 | 434 | O2 = `32.500317N 116.860817W` |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `RUTA flo-otay FO96` | 622 |

Tipos: `poste`: 467; `excedente`: 138; `cajadedmpalme`: 16; `Registro`: 1.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 622 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 620; `FUERA_RANGO`: 2. Repeticiones adicionales de triples literales dentro de esta hoja: 216 en 216 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 223. No se removió ninguna.

Auxiliares: 622 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 622 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| F2 | `IF(ISERROR(FIND(" ", D2)), D2, LEFT(D2, FIND(" ", D2)-1))` | `32.500317N` | F2:F623 |
| G2 | `IF(ISERROR(FIND(" ", D2)), D2, RIGHT(D2, LEN(D2)-FIND(" ", D2)))` | `116.860817W` | G2:G623 |
| H2 | `IF(RIGHT(F2,1)="N", VALUE(LEFT(F2,LEN(F2)-1)), -VALUE(LEFT(F2,LEN(F2)-1)))` | `32500317` | H2:H623 |
| I2 | `IF(RIGHT(G2,1)="E", VALUE(LEFT(G2,LEN(G2)-1)), -VALUE(LEFT(G2,LEN(G2)-1)))` | `-116860817` | I2:I623 |
| L2 | `COUNTIF(C:C, "cajadedmpalme")` | `16` | Individual |
| O2 | `IFERROR(__xludf.DUMMYFUNCTION("FILTER(D:D, COUNTIF(D:D, D:D) > 1)\n"),"32.500317N 116.860817W")` | `32.500317N 116.860817W` | Individual |

Errores textuales tipados `e` o `str`: I33 (str: #VALUE!), I35 (str: #VALUE!), I434 (str: #VALUE!), I437 (str: #VALUE!). Un valor `#VALUE!` de tipo `str` también es incidencia; contar solo tipo `e` la ocultaría.

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 120 | 3 |
| 127 | 3 |
| 331 | 3 |
| 338 | 3 |
| 359 | 3 |
| 366 | 3 |
| 525 | 3 |
| 532 | 3 |

Muestras: `xl/drawings/drawing1.xml` fila 2, columna 5 → `xl/media/image14.jpg`; `xl/drawings/drawing1.xml` fila 3, columna 5 → `xl/media/image1.png`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

La fila 624 solo contiene J624 = `.` y no es candidato. O2:O435 tiene fórmulas con `__xludf.DUMMYFUNCTION`, `FILTER` y cachés de coordenadas duplicadas: columna auxiliar, no una segunda lista de activos. L2 usa COUNTIF sobre C:C y su caché es 16. No se recalculó.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx — Sheet1

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | A1:L304 |
| Filas XML / última fila XML | 304 / 304 |
| Filas con valor / primera / última | 304 / 1 / 304 |
| Candidatos / intervalo | 303 / 2:304 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 916; `n`: 910; `str`: 606 |
| Fórmulas / caché ausente | 1212 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 457 / 457 |
| Filas de anclaje / con varias imágenes / máximo | 303 / 149 / 3 |
| Números A poblados / distintos (texto XML) | 303 / 1 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 304 | `s`: 1; `n`: 303 | 0 | A2 = `32` |
| B | `Ruta` | 304 | `s`: 304 | 0 | B2 = `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` |
| C | `Elemento de red` | 304 | `s`: 304 | 0 | C2 = `poste` |
| D | `Coordenadas` | 304 | `s`: 304 | 0 | D2 = `32.54350024N 116.90722615W` |
| E | `Foto` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| F | `` | 303 | `str`: 303 | 303 | F2 = `32.54350024N` |
| G | `` | 303 | `str`: 303 | 303 | G2 = `116.90722615W` |
| H | `` | 303 | `n`: 303 | 303 | H2 = `32.54350024` |
| I | `` | 303 | `n`: 303 | 303 | I2 = `-116.90722615` |
| J | `Numero de Poste` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| K | `Cajas de Empalme` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| L | `6` | 1 | `n`: 1 | 0 | Solo encabezado/resumen |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | 303 |

Tipos: `poste`: 240; `cajadedmpalme`: 6; `excedente`: 57.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 303 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 302; `NW_VARIANTE`: 1. Repeticiones adicionales de triples literales dentro de esta hoja: 1 en 1 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 12. No se removió ninguna.

Auxiliares: 0 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 0 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| F2 | `IF(ISERROR(FIND(" ", D2)), D2, LEFT(D2, FIND(" ", D2)-1))` | `32.54350024N` | F2:F65 |
| G2 | `IF(ISERROR(FIND(" ", D2)), D2, RIGHT(D2, LEN(D2)-FIND(" ", D2)))` | `116.90722615W` | G2:G65 |
| H2 | `IF(RIGHT(F2,1)="N", VALUE(LEFT(F2,LEN(F2)-1)), -VALUE(LEFT(F2,LEN(F2)-1)))` | `32.54350024` | H2:H65 |
| I2 | `IF(RIGHT(G2,1)="E", VALUE(LEFT(G2,LEN(G2)-1)), -VALUE(LEFT(G2,LEN(G2)-1)))` | `-116.90722615` | I2:I65 |
| F66 | `IF(ISERROR(FIND(" ", D66)), D66, LEFT(D66, FIND(" ", D66)-1))` | `32.53828465N` | F66:F129 |
| G66 | `IF(ISERROR(FIND(" ", D66)), D66, RIGHT(D66, LEN(D66)-FIND(" ", D66)))` | ` 116.92096598W` | G66:G129 |

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 67 | 3 |
| 85 | 3 |
| 138 | 3 |
| 161 | 3 |
| 280 | 3 |
| 2 | 2 |
| 9 | 2 |
| 10 | 2 |

Muestras: `xl/drawings/drawing1.xml` fila 2, columna 5 → `xl/media/image1.jpeg`; `xl/drawings/drawing1.xml` fila 3, columna 5 → `xl/media/image2.jpeg`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx — Hoja1

| Métrica | Valor |
| --- | --- |
| Familia | F2_RUTA_ABC_FOTO_D |
| Dimensión declarada | No declarada |
| Filas XML / última fila XML | 1000 / 1000 |
| Filas con valor / primera / última | 45 / 1 / 45 |
| Candidatos / intervalo | 44 / 2:45 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 136; `str`: 88; `n`: 88 |
| Fórmulas / caché ausente | 176 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 45 / 45 |
| Filas de anclaje / con varias imágenes / máximo | 44 / 1 / 2 |
| Números A poblados / distintos (texto XML) | 0 / 0 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Ruta ` | 45 | `s`: 45 | 0 | A2 = `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` |
| B | `Elemento de Red ` | 45 | `s`: 45 | 0 | B2 = `poste` |
| C | `Coordenadas` | 45 | `s`: 45 | 0 | C2 = `32.529070N 116.983918W` |
| D | `Foto` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| E | `` | 44 | `str`: 44 | 44 | E2 = `32.529070N` |
| F | `` | 44 | `str`: 44 | 44 | F2 = `116.983918W` |
| G | `` | 44 | `n`: 44 | 44 | G2 = `32529070` |
| H | `` | 44 | `n`: 44 | 44 | H2 = `-116983918` |

Mapeo verificado: route ← A; type ← B; coord ← C; photo ← D; token_lat ← E; token_lon ← F; aux_lat ← G; aux_lon ← H. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | 44 |

Tipos: `poste`: 38; `excedente`: 5; `cajadedmpalme`: 1.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 44 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 44. Repeticiones adicionales de triples literales dentro de esta hoja: 1 en 1 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 4. No se removió ninguna.

Auxiliares: 44 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 44 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

### Fórmulas representativas (sin ejecutar)

| Celda | Fórmula literal XML | Caché XML | Rango compartido |
| --- | --- | --- | --- |
| E2 | `IF(ISERROR(FIND(" ", C2)), C2, LEFT(C2, FIND(" ", C2)-1))` | `32.529070N` | E2:E45 |
| F2 | `IF(ISERROR(FIND(" ", C2)), C2, RIGHT(C2, LEN(C2)-FIND(" ", C2)))` | `116.983918W` | F2:F45 |
| G2 | `IF(RIGHT(E2,1)="N", VALUE(LEFT(E2,LEN(E2)-1)), -VALUE(LEFT(E2,LEN(E2)-1)))` | `32529070` | G2:G45 |
| H2 | `IF(RIGHT(F2,1)="E", VALUE(LEFT(F2,LEN(F2)-1)), -VALUE(LEFT(F2,LEN(F2)-1)))` | `-116983918` | H2:H45 |

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 2 | 2 |

Muestras: `xl/drawings/drawing1.xml` fila 2, columna 4 → `xl/media/image9.jpg`; `xl/drawings/drawing1.xml` fila 3, columna 4 → `xl/media/image6.jpg`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## Postes_CFE.xlsx — Postes_CFE

| Métrica | Valor |
| --- | --- |
| Familia | F3_NUMERO_BCD |
| Dimensión declarada | A1:K4342 |
| Filas XML / última fila XML | 4342 / 4342 |
| Filas con valor / primera / última | 4342 / 1 / 4342 |
| Candidatos / intervalo | 4341 / 2:4342 |
| Filas vacías intercaladas con respecto a valores | Ninguna |
| Filas con valores fuera de campos candidatos | Ninguna |
| Estado / filas con valores ocultas | visible / 0 |
| Tipos de celda no vacía | `s`: 21710; `n`: 12786; `e`: 22 |
| Fórmulas / caché ausente | 0 / 0 |
| Hipervínculos de hoja | 0 |
| Medios del libro / anclas de hoja | 6688 / 6863 |
| Filas de anclaje / con varias imágenes / máximo | 4341 / 2321 / 38 |
| Números A poblados / distintos (texto XML) | 4125 / 71 |

### Columnas observadas

| Columna | Encabezado real fila 1 (literal) | Celdas con valor/fórmula | Tipos | Fórmulas | Ejemplo con fila |
| --- | --- | --- | --- | --- | --- |
| A | `Numero` | 4126 | `s`: 1; `n`: 4125 | 0 | A2 = `2` |
| B | `Ruta` | 4342 | `s`: 4342 | 0 | B2 = `Playas a Escenica` |
| C | `Elemento de red` | 4342 | `s`: 4342 | 0 | C2 = `poste` |
| D | `Coordenadas` | 4342 | `s`: 4342 | 0 | D2 = `32.473981N 117.118553W` |
| E | `Foto` | 1 | `s`: 1 | 0 | Solo encabezado/resumen |
| F | `` | 4341 | `s`: 4340; `n`: 1 | 0 | F2 = `32.473981N` |
| G | `` | 4341 | `s`: 4341 | 0 | G2 = `117.118553W` |
| H | `` | 4341 | `n`: 4330; `e`: 11 | 0 | H2 = `32.473981000000002` |
| I | `` | 4341 | `n`: 4330; `e`: 11 | 0 | I2 = `-117.11855300000001` |
| J | `` | 1 | `s`: 1 | 0 | J4328 = `\|` |

Mapeo verificado: route ← B; type ← C; coord ← D; photo ← E; token_lat ← F; token_lon ← G; aux_lat ← H; aux_lon ← I; number ← A. Las fotografías son objetos de drawing, aunque la celda Foto carezca de valor. K/L contienen resúmenes y no son atributos de cada activo. No se detectó columna de observaciones operativas por registro.

### Rutas y categorías, sin equivalencias

| Ruta literal | Candidatos |
| --- | --- |
| `Playas a Escenica` | 110 |
| `Ruta Konecta - Bellas Artes` | 68 |
| `Ruta Konecta - Fusion` | 28 |
| `Ruta Konecta - Ocampo` | 12 |
| `Ruta Konecta Playas` | 28 |
| `RUTA intrc gloria-natura-pacifico` | 49 |
| `Ruta interc troncal via rapida-cetys-cucapah interc troncal ruta otay-flo` | 237 |
| `RUTA flo-otay FO96` | 315 |
| `ruta cll 1ra y Matias Brna-mar baltico/mar FO12` | 39 |
| `Ruta siglo21 - pte ngro pinos f024` | 94 |
| `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | 90 |
| `ruta1 de emergencia fo24` | 33 |
| `ruta zgas-interc pt bvsta std fo24` | 59 |
| `Ruta puente americas (granero)-interc via rapida STD-CC-MBIT` | 47 |
| `Plan a Playas` | 218 |
| `Ruta flo Magon/cris colom-Ign Allende/Azcona` | 24 |
| `Ruta brazo interc stdrio/std playas-costco rio` | 24 |
| `Ruta nva por emergencia 2 fo12` | 11 |
| `ruta puente americas (granero) - DESOM FO 24` | 50 |
| `RUTA BLVR CUAHUTEMOC NORTE, LIBERTAD-CUAHUTEMOC NORTE/ CALLE 16 DROP 2 HILOS` | 67 |
| `RUTA LA GLORIA - RED7 RADIOBASE LAZARO CARDENAS FO24` | 68 |
| `Ruta M d chicago-avit-radiobase oaxaca red 7 FO12` | 57 |
| `ruta MDCHICAGO/CITIO VALLARTA RED7 Fo12` | 16 |
| `Ruta Konekta Firocopy` | 19 |
| `Ruta Konekta Juarez` | 5 |
| `GPON` | 105 |
| `ruta ptenegro pinos / blvr diaz ordaz y av las presas` | 116 |
| `Ruta Santa fe` | 47 |
| `rta fo24insurgentes intrc std-crzrflorido` | 49 |
| `Conexión florido` | 53 |
| `RUTA RIO SUB` | 12 |
| `colinas mty alestra` | 120 |
| `FO 48 RTA La MORITA` | 51 |
| `Ruta canal 12 level antes 2014` | 377 |
| `ruta interc sta fe - centro cultural sta fe2 FO12` | 19 |
| `RTA PARPROFO12` | 23 |
| `Ruta pte gloria sur - sta fe entrada cedros FO24` | 110 |
| `ruta brazo flo-otay-refugio/tijtec FO24` | 54 |
| `RTA Mariano interc citio crojaflo-sitio bberos otay y rta c3tys-cucapah` | 46 |
| `24 hilos cerro colorao` | 57 |
| `ruta libramiento sur talleres municipal R3` | 79 |
| `ruta comercial platech1-blvr heroes de independencia (frente OPA2) FO 24` | 26 |
| `Ruta insurgentes - florido F96` | 31 |
| `ruta la gloria-barceloma-entronque blvr garcia / delicias fo48` | 170 |
| `Ruta citio bomberos FO24` | 9 |
| `Ruta blvr industrial Anaglobal FO24` | 16 |
| `ruta unida deportiva` | 47 |
| `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | 94 |
| `rute interc via rapida - siglo 21 FO48` | 40 |
| `Ruta pte gloria sur hacia santa fe FO12` | 10 |
| `Ruta rubi canal 12` | 39 |
| `ruta stdrio-ros-colinas rbase red 7 FO24` | 29 |
| `Line 10` | 1 |
| `Line 11` | 2 |
| `Ruta Tijtec refugio-deleg mpal presa este FO12` | 21 |
| `ruta interc OPA1 / OPA3 PLANTA NUEVA FO24` | 21 |
| `Ruta siglo21 - parque col reforma FO24` | 52 |
| `ruta interc ruta insurgentes-hyundai-planta1-ruta otay FO72` | 15 |
| `STD HACIA CNAL 12` | 116 |
| `Ruta malecon` | 25 |
| `ruta delg mesa a R3` | 60 |
| `rutaclmxhipo - auditorioFo12` | 14 |
| `Ruta blvr industrial - blvr Bellas artes esquemas Josefina Rendon FO24` | 36 |
| `Ruta Caliente 24 Hilos` | 56 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | 183 |
| `Ruta parque Mexico sur-paseo enseda y parque azteca sur FO 24` | 41 |
| `R3 a Cuahutemoc ` | 47 |
| `Ruta citio std playas - interc century - mir - stdrio` | 31 |
| `Ruta citio std playas - interc century - ros - stdrio` | 6 |
| `RUTA PARQUE MORELOS` | 17 |

Tipos: `poste`: 4341.

### Coordenadas y auxiliares

Campo de coordenadas poblado en 4341 candidatos; vacíos 0. Patrones: `NW_ESTANDAR`: 4322; `NO_INTERPRETABLE`: 13; `FUERA_RANGO`: 6. Repeticiones adicionales de triples literales dentro de esta hoja: 189 en 143 grupos. Repeticiones adicionales del texto de coordenadas, sin distinguir ruta/tipo: 200. No se removió ninguna.

Auxiliares: 49 filas con diferencia mayor que 1e-9 grados, magnitud imposible o texto no numérico, solo donde el campo completo admite interpretación N/W. De ellas 0 tienen únicamente diferencia ≤1e-6 grados, compatible con menor precisión, sin afirmar su causa. Las restantes 49 requieren revisar magnitud o contenido. La comparación de W de FLO-OTAY-BOMBEROS usa magnitud positiva; en las demás hojas usa longitud firmada negativa. No se convierten auxiliares enteros mediante potencias de diez.

Errores textuales tipados `e` o `str`: H561 (e: #VALUE!), I561 (e: #VALUE!), H593 (e: #VALUE!), I593 (e: #VALUE!), H613 (e: #VALUE!), I613 (e: #VALUE!), H681 (e: #VALUE!), I681 (e: #VALUE!), H690 (e: #VALUE!), I690 (e: #VALUE!), H706 (e: #VALUE!), I706 (e: #VALUE!), H709 (e: #VALUE!), I709 (e: #VALUE!), H710 (e: #VALUE!), I710 (e: #VALUE!), H714 (e: #VALUE!), I714 (e: #VALUE!), H718 (e: #VALUE!), I718 (e: #VALUE!), H723 (e: #VALUE!), I723 (e: #VALUE!). Un valor `#VALUE!` de tipo `str` también es incidencia; contar solo tipo `e` la ocultaría.

### Referencias de imágenes

Anclas por fila inicial, índice convertido de cero a uno. Es relación geométrica, no identificación certificada de la foto del activo. Tipos de ancla: oneCellAnchor.

| Fila inicial | Cantidad de imágenes ancladas |
| --- | --- |
| 1793 | 38 |
| 922 | 15 |
| 953 | 8 |
| 885 | 6 |
| 1393 | 6 |
| 3 | 4 |
| 367 | 4 |
| 757 | 4 |

Muestras: `xl/drawings/drawing1.xml` fila 2, columna 5 → `xl/media/image1.png`; `xl/drawings/drawing1.xml` fila 3, columna 5 → `xl/media/image2.png`.

Anclas fuera de filas candidatas: Ninguno. No se inspeccionó visualmente ninguna imagen.

## Orden y atributos ausentes

La columna Numero es constante por libro en las hojas de ruta, y Postes_CFE tiene 4,125 celdas A pobladas con solo 71 valores distintos para 4,341 candidatos. No constituye un identificador único ni una secuencia de postes demostrada. La conservación de secuencia XLSX→CSV sí se verifica en 06, pero no prueba recorrido ni conectividad. J1 de Protección Civil dice Numero de Poste y no tiene datos debajo.

No hay campos estructurados por registro para material/propiedad del poste, transformador, especificación de cable/herrajes, reservas, responsable/concesionario, logos aprobados, aristas desde/hasta o inicio/fin confirmado. FO24/FO72/FO96 en nombres de ruta son texto y no acreditan por sí solos esos atributos. La posible información visible en fotos queda fuera de esta inspección.
