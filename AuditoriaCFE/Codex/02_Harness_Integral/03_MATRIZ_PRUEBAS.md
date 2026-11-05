# Matriz de aceptación y pruebas — pipeline integral CFE

**Regla:** `OK` solo si la prueba se ejecutó y existe su resultado. `OMITIDA` es distinta de `OK`. `PENDIENTE_EVIDENCIA` no equivale a `FALLIDO_TECNICO`. Mantener 43 pruebas originales de versión 0.2.0, no reemplazarlas para inflar métricas.

## Pruebas automáticas obligatorias y artefactos

| ID | Capa | Prueba/fixture | Oráculo esperado | Ambiente |
|---|---|---|---|---|
| T01 | Git | compara HEAD, rama, cambios previos, no secretos staged | ningún dato ignorado/privado publicado | Local |
| T02 | XLSX | 4 familias e identificación de cabeceras | 4 reconocidas + casos anómalos trazados | CI |
| T03 | OOXML | 1,048,576 `row` con una fila útil | recorre filas reales sin cargar rectángulo | CI |
| T04 | OOXML | medios/imagenes/cachés/hojas ocultas | no abre imágenes, sí filas operativas | CI |
| T05 | Calidad | lat/lon N/W, variantes, precisión alta | sin redondeo de identidad ni reparación especulativa | CI |
| T06 | Tipos | variaciones inequívocas POSTE/CAJA_EMP/EXCEDENTE | catálogo exacto y desconocidos en revisión | CI |
| T07 | Identidad | duplicados exactos entre XLSX/subrutas | una fila física, linaje completo | CI |
| T08 | Identidad | dos cajas mismo lugar IDs externos; sin ID ambiguo | separa solo con evidencia confiable | CI |
| T09 | CP01 | sin P03/P06 | 00 poblado con identificables; 01 no promueve | CI |
| T10 | CP01 | errores/correcciones/exclusión por resolución | no edita XLSX; hash/estado/antes/después | CI |
| T11 | CP01 | revisión separada | 00 limpio de repeticiones, revisión reconciliada | CI |
| T12 | CP01 | cuatro auditorías/copias | fuentes en manifiesto, nada cruza auditorías | Local con originales |
| T13 | CP01 | regresión histórica Mirador | extracción 551; grupo previo 494 antes de nuevos overrides | Local con originales |
| T14 | CP01 | regresión histórica Otay | extracción 969; grupo previo 749 antes de nuevos overrides | Local con originales |
| T15 | CP01 | Natura | 507 candidatos/14 rutas en diagnóstico histórico | Local con originales |
| T16 | CP01 | General | 4341 candidatos en origen histórico; conteos explicados | Local con originales |
| T17 | Geografía | polígono, corredor y límites | dentro/fuera/borde correctos, sin autoexceptuar | CI |
| T18 | Geografía | ventana exploratoria vs polígono aprobado | solo aprobado habilita 01 productivo | CI |
| T19 | Geodesia | dos controles válidos | CSV02 proyectado, residual tolerado y CRS explícito | CI sintético |
| T20 | Geodesia | un control / unidades erróneas / +11.5 m | bloquea validación 02 | CI |
| T21 | Geodesia | comparación WCS reales del DWG DATRA | residual real registrado, tolerancia aprobada | AutoCAD + operador |
| T22 | Geodesia | ensayo candidato sin controles | rotulado NO VERIFICADO y sin 02 productivo | CI |
| T23 | Datos | 02 v1/v2 y ruta_id estable | lector distingue versión; cardinalidad 1:1 | CI |
| T24 | Manifest | hashes, conteos, migración legacy, crash | no mezcla lotes ni falsifica integridad | CI + local |
| T25 | KMZ | ZIP con path traversal/bomb/sin KML | rechazo seguro, ninguna extracción a histórico | CI |
| T26 | KMZ | Point/LineString/MultiGeometry/ExtendedData | IDs y coordenadas trazables | CI |
| T27 | KMZ | KMZ real (si disponible) | inventario y propuesta reproducibles, nada confirmado de oficio | Local |
| T28 | Topología | aristas confirmadas y sin confirmar | solo confirmadas entran a SCR | CI |
| T29 | Topología | bifurcación 0-1, 1-2, 1-3 | aristas exactas; nunca 2→3 falso o regreso doble | CI |
| T30 | Topología | ciclo 1-2-3-1 y puente compartido | dibuja 3 aristas una vez; no fuerza árbol | CI |
| T31 | Topología | tramos desconectados y cruces sin nodo | no los conecta artificialmente | CI |
| T32 | Topología | inicio/final desconocidos | candidatos separados de confirmados | CI |
| T33 | Topología | troncal vs ramal B06 | alerta, no reordena grafo certificado | CI |
| T34 | CAD | SCR01 sintaxis, recursos, layers | no postes ni mapa repetido | CI estático + AutoCAD |
| T35 | CAD | SCR02 bloques, P/C/E, atributos | 1 INSERT por ID físico, cuentas coinciden | CI estático + AutoCAD |
| T36 | CAD | símbolos no usan PDMODE por entidad | pruebas de capas/bloques | CI + AutoCAD |
| T37 | CAD | ausencia de topología confirmada | solo puntos PRELIMINAR | CI + AutoCAD |
| T38 | CAD | sistema sin CRS validado | solo modo ensayo en copia, no FINAL | CI + AutoCAD |
| T39 | CAD | perfil AutoCAD 2026 inglés, SCR y LISP | dos invocaciones en orden; no tercer paso oculto | AutoCAD |
| T40 | Plantilla | 1 DWT / mapa embebido / sin XREF falta | DWG nuevo abre con recursos y cajetín editable | AutoCAD |
| T41 | Papel | A1 841×594, DXF/detalles/leyenda | PDF sin recortes, campos verificados | AutoCAD |
| T42 | Presentación | gran inventario General | etiquetas visibles o bloqueo FINAL explicito | AutoCAD + owner |
| T43 | CLI | selección individual, dry-run, --batch | lotes separados, resumen conjunto | CI + Local |
| T44 | Rendimiento | XML grande y miles de registros | medición tiempo, RSS, disco, versión | CI limitado + Local |
| T45 | CI | GitHub Actions Python/lint/contracts | checks públicos sin XLSX/KMZ sensibles | GitHub |
| T46 | Git | PR, protección de main si disponible | PR listo, no merge, reglas verificadas o guía manual | GitHub |
| T47 | Entrega | DWG+PDF A1 y acta | owner revisa frente a manifiesto e incidencias | Manual |

