# 06. Regresión con CSV históricos

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

**Raíz de los CSV históricos, solo lectura:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Auditorias`. Los números de fila CSV siguientes son físicos y cuentan el encabezado cuando existe.

## Método y controles

Se leyeron exclusivamente STD-MIRADOR.csv y STD-OTAY-FLORIDO.csv de HISTORY_CAD con parser CSV, detectando UTF-8 y BOM. Ambos contienen tres campos en sus registros de datos. Se compararon triples literales (Ruta, Elemento de Red, Coordenadas), sin cambiar tipos, decimales ni nombres de ruta. Se comparó tanto multiconjunto como secuencia. Un segundo control colapsa únicamente espacios en blanco de la coordenada, y se declara por separado. No es validación geográfica ni prueba de que se haya recuperado el generador original.

| CSV | SHA-256 | Bytes | Líneas físicas | Encabezado | Vacías (filas físicas) | Registros | Duplicados literales adicionales |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STD-MIRADOR.csv | `46c62d0670e715dae2e0b9a4a306e591c2cbf98a066797f6b8d9aa0d5e583a17` | 32129 | 554 | No | 267, 339, 389 | 551 | 56 |
| STD-OTAY-FLORIDO.csv | `aa509d2928f9a51133f6b8e25d683411067ba7a1d97ed0cfbfa4c7a08510cf56` | 68015 | 970 | Sí | Ninguna | 969 | 218 |

## Reconstrucción de campos y secuencia

### Mirador

Concatenación documental de los 204 candidatos de `CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx` / Sheet1, seguida de los 347 de `CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx` / Hoja1: **551 de 551 triples coinciden literalmente y en el mismo orden** con STD-MIRADOR.csv. No se genera un nuevo CSV. Las tres filas vacías del histórico, 267, 339 y 389, corresponden a las filas 64, 136 y 186 vacías de Canal 12. La conservación de campos y orden es comprobable; la identidad del proceso que creó el archivo no lo es.

La copia STD de 181 registros es un subconjunto literal del STD de 204: faltarían 23 ocurrencias para ese bloque. No debe sumarse como otra ruta al libro de 204. La hoja vacía adicional no aporta registros.

### Otay–Florido

Concatenación documental: 44 de Vía Rápida, 622 de FLO-OTAY final y 303 de Protección Civil, en ese orden y conservando fila de cada fuente: **969 de 969 posiciones** reconstruibles, de las que **968 coinciden literalmente**. La posición 731 de datos (fila física 732) cambia únicamente dos espacios por uno en la coordenada. Al admitir exclusivamente esa normalización sintáctica coinciden las 969 posiciones. No se alteró el archivo original ni se atribuyó una causa al cambio.

| Fuente XLSX relativa | Hoja y fila | CSV histórico y fila física | Coordenada de origen (literal) | Coordenada CSV (literal) |
| --- | --- | --- | --- | --- |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | Sheet1 / 66 | STD-OTAY-FLORIDO.csv / 732 | `32.53828465N  116.92096598W` | `32.53828465N 116.92096598W` |

Se excluye del conteo candidato J624=`.` de FLO-OTAY final, sin borrarlo; F:I y O son auxiliares, no registros adicionales. Los totales de tipos del histórico se reconstruyen de las fuentes.

## Matriz de cobertura de cada fuente candidata

La intersección cuenta ocurrencias con multiplicidad: suma del mínimo de ocurrencias fuente/histórico por triple. Fuente sin cobertura = candidatos menos intersección; histórico sin esta fuente = datos históricos menos intersección. No significa exclusión errónea ni confirma independencia de libros.

### STD-MIRADOR.csv

| XLSX relativo | Candidatos fuente | Intersección literal | Fuente sin cobertura literal | Histórico no cubierto por esta fuente |
| --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 494 | 0 | 494 | 551 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 507 | 0 | 507 | 551 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 181 | 181 | 0 | 370 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 347 | 347 | 0 | 204 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 204 | 204 | 0 | 347 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 622 | 0 | 622 | 551 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 303 | 0 | 303 | 551 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 44 | 0 | 44 | 551 |
| Postes_CFE.xlsx | 4341 | 266 | 4075 | 285 |

Agrupaciones históricas: `STD HACIA CNAL 12`: 204; `Ruta canal 12 level antes 2014`: 347. Tipos: `poste`: 470; `cajadedmpalme`: 20; `excedente`: 61. Patrones: `FUERA_RANGO`: 1; `NW_ESTANDAR`: 549; `NW_VARIANTE`: 1.

### STD-OTAY-FLORIDO.csv

| XLSX relativo | Candidatos fuente | Intersección literal | Fuente sin cobertura literal | Histórico no cubierto por esta fuente |
| --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 494 | 402 | 92 | 567 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 507 | 0 | 507 | 969 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 181 | 0 | 181 | 969 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 347 | 0 | 347 | 969 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 204 | 0 | 204 | 969 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 622 | 622 | 0 | 347 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 303 | 302 | 1 | 667 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 44 | 44 | 0 | 925 |
| Postes_CFE.xlsx | 4341 | 199 | 4142 | 770 |

Agrupaciones históricas: `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72`: 44; `RUTA flo-otay FO96`: 622; `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran`: 303. Tipos: `poste`: 745; `excedente`: 200; `cajadedmpalme`: 23; `Registro`: 1. Patrones: `NW_ESTANDAR`: 967; `FUERA_RANGO`: 2.

Natura no tiene coincidencias literales con ninguno de los CSV. Esto no demuestra ausencia de activos compartidos: hay posibles diferencias de precisión o contenido que no se equipararon. Postes_CFE tiene cobertura parcial (266 ocurrencias con Mirador, 199 con Otay–Florido), pero solo postes y muchas rutas adicionales. FLO-OTAY-BOMBEROS aporta 402 ocurrencias literales comunes con Otay–Florido y 92 adicionales en su propio multiconjunto. No se asumió que fuera el Excel completo que originó el CSV.

## Muestras trazables por fuente

Los ejemplos siguientes indican ruta, tipo, coordenada y posición exactos. La unicidad se evalúa dentro del libro comparado; otras versiones pueden contener el mismo registro. Coincidencia no equivale a cadena de procedencia probada.

| XLSX relativo | Hoja | Fila | Ruta literal | Tipo | Coordenada original | CSV / fila física | Alcance de la atribución |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | Sheet1 | 5 | `RUTA flo-otay FO96` | poste | `32.54350756N 116.9071993W` | STD-OTAY-FLORIDO.csv / 262 | Única dentro de este libro e histórico |
| CFE FLO-OTAY-BOMBEROS.xlsx | Sheet1 | 6 | `RUTA flo-otay FO96` | poste | `32.54374822N 116.90650449W` | STD-OTAY-FLORIDO.csv / 265 | Única dentro de este libro e histórico |
| CFE Natura  - Datra/Natura  - Datra.xlsx | Sheet1 | 2 | `RUTA LA GLORIA - RED7 RADIOBASE LAZARO CARDENAS FO24` | poste | `32.43927N 117.00122W` | STD-OTAY-FLORIDO.csv | Sin coincidencia literal |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | Sheet1 | 2 | `STD HACIA CNAL 12` | poste | `32.52231521N 11702014028W` | STD-MIRADOR.csv / 1 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | Sheet1 | 3 | `STD HACIA CNAL 12` | poste | `32.52241086N 117.02027808W` | STD-MIRADOR.csv / 7 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | Hoja1 | 4 | `Ruta canal 12 level antes 2014` | poste | `32.519545N 117.102770W` | STD-MIRADOR.csv / 207 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | Hoja1 | 5 | `Ruta canal 12 level antes 2014` | poste | `32.519607N 117.102867W` | STD-MIRADOR.csv / 208 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 | 2 | `STD HACIA CNAL 12` | poste | `32.52231521N 11702014028W` | STD-MIRADOR.csv / 1 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 | 3 | `STD HACIA CNAL 12` | cajadedmpalme | `32.52229449N 117.02010997W` | STD-MIRADOR.csv / 2 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 | 218 | `RUTA flo-otay FO96` | poste | `32.54350756N 116.9071993W` | STD-OTAY-FLORIDO.csv / 262 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 | 219 | `RUTA flo-otay FO96` | cajadedmpalme | `32.54351386N 116.90720329W` | STD-OTAY-FLORIDO.csv / 263 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | Sheet1 | 2 | `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.54350024N 116.90722615W` | STD-OTAY-FLORIDO.csv / 668 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | Sheet1 | 3 | `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | cajadedmpalme | `32.54349957N 116.9072328W` | STD-OTAY-FLORIDO.csv / 669 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | Hoja1 | 2 | `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | poste | `32.529070N 116.983918W` | STD-OTAY-FLORIDO.csv / 2 | Única dentro de este libro e histórico |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | Hoja1 | 3 | `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | poste | `32.528860N 116.984002W` | STD-OTAY-FLORIDO.csv / 3 | Única dentro de este libro e histórico |
| Postes_CFE.xlsx | Postes_CFE | 3915 | `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.54350024N 116.90722615W` | STD-OTAY-FLORIDO.csv / 668 | Única dentro de este libro e histórico |
| Postes_CFE.xlsx | Postes_CFE | 3916 | `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.54336443N 116.90742598W` | STD-OTAY-FLORIDO.csv / 671 | Única dentro de este libro e histórico |

