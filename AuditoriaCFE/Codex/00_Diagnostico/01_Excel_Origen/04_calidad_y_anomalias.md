# 04. Calidad y anomalías

Fase 1A. Corte: 2026-11-03, America/Tijuana. Estado: diagnóstico, sin autorización de implementación.

**Raíz XLSX:** `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\Auditorias-20261104T035633Z-1-001\postes`. Todas las referencias a XLSX en este documento son relativas a esta raíz y conservan los nombres exactos, con `/` como separador documental.

## Hechos comprobados y alcance de los conteos

7,043 candidatos físicos, sin consolidar versiones ni deduplicar. Hay 0 rutas vacías, 0 tipos vacíos y 0 campos de coordenadas vacíos. Un texto como No detectado está poblado, pero no suministra coordenadas. Los totales no representan activos únicos.

| Patrón del campo completo | Candidatos | Criterio |
| --- | --- | --- |
| NW_ESTANDAR | 7017 | DecimalN, espacio único, DecimalW; dentro del rango mundial |
| NW_VARIANTE | 3 | N/W interpretable; espacio doble o ausente |
| FUERA_RANGO | 10 | Latitud >90 o magnitud de longitud >180; sin corregir dígitos |
| NO_INTERPRETABLE | 13 | 11 No detectado, una B como hemisferio y una W ausente |

7,020 campos son interpretables en N/W dentro de rango mundial; esto no acredita ubicación correcta en Tijuana. No se asignó un estado final de negocio a todos los registros porque las reglas de ámbito, versiones y duplicados aún requieren aprobación.

## Todas las coordenadas fuera de rango, no interpretables o con variante sintáctica

| XLSX relativo | Hoja | Fila original | Ruta literal | Tipo literal | Coordenada original íntegra | Diagnóstico |
| --- | --- | --- | --- | --- | --- | --- |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | Sheet1 | 2 | `STD HACIA CNAL 12` | poste | `32.52231521N 11702014028W` | FUERA_RANGO |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | Sheet1 | 58 | `STD HACIA CNAL 12` | poste | `32.52417096N117.03452398W` | NW_VARIANTE |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 | 2 | `STD HACIA CNAL 12` | poste | `32.52231521N 11702014028W` | FUERA_RANGO |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | Sheet1 | 81 | `STD HACIA CNAL 12` | poste | `32.52417096N117.03452398W` | NW_VARIANTE |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 | 198 | `RUTA flo-otay FO96` | excedente | `432.464440N 116.863542W` | FUERA_RANGO |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 | 604 | `RUTA flo-otay FO96` | excedente | `432.464440N 116.863542W` | FUERA_RANGO |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | Sheet1 | 66 | `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | excedente | `32.53828465N  116.92096598W` | NW_VARIANTE |
| Postes_CFE.xlsx | Postes_CFE | 522 | `RUTA flo-otay FO96` | poste | `32.504670B 116.865587W` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 561 | `ruta cll 1ra y Matias Brna-mar baltico/mar FO12` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 593 | `Ruta siglo21 - pte ngro pinos f024` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 613 | `Ruta siglo21 - pte ngro pinos f024` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 681 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 690 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 706 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 709 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 710 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 714 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 718 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 723 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | poste | `No detectado` | NO_INTERPRETABLE |
| Postes_CFE.xlsx | Postes_CFE | 2257 | `Ruta pte gloria sur - sta fe entrada cedros FO24` | poste | `132.480037N 116.989493W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 2648 | `Ruta insurgentes - florido F96` | poste | `132.512608N 116.979762W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 2658 | `ruta la gloria-barceloma-entronque blvr garcia / delicias fo48` | poste | `632.511790N 116.975135W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 3285 | `Plan a Playas` | poste | `132.422402N 117.035931W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 3290 | `Plan a Playas` | poste | `232.424924N 117.030285W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 3362 | `STD HACIA CNAL 12` | poste | `32.52231521N 11702014028W` | FUERA_RANGO |
| Postes_CFE.xlsx | Postes_CFE | 3716 | `Ruta Caliente 24 Hilos` | poste | `32.51067201N 116.99207905` | NO_INTERPRETABLE |

Las 10 ocurrencias fuera de rango no son necesariamente 10 errores independientes: una longitud sin decimal se repite en tres versiones/fuentes y la latitud 432.464440 se repite dos veces en FLO-OTAY final. No se propuso ninguna corrección de dígitos.

