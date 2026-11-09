# Revisión independiente — A3 / Presentación CAD Mirador

**Corte examinado:** PR #1 `codex/etl-unificado-auditoria-js`, cambios de checkpoints en `bdc8a56`, corrección de política de publicación en `ebe2d861464d91ea8d04c8363eaac8b71bfe81e5`. **Auditoría:** Mirador, DIAGNÓSTICO NO VERIFICADO; nunca FINAL.

## Evidencia y método

Se recibieron `V1.zip`…`V4.zip`, `COMPARATIVA_VARIANTES.csv`, `METRICAS_VARIANTES.json`, `SHA256SUMS.txt` y versiones reescaladas de las páginas. Se comprobó CRC de los cuatro ZIP, SHA-256 de cada PDF y de las evidencias disponibles, se abrieron los PDF directamente con Poppler (`pdfinfo`) y PyMuPDF y se examinaron las cuatro imágenes `densa.png`, `aislada_norte.png`, `aislada_oeste.png` y la página completa de cada variante.

Los cuatro PDF auténticos tienen una página ISO A1 horizontal de aproximadamente 841.022 × 594.078 mm, versión PDF 1.7, son renderizables y no contienen imágenes raster incrustadas. Estos controles validan el archivo PDF, **no** la legibilidad de todas las etiquetas ni la exactitud de la georreferenciación.

La comparación de hashes validó **62 recursos** presentes y enumerados en el manifiesto entre los cuatro ZIP y los dos archivos auxiliares. Los cuatro `.bak` de los ZIP no aparecen en `SHA256SUMS.txt`. **Nueve auxiliares adicionales** que sí figuran en el manifiesto original no fueron adjuntados, por lo que no se afirma la comprobación de la totalidad de las 71 entradas de origen. Las cuatro copias `.bak` y `.dwg` no se necesitan en el nuevo paquete ligero.

## Cuatro variantes (observación visual + métrica AABB de Codex)

| Variante | Etiquetas activas | Intersecciones AABB potenciales entre pares | Evaluación |
|---|---:|---:|---|
| V1 — Solo símbolos | 0 | 0 | Evidencia útil de la concentración geográfica; no acredita presentación final |
| V2 — Identificadores | 493 | 45,858 | Gran conglomerado negro: ilegible en zona densa |
| V3 — Coordenadas | 493 | 42,360 | Acumulación de cadenas largas: ilegible en zona densa |
| V4 — Completa | 986 | 122,441 | Superposición de ambas clases y ocultamiento de mapa/símbolos: **NO APTA PARA ENTREGA** |

Los conteos de 493 elementos (414 POSTE / 20 CAJA_EMP / 59 EXCEDENTE) y cero aristas coinciden con las métricas y el informe previo. El cajetín `DATRA_A1` muestra los tres totales. No se repitió el ETL con originales; la identidad y posición en DWG son el resultado de inspección nativa **reportado** por Codex, no una comparación independiente de XDATA reconstruida a partir del DWG en AutoCAD.

Los recortes de **norte aislado** demuestran que las etiquetas sí se leen cuando están separadas. Los recortes de **oeste aislado** muestran cruces entre etiquetas de dos puntos incluso fuera de la nube principal. En la zona **densa**, V1 ya está sobrecargada por los componentes cartográficos heredados y los símbolos; V2–V4 generan bandas negras por textos vectoriales. No es un fallo del motor PDF.

Las métricas entregadas indican que 473/493 centros (≈95.9 %) están en el rectángulo percentil p1–p99 de ~88.96 × 35.55 mm, solo 1.28 % del área del viewport. El rectángulo de todos los centros ocupa ~42.01 % del viewport. **No** son estimaciones de superficie ocupada por tinta, y los 122,441 pares AABB son colisiones potenciales de cajas, no encuentros exactos de glifos.

### Hallazgos de presentación

