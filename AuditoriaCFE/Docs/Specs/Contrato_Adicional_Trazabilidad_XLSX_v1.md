# Contrato aditivo de trazabilidad XLSX v1

Extensión solicitada para el piloto PR #1, 2026-11-05. No sustituye P-09 v1
ni modifica CSV00 (12 columnas), CSV01 (3 columnas) o CSV02 v1/v2.
La aceptación del diseño de presentación por el owner queda pendiente.

Los perfiles integrales generan `01_trazabilidad_limpieza.xlsx` y
`02_trazabilidad_transformacion.xlsx`. Son productos visibles adicionales,
no nuevas entradas al ETL. Los dos SCR siguen siendo los únicos pasos CAD.

| Libro | Hojas y fuente de la misma corrida |
|---|---|
| Limpieza | Resumen: conteos del manifiesto; Unificados: CSV00; Revision: bandeja CSV; Incidencias: reporte CSV; Linaje: una fila por ocurrencia JSONL; Fuentes_Hashes: hashes/tamaños de derivados y fuentes |
| Transformación | Resumen_Gates: estados del manifiesto; Admision_P03: CSV01; Proyeccion_Validada: CSV02 o solo encabezado; Proyeccion_Diagnostica: CSV diagnóstico separado o encabezado; Asociaciones_Rutas: CSV; Topologia_Propuesta: CSV; Topologia_Confirmada: asociaciones de aristas aceptadas por el mismo validador |

Resumen y Resumen_Gates son las primeras pestañas. Las hojas vacías contienen
solo encabezado; la explicación queda en Resumen_Gates, sin filas ficticias.
`DIAGNOSTICO_NO_VERIFICADO` no acredita CRS ni conectividad. La hoja Linaje
conserva campos originales, interpretados, fuente/hoja/fila/hash, prevalente,
resolución e incidencias. Los objetos anidados se serializan como JSON textual.

Todas las celdas son `inlineStr` con formato Excel texto, incluidos IDs,
coordenadas, conteos y valores que empiezan por `=`, `+`, `-` o `@`. No hay
fórmulas, macros, vínculos externos, medios ni hojas ocultas. Límite Excel de
32 767 caracteres por celda: error explícito, nunca truncamiento silencioso.
Encabezados congelados, autofiltros y anchos limitados permiten inspección.

Diseño prototipado e inspeccionado con Artifact Tool; el emisor Python usa
OOXML estándar con biblioteca estándar para funcionar también en CI sin
dependencias del entorno Codex. ZIP interno ordenado, timestamp fijo 1980,
sin propiedades de autor/fecha volátiles: determinismo binario verificable.

`fuentes_derivadas_id` es SHA-256 canónico del inventario de CSV/JSONL/JSON
ya emitidos antes de los libros. No incluye los libros ni el manifiesto final:
evita autorreferencia. El manifiesto final incluye los hashes/tamaños de ambos
XLSX, junto con entradas, configuración, código y ejecución. No se recalcula
identidad ni transformación dentro del exportador.

Aceptación técnica: reconciliar filas contra cada CSV/JSONL, probar precisión
textual e inyección de fórmula, abrir OOXML y renderizar sus 13 hojas, comparar
dos corridas byte a byte y comprobar hashes con `--verificar-paquete`.
La apertura interactiva Excel y la presentación definitiva son revisión humana.