## Ámbito geográfico: señales de revisión, sin topología

Como filtro exploratorio se identificaron 13 ocurrencias dentro de rango mundial pero fuera de la ventana amplia latitud [32,33] N y longitud [-118,-116]. La ventana se declara expresamente como herramienta de diagnóstico basada en el entorno descrito, pendiente de aprobación como regla; no define el perímetro de una auditoría ni demuestra que los demás puntos estén bien. No se calcularon vecinos, distancias, aristas ni proyecciones.

| XLSX relativo | Hoja | Fila | Ruta literal | Coordenada original |
| --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | Sheet1 | 117 | `RUTA flo-otay FO96` | `2.52867353N 116.89829643W` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | Hoja1 | 247 | `Ruta canal 12 level antes 2014` | `32.513781N 177.083774W` |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | Hoja1 | 374 | `RUTA flo-otay FO96` | `2.52867353N 116.89829643W` |
| Postes_CFE.xlsx | Postes_CFE | 33 | `Ruta Konecta - Bellas Artes` | `39.54154139N 116.94306187W` |
| Postes_CFE.xlsx | Postes_CFE | 148 | `Ruta Konecta Playas` | `32.513202N 17.095592W` |
| Postes_CFE.xlsx | Postes_CFE | 156 | `RUTA intrc gloria-natura-pacifico` | `39.45546659N 116.97817999W` |
| Postes_CFE.xlsx | Postes_CFE | 379 | `RUTA flo-otay FO96` | `39.520563N 116.888078W` |
| Postes_CFE.xlsx | Postes_CFE | 672 | `Ruta STD / blvr aguacaliente/Emilio carranza FO72` | `2.51316N 117.00678W` |
| Postes_CFE.xlsx | Postes_CFE | 1457 | `GPON` | `39.453843N 117.021592W` |
| Postes_CFE.xlsx | Postes_CFE | 2405 | `RTA Mariano interc citio crojaflo-sitio bberos otay y rta c3tys-cucapah` | `2.488878N 116.982383W` |
| Postes_CFE.xlsx | Postes_CFE | 3599 | `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | `82.51863465N 116.98844751W` |
| Postes_CFE.xlsx | Postes_CFE | 3730 | `Ruta Caliente 24 Hilos` | `32.51361606N 119.99817227W` |
| Postes_CFE.xlsx | Postes_CFE | 3891 | `Ruta canal 12 level antes 2014` | `32.513781N 177.083774W` |

Otra señal específica del contexto AS-IS: `32.476223N 116.48565W` está en FLO-OTAY final, Hoja1, filas 91 y 496 (CSV histórico filas 135 y 540), y en FLO-OTAY-BOMBEROS, Sheet1, fila 197. Se conserva el texto con cinco decimales de W. Cumple los límites mundiales y queda dentro de la ventana amplia, pero sigue requiriendo corroboración local. No se eliminó por distancia ni similitud con otros puntos.

## Auxiliares y errores de celda

La coordenada completa es la fuente primaria propuesta. Se compararon numéricos auxiliares contra el texto N/W cuando era interpretable, con tolerancia diagnóstica 1e-9 grados. En FLO-OTAY-BOMBEROS E es W positivo; en las otras hojas I/H usa longitud negativa según el mapeo. Las pequeñas diferencias de precisión se distinguen de errores de magnitud.

| XLSX relativo | Filas con incidencia auxiliar | Solo diferencia de precisión ≤1e-6 | Otras incidencias | Celdas con texto de error e/str |
| --- | --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 150 | 150 | 0 | 0 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 0 | 0 | 0 | 0 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 158 | 156 | 2 | 2 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 0 | 0 | 0 | 0 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 180 | 178 | 2 | 2 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 622 | 0 | 622 | 4 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 0 | 0 | 0 | 0 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 44 | 0 | 44 | 0 |
| Postes_CFE.xlsx | 49 | 0 | 49 | 22 |

Hay 1,203 filas con alguna señal auxiliar bajo ese criterio: 484 solo por diferencia pequeña de precisión y 719 por otras causas. Las 13 coordenadas no interpretables no entran en esa comparación numérica; sus incidencias y errores se documentan por separado. Un valor auxiliar coincidente no salva una coordenada mundialmente imposible.

| XLSX / hoja / celda | Campo completo original | Auxiliar literal | Observación |
| --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx / Sheet1 / E6 | 32.54374822N 116.90650449W | 116.9065045 | Diferencia de precisión, no fallo de escala |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx / Hoja1 / G2 | 32.529070N 116.983918W | 32529070 | Caché de fórmula sin decimal; H2=-116983918 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx / Hoja1 / H2 | 32.500317N 116.860817W | 32500317 | 622 candidatos con incidencias auxiliares de magnitud/contenido |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx / Sheet1 / H81 | 32.52417096N117.03452398W | #VALUE! | Caché str; la coordenada completa sí admite separación por N/W |
| Postes_CFE.xlsx / Postes_CFE / H561 | No detectado | #VALUE! | Error tipado e; no hay fórmula en la celda |

Postes_CFE almacena 22 celdas `e` (#VALUE!) sin fórmulas, en H/I de 11 filas. Las hojas STD y su copia agregan cuatro textos #VALUE! de tipo `str`. FLO-OTAY final agrega cuatro textos #VALUE! de tipo `str`. Son 30 celdas con texto de error en total. Ninguna se recalculó. Las 6,175 fórmulas tienen caché, cuya vigencia no se verificó. La presencia de VALUE y resultados sin decimal es hecho; atribuirla a configuración regional sería inferencia sin prueba.

## Duplicados y versiones

Repetición exacta = igualdad literal de ruta, tipo y coordenada completa dentro de una hoja. Se cuentan ocurrencias adicionales, no el número total de filas afectadas. Se encontraron 558 adicionales dentro de las hojas. En todo el conjunto, 5,177 triples distintos para 7,043 candidatos (1,866 repeticiones adicionales globales), sin afirmar identidad de activos. Los solapes entre versiones no se suman como nuevos activos.

| XLSX relativo | Grupos repetidos | Adicionales | Coordenadas repetidas adicionales (sin ruta/tipo) |
| --- | --- | --- | --- |
| CFE FLO-OTAY-BOMBEROS.xlsx | 90 | 92 | 92 |
| CFE Natura  - Datra/Natura  - Datra.xlsx | 3 | 3 | 69 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Copy of STD HACIA CNAL 12.xlsx | 0 | 0 | 0 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx | 56 | 56 | 56 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/STD HACIA CNAL 12.xlsx | 0 | 0 | 0 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx | 216 | 216 | 223 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx | 1 | 1 | 12 |
| CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx | 1 | 1 | 4 |
| Postes_CFE.xlsx | 143 | 189 | 200 |

### Evidencia de duplicados: CFE FLO-OTAY-BOMBEROS.xlsx / Sheet1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.537673N 116.92415935W` | 290, 405 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.53743333N 116.92535937W` | 291, 406 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.53731482N 116.9271807W` | 292, 407 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.53727803N 116.92774913W` | 293, 408 |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.53718819N 116.92826583W` | 294, 409 |

