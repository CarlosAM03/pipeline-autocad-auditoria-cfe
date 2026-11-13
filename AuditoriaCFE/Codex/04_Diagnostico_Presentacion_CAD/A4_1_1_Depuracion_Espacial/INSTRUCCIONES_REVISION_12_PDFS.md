# Revisar y reproducir los 12 PDF

Abrir la carpeta privada `AuditoriaCFE/auditorias/_comparativa_A4_1_1`. Cada auditoría tiene carpetas 050m, 100m, 200m y 300m. El PDF consolidado y su DWG están dentro de `resultados_cad`. Las hojas originales trazadas, capturas y logs están en `resultados_cad/evidencia`.

Comparar primero la vista general y después los detalles indicados por `indice_presentacion.csv`. Verificar qué quedó fuera mediante `COORDENADAS_DESCARTADAS_VISUALIZACION.csv`, las ocurrencias afectadas y el recorte huérfano de referencia. El índice, las asociaciones y el linaje identifican subrutas. Los dos libros de cada radio añaden la pestaña Decision_Visual. La matriz privada conserva el resultado para cada ID en los cuatro radios. La matriz del directorio documental muestra patrones agregados por tipo para la rama pública.

Para regenerar, preservar el directorio previo en el almacenamiento privado y usar un directorio de comparación nuevo, con los lotes A4_1_r5 intactos. Desde la raíz, con la venv del proyecto ejecutar, en este orden:

```powershell
python AuditoriaCFE/herramientas/comparativa_espacial.py --territorio <archivo-local-geojson>
python AuditoriaCFE/herramientas/ensayo_comparativa_espacial.py
python AuditoriaCFE/herramientas/cerrar_comparativa_espacial.py
```

El ensayo requiere AutoCAD Core Console 2026, Poppler y PyMuPDF. También se puede abrir cada DWG virgen de la variante, ejecutar SCR01 y SCR02, y publicar los layouts de la variante en el orden de `presentacion_paginas.json`. Verificar los hashes del manifiesto antes de compartir.
