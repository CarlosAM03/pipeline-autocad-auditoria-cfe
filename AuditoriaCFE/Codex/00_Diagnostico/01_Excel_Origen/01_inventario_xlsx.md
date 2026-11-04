# 01. Inventario de XLSX originales

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

## Preflight y custodia

Se validaron antes del inventario las rutas exactas del encargo. WORKSPACE_ROOT, PROJECT_ROOT, HISTORY_ROOT, RAW_XLSX_ROOT y HISTORY_CAD existen como directorios y sus padres resueltos coinciden con las relaciones exigidas. SPEC_FILE y ASIS_FILE existen. Los dos XLSX esperados en la raíz y los dos CSV de referencia existen. La salida no existía al iniciar. Su ruta canónica está dentro de PROJECT_ROOT y fuera de HISTORY_ROOT. Ningún archivo descubierto sale de RAW_XLSX_ROOT al resolver enlaces. No se buscaron rutas sustitutivas.

| Autoridad | Ruta absoluta |
| --- | --- |
| WORKSPACE_ROOT | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria |
| PROJECT_ROOT | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE |
| HISTORY_ROOT | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001 |
| RAW_XLSX_ROOT | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes |
| HISTORY_CAD | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Auditorias |
| SPEC_FILE | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.1.md |
| ASIS_FILE | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Reconstruccion_Pipeline_CFE_ASIS_2026-11-03.md |
| DIAG_OUTPUT | C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\00_Diagnostico\01_Excel_Origen |

## Método y universo

Búsqueda recursiva exclusivamente bajo RAW_XLSX_ROOT: **9 XLSX, 0 XLS**, 10 hojas, 7,043 candidatos y 9,563 partes de medios. SHA-256 calculado leyendo bytes por bloques. ZIP en modo `r`; se inspeccionaron tablas centrales, workbook, relaciones, sharedStrings, hojas mediante XML streaming y anclas de drawings. No se leyeron los bytes de las imágenes ni se extrajo postes.zip. Solo se mantuvieron en memoria filas con valor o fórmula; se liberaron las filas XML ya procesadas. Se procesó un libro a la vez. El conjunto retenido corresponde a miles de filas útiles, no al área formateada. No se abrieron libros con Excel ni se recalcularon fórmulas.

| XLSX relativo | Bytes del archivo | MiB | Hojas | Candidatos | Medios ZIP | Anclas |
| --- | --- | --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 25182 | 0.02 | Sheet1 | 494 | 0 | 0 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 194881065 | 185.85 | Sheet1 | 507 | 842 | 848 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 4771198 | 4.55 | Sheet1; Sheet2 | 181 | 196 | 196 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 116426345 | 111.03 | Hoja1 | 347 | 606 | 606 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 5367016 | 5.12 | Sheet1 | 204 | 206 | 206 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 91637570 | 87.39 | Hoja1 | 622 | 523 | 782 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 12269413 | 11.70 | Sheet1 | 303 | 457 | 457 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 9448586 | 9.01 | Hoja1 | 44 | 45 | 45 |
| Postes_CFE.xlsx | 184189878 | 175.66 | Postes_CFE | 4341 | 6688 | 6863 |

## Manifiesto de huellas

| XLSX relativo | SHA-256 |
| --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | `0c864245749eb58e9bebd5d7316a9fc9cdb1b42557b55f528084d0d522aedc71` |
| CFE Natura  - Datra/Natura  - Datra.xlsx | `91a2163739d3bee843ebc17432c4b8a28c2b32575efdf879b53f5815d18953bb` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | `9b357d30260132fd6b3558eecbb0ac47aeb05f0526c7f92f9ea417ca2613e8d2` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | `213e6252440f2668ccaa17bdd3e4f27eeceac7544d7c40e9f3680a6148fb4897` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | `be8b95cecbcc77ffc9260058a75d6347ab9f0f81862f86d43490e4075709c538` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | `8cc45d2b33e8c599666e94be90f466fc97015dbee2867e01958e99aac4c8454d` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | `93fee944c6cf3c0461cc34261e55b3f3ec9475b7f6a5dcce3cdac368866b3c71` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | `7df3086c48d25dd29e146c592417ecf25d1e36690212a2842abe250017b3242d` |
| Postes_CFE.xlsx | `230cb70392a5b04b9121f1000192325c7efedb3fc7126eadf2d6fdaa917fa637` |