1. **P-01 BLOQUEANTE:** La presentación V4 no es legible en zonas densas; debe bloquearse cualquier entrega FINAL.
2. **P-02 IMPORTANTE:** La política de encuadre de todos los extremos reduce el espacio útil de la nube principal. No autoriza recortar ni corregir puntos: P03 y los controles físicos P06 siguen pendientes.
3. **P-03 IMPORTANTE:** El algoritmo acopla zoom/viewport y tamaño de INSERT, IDs y coordenadas mediante `s` y `h` (`cad.py` y `cad_runtime.lsp`). Separar parámetros es una alternativa técnica para A4, no una decisión visual ya aprobada.
4. **P-04 IMPORTANTE:** La leyenda EXCEDENTE (triángulo) difiere de su bloque v1; falta decidir cuál prevalece. Los cinco paneles constructivos y la ubicación permanecen vacíos.
5. **P-05 IMPORTANTE:** La plantilla DATRA vigente cambió de hash entre los checkpoints A0–A2 y A3. Las variantes son comparables entre sí porque usaron una única copia de piloto, pero antes de aplicar correcciones se debe establecer la versión base autorizada y verificar diferencias de plantilla.
6. **P-06 MENOR:** PyMuPDF extrae exactamente los mismos 372 caracteres de texto de mapa de los cuatro PDF, pese a que V2–V4 muestran etiquetas nuevas. Los IDs/coordenadas se dibujaron visualmente como geometría vectorial, **no son recuperables como texto seleccionable mediante esa extracción**. La trazabilidad sigue disponible en CAD/XLSX; si se exige buscabilidad en PDF, es una decisión/solución aparte.
7. **P-07 TRAZABILIDAD:** A3 informa que tres rutas XLSX históricas del inventario A0–A2 ya no existían en su ubicación y que la plantilla actual tenía un hash diferente antes de A3. No atribuir esos cambios a Codex sin un registro de operaciones.

## GitHub / CI

El commit `bdc8a56` falló en los ocho jobs por `verificar_publicacion.py`: un PDF nuevo rastreado estaba prohibido por el guardia. El owner retiró el PDF del índice en `ebe2d86` y lo excluyó por `.gitignore`. Se comprobó GitHub: el PR #1 sigue abierto, sin merge, y **ambos workflows nuevos (push y PR) están verdes, cuatro jobs por ejecución**. En un job de PR Linux py3.10 se ejecutaron 93 tests con 9 omisiones históricas (84 ejecutados satisfactoriamente). La corrección de CI no modifica la generación CAD.

## Conclusión y contrato recomendado para A4

**A3 está suficientemente demostrado para pasar a la definición de alternativas de presentación, NO a la liberación de un plano.** No se deben modificar CRS, X/Y, elemento_id, deduplicación, topología, CSV/XLSX o historial. Mirador sigue PRELIMINAR con cero aristas confirmadas.

Antes de diseñar parámetros definitivos, solicitar al owner: (a) versión de la plantilla DATRA a preservar; (b) jerarquía entre vista general única y legibilidad de cada etiqueta, y si se permiten llamadas/despieces dentro de la misma lámina A1; (c) contenido/representación final de leyenda y paneles; (d) política de tratamiento documental de puntos aislados, **sin descartarlos ni moverlos**. En tanto no estén aprobados, A4 debería producir comparativas de alternativas **solo en copias**, mediciones y un ADR/decisión pendiente, sin editar el runtime de producción.

Opciones técnicas a evaluar, no aprobadas: desacoplar `viewport_scale`, `block_size_mm`, `id_height_mm`, `coord_height_mm`, offsets y anotaciones de alta densidad; ensayar líder/callout con IDs trazables; usar insets o tabla referenciada dentro de la misma hoja si el contrato lo permite; gestionar el exceso de densidad como gate explícito en vez de ocultarlo. No prometer que reducir letras resolverá la concentración.

**Fuentes:** cuatro PDF auténticos y sus recortes recibidos; `METRICAS_VARIANTES.json`; `COMPARATIVA_VARIANTES.csv`; `SHA256SUMS.txt`; checkpoints A0–A2 y A3 publicados en el commit `bdc8a56`; estado de workflows de `ebe2d86` obtenido de GitHub. No se inspeccionaron originales privados XLSX/KMZ ni se ejecutó AutoCAD local en esta revisión.
