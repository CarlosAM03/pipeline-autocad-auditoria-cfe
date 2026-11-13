# Checkpoint A4.1.1 — Doce variantes disponibles para revisión

**Ejecución experimental completa.** Natura, Mirador y Otay–Florido tienen cuatro variantes cada una, a 50, 100, 200 y 300 m. Se verificaron los 12 DWG editables, 12 PDF consolidados, 126 páginas vectoriales, 12 CSV y resúmenes de exclusiones y 24 XLSX de trazabilidad. Cada variante dispone de dos SCR, LISP, índice, configuración, manifiesto y SHA-256. Se conservó el inventario de 1 680 identidades originales.

Ruta privada `AuditoriaCFE/auditorias/_comparativa_A4_1_1/`. Las tres carpetas principales contienen las variantes y su comparativa. Los DWG y PDF de cada variante están dentro de `resultados_cad/`. La raíz contiene la comparativa global, la matriz privada por ID, el GeoJSON y su procedencia. Los recortes huérfanos se toman de la línea base y, cuando el sector cae dentro de una ventana filtrada, se incluye una imagen comparativa de contexto.

**ZIP privado:** `A4_1_1_REVISION_PRIVADA.zip`, 1 884 324 bytes, SHA-256 `3b4fe1bd7c3dc356e09a8b76bb930a659dc4d2e2dd7b48d1135bdb9015094a1c`. CRC y hashes verificados. Los PDF y DWG completos permanecen en cada variante.

El radio de 50 m deja fuera de la vista 397 identidades de Natura, 224 de Mirador y 432 de Otay–Florido. Mirador y Otay–Florido conservan exactamente el mismo conjunto a 200 y 300 m, aunque el grafo auxiliar puede cambiar. En el contraste AGEM se marcaron 14 identidades en Mirador y 3 en Otay–Florido. Coinciden con exclusiones en los cuatro radios por la regla de proximidad, independientemente del territorio. La selección de un radio requiere revisar representatividad, subrutas y evidencia de campo.

Rama `codex/etl-unificado-auditoria-js`. Base `acba0630d8be752877396113cf418ba3b706a376`, implementación `0d478ac25c23b7677e39d4ea9b080dfdbd644818`. Los resultados privados quedan fuera del índice. La rama pública conserva exclusivamente código, pruebas y resultados agregados. PR #1 abierto, sin fusión.

El responsable conserva la decisión de radio, recuperaciones manuales y eventuales fusiones. Las auditorías continúan PRELIMINARES. La recuperación constructiva A4.2 queda fuera de este checkpoint.

- [Resultados](RESULTADOS_12_VARIANTES.md)
- [Comparativa de doce variantes](COMPARATIVA_GLOBAL_A4_1_1.csv)
- [Estadística de distancias](ESTADISTICA_DISTANCIAS.md)
- [Pruebas y regresiones](PRUEBAS_Y_REGRESIONES.md)
- [Instrucciones de revisión](INSTRUCCIONES_REVISION_12_PDFS.md)