## Causa del tamaño

Los tamaños siguientes son metadatos del ZIP, no imágenes extraídas. Medios cuenta partes, no activos ni fotografías únicas. Una parte puede utilizarse en varias anclas.

| XLSX relativo | Medios sin comprimir MiB | Medios comprimidos MiB | ZIP total sin comprimir MiB | Mayor parte no media (bytes) |
| --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 0.00 | 0.00 | 0.12 | xl/worksheets/sheet1.xml (103226) |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 185.66 | 185.66 | 186.80 | xl/drawings/drawing1.xml (869105) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 4.53 | 4.50 | 4.80 | xl/worksheets/sheet1.xml (127049) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 108.05 | 108.05 | 176.85 | xl/worksheets/sheet1.xml (71349767) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 5.10 | 5.07 | 5.37 | xl/worksheets/sheet1.xml (128219) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 87.51 | 87.27 | 88.40 | xl/drawings/drawing1.xml (432340) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 11.59 | 11.59 | 12.31 | xl/drawings/drawing1.xml (496072) |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 9.04 | 8.99 | 9.14 | xl/worksheets/sheet1.xml (60091) |
| Postes_CFE.xlsx | 174.29 | 174.29 | 182.89 | xl/drawings/drawing1.xml (5961016) |

Natura y Postes_CFE están dominados por medios. Canal 12 agrega `xl/worksheets/sheet1.xml` de 71,349,767 bytes, con 1,048,576 filas XML; solo 348 filas tienen valores, incluido el encabezado. Esto demuestra exceso de área/formato sin que el conteo de registros aumente.

## Originales idénticos y posibles versiones

Las 9 huellas SHA-256 son distintas: no hay libros idénticos byte a byte. La igualdad de registros no demuestra igualdad de archivos ni identidad de activos.

`Copy of STD HACIA CNAL 12.xlsx` tiene 181 candidatos, segunda hoja vacía y 196 medios; `STD HACIA CNAL 12.xlsx` tiene 204 candidatos y 206 medios. Los 181 triples de la copia aparecen en el libro de 204 registros. Son versiones candidatas, sin prueba de cuál es autoritativa ni de la cronología. No se eligió ni eliminó ninguna.

| Fuente A | Fuente B | Intersección de ocurrencias de triples literales |
| --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 287 |
| CFE FLO-OTAY-BOMBEROS.xlsx | CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 115 |
| CFE FLO-OTAY-BOMBEROS.xlsx | Postes_CFE.xlsx | 133 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | Postes_CFE.xlsx | 294 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 181 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | Postes_CFE.xlsx | 72 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | Postes_CFE.xlsx | 192 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Postes_CFE.xlsx | 74 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Postes_CFE.xlsx | 17 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | Postes_CFE.xlsx | 182 |

La intersección usa multiconjuntos y cuenta `min(ocurrencias_A,ocurrencias_B)`. No es una deduplicación. Natura comparte 294 ocurrencias con Postes_CFE y aporta otras 213 sin coincidencia literal en ese libro. FLO-OTAY-BOMBEROS solapa con las dos rutas históricas, pero no sustituye sus 969 registros.

## Contexto leído y límites

| Documento de contexto | SHA-256 |
| --- | --- |
| C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\AuditoriaCFE\Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.1.md | `cc4c5054a0c919add5ec1c28e08e750ac51ce102564d6067b27743b22462bfab` |
| C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\Reconstruccion_Pipeline_CFE_ASIS_2026-11-03.md | `89b81e5e473b283b32ab43312c1c367cfd618041fff505acbcb90f76e9519205` |

El AS-IS declaraba los Excel ausentes en su checkpoint anterior. Esta fase comprueba su disponibilidad local actual, sin editar ese documento. No se analizaron DWG, PDF, TXT ni el contenido de postes.zip. La validación de integridad posterior a los reportes se registra en 07.