## Errores preservados por los históricos

| Fuente XLSX relativa | Hoja y fila | CSV y fila física | Coordenada literal | Resultado de calidad |
| --- | --- | --- | --- | --- |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 / 2 | STD-MIRADOR.csv / 1 | `32.52231521N 11702014028W` | Longitud imposible; no insertar decimal automáticamente |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 / 81 | STD-MIRADOR.csv / 80 | `32.52417096N117.03452398W` | Sintaxis sin espacio; auxiliares #VALUE! |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | Hoja1 / 247 | STD-MIRADOR.csv / 450 | `32.513781N 177.083774W` | Rango mundial válido, fuera de ventana exploratoria |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 / 198 y 604 | STD-OTAY-FLORIDO.csv / 242 y 648 | `432.464440N 116.863542W` | Latitud imposible |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 / 374 | STD-OTAY-FLORIDO.csv / 418 | `2.52867353N 116.89829643W` | Rango mundial válido, atípico para contexto local |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 / 91 y 496 | STD-OTAY-FLORIDO.csv / 135 y 540 | `32.476223N 116.48565W` | Corroborar ubicación; no eliminar automáticamente |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 / 325 | STD-OTAY-FLORIDO.csv / 369 | `32.539783N 116.905100W` | Tipo Registro sin decisión |

