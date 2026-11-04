# Auditorías CFE — Revisión técnica del diagnóstico de Excel (Fase 1A)

**Fecha de revisión:** 3 de noviembre de 2026 (America/Tijuana).  
**Estado:** revisión documental del paquete `01_Excel_Origen.zip`; no constituye aprobación de reglas de negocio ni autorización de implementación.  
**Alcance:** siete entregables de Codex. No se tuvo acceso directo al sistema de archivos de Windows donde Codex ejecutó el diagnóstico; los hashes de fuentes históricas fueron reportados por Codex, no recalculados en esta revisión.

## 1. Dictamen

**Fase 1A: aceptable como diagnóstico documental, con observaciones y decisiones abiertas.** El archivo comprimido contiene los siete entregables previstos. Los conteos principales son consistentes entre informes y el catálogo de mapeo contiene 87 reglas/registros de correspondencia distribuidos entre las cuatro familias. No se ha implementado el extractor y no se autoriza ninguna deduplicación, corrección de coordenadas o combinación de rutas automática.

## 2. Evidencias cuantitativas

| Concepto | Resultado |
|---|---:|
| XLSX | 9 |
| Hojas | 10 (9 con candidatos, 1 vacía) |
| Filas con valores | 7,053 |
| Filas candidatas | 7,043 |
| Postes / excedentes / cajas / Registro | 6,694 / 292 / 56 / 1 |
| Partes de medios / anclas | 9,563 / 10,003 |
| Fuera de rango mundial / no interpretables / variantes sintácticas | 10 / 13 / 3 |
| Triples literales distintos globales | 5,177 (no equivalen a activos únicos) |
| Repeticiones adicionales dentro de hojas | 558 |
| Señales de discrepancia auxiliar | 1,203 (484 solo de precisión; 719 otras) |
| Reproducción literal STD-MIRADOR | 551/551 registros en orden |
| Reproducción literal STD-OTAY-FLORIDO | 968/969; 969/969 al normalizar solo espacio doble |

Los 7,043 candidatos **incluyen copias, versiones y registros repetidos**. Los datos permiten reconstruir la extracción histórica, pero no demuestran exactitud geográfica ni conectividad de red.

## 3. Familias de entrada y alcance del parser

- **F1_NOMBRE_ABC:** `Nombre`, `elemento`, `coordenandas completas` (A:C), con auxiliares D:E.
- **F2_RUTA_ABC_FOTO_D:** `Ruta`, `Elemento de Red`, `Coordenadas` (A:C), imagen en D, auxiliares E:H.
- **F3_NUMERO_BCD:** numeración A, ruta B, tipo C, coordenadas D, fotografía E y auxiliares F:I. Incluye una columna D1 sin encabezado y hojas con resúmenes/fórmulas adicionales.
- **F4_DESPLAZADO_BCD:** ruta B, tipo C, coordenadas D, fotografía E y auxiliares F:I, sin identificador en A.

El detector debe reconocer **estructura**, no nombres de archivo, y rechazar una estructura no reconocida con error explícito. El diseño basado en lectura secuencial OOXML es razonable para los libros grandes; aún faltan pruebas de memoria, tiempo y resiliencia con implementación real.

## 4. Resoluciones técnicas recomendadas, sin alterar reglas de negocio

1. **Inmutabilidad y linaje:** mantener originales de `Auditorias-20261104T035633Z-1-001/postes/` en solo lectura. Conservar SHA-256, archivo, hoja, fila y valores literales. Las imágenes no son un campo de salida CSV.
2. **CSV mínimo:** conservar las tres columnas `Ruta,Elemento de Red,Coordenadas`, con encabezado, UTF-8 y escape CSV válido. Registrar en lateral el linaje y motivos de calidad. La codificación exacta de tipos en el CSV es una decisión por confirmar: `POSTE/CAJA_EMP/EXCEDENTE` rompería la comparación literal con `poste/cajadedmpalme/excedente` sin un adaptador.
3. **Coordenadas:** el texto geográfico completo es la fuente primaria propuesta; auxiliares son evidencia diagnóstica. Admitir variantes de espacios N/W solo con regla documentada. Nunca insertar puntos decimales o reemplazar caracteres por suposición. No proyectar todavía.
4. **Versiones y solapes:** seleccionar fuentes por auditoría mediante manifiesto ordenado. No combinar automáticamente `Postes_CFE`, Natura, FLO-OTAY-BOMBEROS y las subrutas; tampoco incluir la copia STD de 181 junto al STD de 204 sin decisión.
5. **Duplicados:** registrar todas las ocurrencias; no eliminar por latitud/longitud. Distinguir duplicados de filas fuente, coincidencias entre libros, infraestructura compartida y errores comprobados. La incidencia `DUPLICADO_LITERAL` no debe bloquear sistemáticamente toda la extracción sin una regla de negocio explícita.
6. **Dos modalidades de comprobación:** (a) replay literal de extracción histórica, para confirmar lector y orden; (b) exportación validada, con bloqueo o revisión de coordenadas según contrato final. No exigir que ambas salidas tengan el mismo número de registros si la segunda aplica controles nuevos.
7. **Límites de escritura:** toda implementación futura debe vivir en `AuditoriaCFE/`; los XLSX y entregables de `Auditorias-20261104T035633Z-1-001/` permanecen intactos.

