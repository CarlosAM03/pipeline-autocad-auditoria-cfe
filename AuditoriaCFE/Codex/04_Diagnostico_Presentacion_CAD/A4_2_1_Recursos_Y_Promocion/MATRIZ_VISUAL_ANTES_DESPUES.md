# Comparación de las 38 hojas

| Zona | A4.2 | A4.2.1 | Evidencia |
|---|---|---|---|
| Cajetín | Identificación vectorial | Identificación más logo gráfico | 38 comparaciones raster a 160 dpi y verificación de proporción 1:1 |
| Ubicación | Recuadro vacío | PNG general de Tijuana | 38 comparaciones raster a 160 dpi y proporción 4:3 |
| Cartografía, encuadre y paneles | Vectoriales | Misma representación | Comparación píxel a píxel fuera de las dos regiones a 72 dpi en las 38 hojas |
| Tamaño y contenido | A1 horizontal | A1 horizontal vectorial con dos rasters | AutoCAD, Poppler y PyMuPDF |

Los 38 PDF individuales proceden del trazador AutoCAD y se consolidaron por auditoría sin rasterizar la cartografía. Los tamaños medidos en PDF son aproximadamente 22.06 × 22.01 mm y 68.03 × 51.01 mm. Cada recurso tiene el mismo hash de imagen PDF en las 38 hojas. Se inspeccionaron visualmente recortes representativos; la comparación automatizada cubrió todas las hojas. Los recortes completos del logo reproducen el borde ya presente en el PNG fuente.