## Criterios de liberación

**CP-01:** 00 íntegro y 00 revisión reconciliada, trazabilidad/exclusiones, regresiones, sin fuentes modificadas.

**CP-02:** 01 con ámbito aprobado; 02 solo con controles WCS reales (si no, `PENDIENTE_EVIDENCIA`); IDs y proyección/manifest versionados.

**CP-03:** SCR01 generado y ensayado contra copia de plantilla/DWT nativa; si no hay GUI queda `PENDIENTE_PRUEBA_CAD` sin fingir aprobación.

**CP-04:** SCR02 estático y, cuando haya AutoCAD, ejecutable con conteos/entidades validables; aristas solo si confirmadas, caso contrario puntos preliminares.

**E2E auditorías:** cuatro corridas explícitas, cada una con `entrada/`, `salida/`, manifest y resumen independiente; General requiere control de legibilidad especial. Bomberos no es gate de primera entrega.

**Final humano:** dueño de la auditoría confirma por revisión visual que DWG/PDF A1, coordenadas y recursos corresponden al levantamiento y valida incidentes. Una ejecución técnica terminada puede permanecer PRELIMINAR.

## Evidencia mínima por checkpoint

`acta_checkpoint.md`: código/hash, entradas y hashes, configuración/perímetro, número de pruebas ejecutadas/aprobadas/omitidas, estado por gate, errores y causa, capturas CAD si aplica, enlaces a manifiestos/archivos locales y commit Git. `CI green` no reemplaza `AutoCAD probado`, y viceversa.

## Política anti-regresiones

- Oráculo 7baa82c portable y verificable, no regenerar desde HEAD para simular compatibilidad.
- No cambiar bytes de 01/02 existentes sin versión nueva, diff de esquema y prueba de migración.
- Históricos 533/965 `POINT` sirven de regresión **histórica**, no son conteos de únicos ni autoridad geográfica; Mirador DWG tenía 527 POINT frente a TXT 533, dejar diferencia documentada.
- Contar explícitamente pruebas omitidas si no existe KMZ/AutoCAD/histórico; en CI pública no enmascararlas como 43/43 regresiones reales.

## Resultado del cierre integral

80 pruebas locales aprobadas, 0 fallidas/omitidas; las 43 anteriores siguen intactas. T01–T20/T22–T38 y T43/T44: código, fixtures y regresiones ejecutados según [cierre](CIERRE_INTEGRAL_2026-11-05.md). T21 queda PENDIENTE_EVIDENCIA por controles reales ausentes. T27 KMZ real disponible y leído sin confirmar propuestas.

T39: Core Console 2026 ejecutó ambos SCR, repetición/idempotencia y guardado en cinco copias (fixture + cuatro auditorías), con conteos reales; GUI no acreditada. T40 DWT canónica no creada/aceptada. T41 cinco PDF de una A1 comprobados con pdfinfo; no equivalen a impresión aceptada. T42 render de General/Mirador revela solapamientos, BLOQUEANTE FINAL. T45 CI de f22d886 verde; corte posterior de 80 casos se vuelve a comprobar en PR. T46 PR #1 y protección main verificados por API, sin merge. T47 ACEPTADO_HUMANO sigue pendiente. Los resultados detallados conservan hashes locales en cada salida/resultados_cad.
