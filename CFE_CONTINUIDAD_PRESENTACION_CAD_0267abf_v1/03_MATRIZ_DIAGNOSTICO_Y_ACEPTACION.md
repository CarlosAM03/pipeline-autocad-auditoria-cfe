# Matriz de diagnóstico y aceptación — presentación CAD

| Prueba | Evidencia requerida | Resultado que cuenta como OK | Estado actual |
|---|---|---|---|
| D01 Layout | Captura CTAB, inventario de layouts y manifiesto del plot | PDF emitido desde `DATRA_A1`; `Layout1` no sustituye la prueba | Pendiente de repetir/contrastar |
| D02 Modelo | CSV proyectado/diagnóstico + extracción de INSERT de Model por ID | Exactamente misma cantidad, coordenadas y tipos; sin transformaciones visuales ocultas | Core reporta conteos; cotejo por muestra independiente pendiente |
| D03 CRS | Dos puntos no coincidentes WCS/GPS, tolerancia acreditada | Residuos dentro de tolerancia aprobada | P06 pendiente |
| D04 Extremos | Distribuciones, bbox total, bbox robusto y mapa de outliers | Ningún dato excluido por motivos de presentación | Pendiente |
| D05 Viewport | Rectángulo Paper, cámara, lock, orientación, centro y escala | Encuadre completo de símbolos y textos, sin perder mapa | Pendiente |
| D06 Símbolos | Dimensiones nativas Model y mm en A1 | Escala de bloques independiente del texto, correcta y consistente según propuesta aprobada | Pendiente |
| D07 Etiquetas | Medición automática de colisiones + 3 renders A1 con muestras | IDs y coordenadas legibles en zonas densas y aisladas; cero recortes relevantes | Pendiente; Mirador presenta solapamientos |
| D08 Cajetín | ATTRIB nativos y render de columna derecha | `TOTAL_POSTES/CAJAS/EXCEDENTES` coinciden con el manifiesto | Reportado por Codex, revisión visual humana pendiente |
| D09 Paneles | Inspección de 5 recuadros y fuentes | Detalles aprobados o explícitamente no homologados, sin prometer FINAL | Pendiente |
| D10 PDF | Documento PDF real, `pdfinfo`, PyMuPDF, render comparado | A1 1 página y contenido vectorial sin recortes ni glifos perdidos | Piloto reportado OK técnico; aceptación de presentación NO |
| D11 Seguridad | Hash copia, reporte de preservación, comandos nativos | Originals inmutables, dos SCR, sin alterar otras auditorías | Reportado en piloto; repetir tras cambios |
| D12 Idempotencia | Dos ejecuciones de SCR02, XDATA y hashes | Misma cardinalidad e IDs, sin elementos huérfanos | Reportado en piloto; repetir tras cambios |

## Artefactos mínimos del próximo ensayo

`diagnostico_layouts.json`, `diagnostico_modelo.csv`, `diagnostico_viewport.json`, `metricas_etiquetas.csv`, `outliers_para_revision.csv`, `reporte_comparacion_A1.md`, `capturas/` y `pdf/` auténticos, `SHA256SUMS.txt`, `manifest.json`, diff de código, suite y Core Console logs. Puede ser un ZIP privado optimizado de **menos de 15 MiB** sin XLSX originales, KMZ ni DWG grandes. No reemplazar evidencia completa original: los anexos grandes permanecen locales con hash y ruta.

## Gates

- Presentación técnica solo se aprueba si D01/D02/D05/D06/D07/D08/D10/D11/D12 pasan en copias y el owner revisa el A1.
- D03/P06 es obligatorio para acreditar la superposición con cartografía. Sin él, los resultados siguen diagnóstico no verificado.
- D09/P07 y P08 requieren decisión sobre contenido y legibilidad; la evaluación automática no puede cambiar estas reglas.
- P05 sigue siendo autoridad independiente para aristas reales.