### Evidencia de duplicados: CFE Natura  - Datra/Natura  - Datra.xlsx / Sheet1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `ruta comercial platech1-blvr heroes de independencia (frente OPA2) FO 24` | poste | `32.43485N 116.98618W` | 184, 185 |
| `colinas mty alestra` | poste | `32.50365N 117.02537W` | 420, 421 |
| `colinas mty alestra` | poste | `32.49624N 117.03147W` | 448, 449 |

### Evidencia de duplicados: CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador/Ruta canal 12 level antes 2014 Completo.xlsx / Hoja1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `Ruta canal 12 level antes 2014` | poste | `32.519300N 117.102513W` | 2, 121 |
| `Ruta canal 12 level antes 2014` | poste | `32.519472N 117.101973W` | 3, 122 |
| `Ruta canal 12 level antes 2014` | poste | `32.519742N 117.101453W` | 6, 123 |
| `Ruta canal 12 level antes 2014` | poste | `32.519780N 117.103229W` | 7, 119 |
| `Ruta canal 12 level antes 2014` | poste | `32.519858N 117.101138W` | 8, 124 |

### Evidencia de duplicados: CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/RUTA FLO-OTAY FO96 final.xlsx / Hoja1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `RUTA flo-otay FO96` | poste | `32.500317N 116.860817W` | 2, 397 |
| `RUTA flo-otay FO96` | excedente | `32.500317N 116.860823W` | 3, 398 |
| `RUTA flo-otay FO96` | excedente | `32.500313N 116.860823W` | 4, 399 |
| `RUTA flo-otay FO96` | poste | `32.499827N 116.860947W` | 5, 400 |
| `RUTA flo-otay FO96` | poste | `32.499608N 116.861052W` | 6, 401 |

