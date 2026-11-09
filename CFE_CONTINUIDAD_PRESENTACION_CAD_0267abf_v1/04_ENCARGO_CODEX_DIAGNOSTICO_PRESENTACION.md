# Encargo a Codex — diagnóstico CAD de presentación, SIN modificar datos físicos

## Autoridad y objetivo

Rama actual `codex/etl-unificado-auditoria-js`; corte de referencia `0267abf312d8cbc6da9b927211f7ae4ca96f7524`. Leer `AGENTS.md`, ADR-000 + ADR-001, TO-BE v0.3, P-09, acta del piloto, code review H01-H10 y los archivos de este paquete. Trabajar en COPIAS. No fusionar PR #1 ni cambiar main. No acceder a carpetas de auditorías distintas del piloto salvo para comprobación **solo lectura** de integridad.

### Fase A — reproducir, medir y explicar antes de editar

1. Registrar inventario y SHA de copia DWG, dos SCR, runtime LISP, CAD data LISP, manifiesto, PDF actual y configuración de Mirador. No inventar PDF si el archivo local no existe.
2. Emitir diagnóstico nativo de espacios, unidades, UCS/WCS, `CTAB`, layout activo, viewports, cajas de vista, cámara, zoom, lock, escalas, layers y atributos de cajetín. Comparar explícitamente `Layout1` y `DATRA_A1`.
3. Extraer INSERT propios y etiquetas TEXT de Model con XDATA y **compararlos contra CSV02 diagnóstico por `elemento_id` y coordenadas**. Si faltan datos, declarar el hallazgo, no corregirlos de oficio.
4. Calcular bbox total y cuantiles de x/y, clasificar outliers para revisión pero no borrar ni desplazar puntos. Medir contenido de mapa original y su relación con puntos de auditoría. No asumir CRS de la base por `INSUNITS`.
5. Calcular dimensiones previstas en papel para bloques y textos a partir del viewport actual; identificar colisiones y recortes con evidencia antes de inferir su causa.

### Fase B — aislar mecanismos visuales

6. Producir cuatro variantes DIAGNÓSTICAS de Paper Space (base con símbolos; base con IDs; base con coordenadas; base completa) con los mismos IDs/posiciones. Las tres simplificadas son solo herramientas de QA, no salida final.
7. Plotear desde `DATRA_A1` en A1 real. Exportar vistas completas y 3 zonas recortadas a misma resolución/escala, con medidas y clases de contenido.
8. Comparar PDF auténticos con dos herramientas de render; detectar glifos, densidad, solapamientos y clipping. Registrar si la presentación de `Layout1` explica alguna discrepancia de las capturas.

### Fase C — propuesta de solución (no imponer decisiones visuales)

9. Proponer **separar parámetros** `symbol_size_mm`, `id_text_height_mm`, `coord_text_height_mm`, `label_offset_mm`, `viewport_padding_mm` del factor de escala de datos. No homologarlos ni cambiar el estilo definitivo sin aprobación del owner.
10. Si se decide implementar refactor puramente técnico, conservar por defecto el aspecto anterior y parametrizar; producir diff y prueba de no regresión. No modificar identidad, normalización, CSV, XLSX, topología, EPSG, DATRA base ni P03/P06.
11. Tratar el incumplimiento de 1 A1/etiquetas completas como **BLOQUEANTE**, y documentar alternativas con consecuencias, no seleccionar por cuenta propia.
12. Repetir tests, benchmark, idempotencia SCR02, recuperación, hash/custodia y ensayo nativo en COPIA.

### Entregables

- `REPORTE_DIAGNOSTICO_PRESENTACION.md` con evidencia por hallazgo: hechos medidos, hipótesis, interpretación y acciones propuestas.
- `MATRIZ_ANTES_DESPUES.csv`: layout, zoom, bbox, alturas en papel, colisiones, recortes, IDs, total postes/cajas/excedentes, 1 A1.
- ZIP privado con manifiesto SHA256, PDF genuinos, vistas pequeñas, logs compactados y JSON/CSV de métricas; objetivo <15 MiB. Si los PDF vectoriales exceden, anexo separado sin degradarlos. Prohibido publicar el ZIP en GitHub.
- Instrucciones para owner: qué ejecutar en AutoCAD GUI, cómo inspeccionar layout, dos controles WCS, cajetín y paneles.
- Un commit o serie de commits focalizados solo si hay correcciones permitidas; PR abierto sin merge; al cerrar indicar SHA y CI real.

### Criterios de no-regresión

No tocar históricos ni copiar resultados de un lote sobre otro; no introducir offsets espaciales arbitrarios; no atribuir conectividad ficticia a Mirador; no alterar contratos de los dos XLSX/CSV ni los dos SCR; no ocultar puntos no admitidos en un producto que pretenda ser FINAL; no declarar P04/P07/P08 cerrados mediante checks programáticos.