## 5. Observaciones que requieren cierre

| Asunto | Evidencia | Resolución propuesta |
|---|---|---|
| Mirador: 56 frente a 58 duplicados | `06_regresion...` usa triples literales y obtiene 56; el AS-IS anterior indicaba 58 | Identificar las dos ocurrencias que difieren y publicar ambos criterios de conteo antes de declarar reconciliada esa métrica |
| Versiones STD | Copia de 181 incluida en libro de 204 | Usar libro de 204 para regresión histórica; mantener copia como caso de prueba, sin declararla obsoleta a nivel empresarial |
| Etiqueta `Registro` | Una ocurrencia en FLO-OTAY final | Conservar como `REVISAR` hasta determinar categoría física y tratamiento CAD |
| Coordenadas imposibles y atípicas | 10 imposibles, 13 no interpretables, al menos 13 fuera de ventana exploratoria | No corregir ni suprimir. Definir ámbito por auditoría, no una ventana fija de ciudad si puede haber rutas más extensas |
| Auxiliares | 1,203 señales; a menudo magnitudes sin decimal o precisión diferente | No usarlos como coordenada autoritativa; distinguir avisos informativos de bloqueos |
| Orden | Filas y `Numero` no prueban conectividad | Conservar orden de extracción, sin generar aristas ni dibujar polilíneas en esta fase |
| Nomenclatura de fase | Encargo denomina próximo extractor «Fase 1B»; TO-BE v0.1 reserva 1B para topología | Llamar siguiente trabajo **«Implementación del extractor ETL (Proceso 1A)»**; mantener topología como Proceso 1B |

## 6. Selección para pruebas de implementación (propuesta técnica)

**Pruebas piloto, no selección productiva:**
- `CFE FLO-OTAY-BOMBEROS.xlsx`: F1, 494 candidatos, dos rutas, sin medios.
- `ruta via rapida interc STD CC CALZ DEL TECNOLOGICO FO72.xlsx`: F2, 44 candidatos, fotografías y auxiliares numéricos sospechosos.
- `Ruta canal 12 level antes 2014 Completo.xlsx`: F3, 347 candidatos, 1,048,576 filas XML y medios pesados.
- `Natura  - Datra.xlsx`: F4, 507 candidatos, columnas desplazadas; incorporar después de las primeras tres pruebas.

**Regresiones de extracción:** Mirador = STD 204 + Canal 12 347, en ese orden; Otay–Florido = Vía Rápida 44 + FO96 final 622 + Protección Civil 303. Los archivos fuente se identifican por sus rutas relativas completas del inventario, no por abreviaturas de este apartado.

## 7. Checkpoint de decisión antes de Codex

**Listo para aprobación técnica:** contratos de linaje, estructura de tres columnas, streaming OOXML, tratamiento de imágenes como metadatos, detector de cuatro familias, comparaciones duales, restricción de no modificar originales.  
**Pendiente de aprobación del responsable:** equivalencias de categorías, `Registro`, duplicados/activos únicos, fuentes por auditoría, equivalencias de rutas, alcance geográfico, normalización sintáctica admisible, tratamiento de filas válidas pero atípicas y cuándo una incidencia bloquea la exportación.  
**Próximo trabajo autorizado solo tras decisión:** implementar y probar el extractor XLSX→CSV en modo local, con linaje y reporte de calidad. No implementar todavía topología, proyección, CAD, DWT ni la auditoría general completa.