### Evidencia de duplicados: CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta proteccion civil-blvr industrial-blvr industrial-esq blvr teran teran.xlsx / Sheet1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `ruta proteccion civil/blvr industrial-blvr industrial/esq blvr teran teran` | poste | `32.526832N 116.994161W` | 189, 190 |

### Evidencia de duplicados: CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido/ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx / Hoja1

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `ruta via rapida interc STD-CC-CALZ DEL TECNOLOGICO FO72` | excedente | `32.527630N 116.984674W` | 6, 7 |

### Evidencia de duplicados: Postes_CFE.xlsx / Postes_CFE

Se muestran hasta cinco grupos por hoja; los conteos anteriores abarcan todos los grupos.

| Ruta literal | Tipo | Coordenada literal | Filas originales |
| --- | --- | --- | --- |
| `Playas a Escenica` | poste | `32.470755N 117.118168W` | 6, 7 |
| `Ruta Konecta - Bellas Artes` | poste | `32.5324607N 116.94432435W` | 13, 47 |
| `Ruta Konecta - Bellas Artes` | poste | `32.53289613N 116.94430843W` | 14, 48 |
| `Ruta Konecta - Bellas Artes` | poste | `32.53319825N 116.94428453W` | 15, 49 |
| `Ruta Konecta - Bellas Artes` | poste | `32.53368125N 116.94418738W` | 16, 50 |

No se fusionaron las rutas. Se conservan 72 nombres literales distintos, incluidos errores ortográficos y el espacio final de `R3 a Cuahutemoc `. La ruta `Conexión florido` conserva su tilde original. La similitud de nombres no acredita equivalencia. Se conservaron filas ocultas: 44 en la copia de STD.

## Categorías de calidad propuestas, pendientes de aprobación

| Estado | Motivos propuestos | Tratamiento futuro |
| --- | --- | --- |
| VALIDO | Ruta y tipo reconocidos; coordenada interpretable, rango y ámbito aceptados; sin incidencia bloqueante pendiente | Elegible para CSV objetivo; no significa topología confirmada |
| REVISAR | TIPO_DESCONOCIDO, RUTA_VACIA, DUPLICADO_LITERAL, POSIBLE_VERSION, FUERA_AMBITO, AUX_INCONSISTENTE, FORMULA_SIN_CACHE, VARIANTE_FORMATO pendiente | Conservar íntegro en lateral; no incorporarlo como aprobado sin resolución |
| RECHAZADO | COORD_FUERA_RANGO o COORD_NO_INTERPRETABLE/NO_DISPONIBLE para uso geográfico | No exportar coordenada defectuosa; conservar fila y motivo; nunca borrar origen |

Prioridad propuesta: un motivo que impida obtener coordenada prevalece como RECHAZADO; sin él, cualquier motivo pendiente determina REVISAR; VALIDO solo al completar todos los controles aprobados. Pueden coexistir varios motivos. El catálogo no se ejecutó como ETL. En esta fase solo se registraron diagnósticos verificables.

Tipos observados: 6,694 poste, 292 excedente, 56 cajadedmpalme y 1 Registro. El último aparece en FLO-OTAY final / Hoja1 / fila 325 / `32.539783N 116.905100W`; se propone REVISAR, sin convertirlo a caja ni poste. No se identificó material, propiedad ni ID individual confiable.

## Hecho, inferencia y regla pendiente

Hechos: conteos, textos, celdas, hashes, posiciones y coincidencias anteriores. Inferencias: los dos STD son posibles versiones; diferencias pequeñas de auxiliares son compatibles con menor precisión; anclas próximas pueden corresponder a fotos del registro. Reglas pendientes: autoridad de versión, equivalencias de ruta, categorías admitidas, ámbito geográfico, duplicados y admisión de variantes N/W. Ninguna inferencia se convirtió en corrección.