## Contraste con AS-IS

Se confirman 551 y 969 registros históricos y las huellas SHA-256 del AS-IS. Se confirma que uno no tiene encabezado y ambos traen BOM UTF-8. La primera fila real de Mirador es el poste con longitud sin decimal; el ejemplo de caja del AS-IS corresponde a la fila 2.

El AS-IS informa 58 repeticiones adicionales en Mirador. El recuento literal reproducido aquí da **56**; trim de extremos y colapso de espacios también dan 56. Otay–Florido sí coincide con 218. Se registra la discrepancia sin atribuir causa no demostrada y sin editar AS-IS. Los controles futuros deben declarar la clave y reglas exactas usadas para contar duplicados. Los conteos del encargo para las tres muestras XLSX se confirman (494 / 44 / 347 candidatos, 0 / 45 / 606 medios y 0 / 176 / 324 fórmulas).

## Uso como prueba de regresión y cobertura faltante

| Familia | Control útil | Límite |
| --- | --- | --- |
| F1_NOMBRE_ABC | 402 ocurrencias literales contra Otay–Florido; dos rutas y 494 candidatos como control de extracción | No reproduce el histórico completo; contiene repeticiones adicionales |
| F2_RUTA_ABC_FOTO_D | Vía Rápida 44/44 y misma secuencia en Otay–Florido | Auxiliares de magnitud defectuosa no deben alimentar coordenadas |
| F3_NUMERO_BCD | Mirador 551/551; FLO-OTAY 622/622; Protección Civil 302/303 literales y 303/303 al unificar espacio | Copia STD es parcial; Postes_CFE solo tiene regresión parcial; no aprobar errores geográficos |
| F4_DESPLAZADO_BCD | Natura: perfil independiente de 507 candidatos, 14 rutas, 842 medios | Sin coincidencia literal en los dos CSV y sin salida histórica propia autorizada para comparar |

No se dispone, dentro de los dos CSV autorizados, de una salida completa de la auditoría general para los 4,341 candidatos de Postes_CFE ni de referencia integral para Natura. No se buscaron otros CSV ni se analizaron CAD/TXT/PDF. Puede reconstruirse la selección de campos y el orden de las dos salidas de rutas, pero no certificarse el universo de activos, la limpieza histórica, la conectividad ni la exactitud de los planos.
