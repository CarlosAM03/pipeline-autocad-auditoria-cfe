# Diagnóstico estático de presentación CAD — `0267abf`

## 1. Separar Model Space y Paper Space

- `cad.py` compila coordenadas `este_m` y `norte_m` de un CSV02 (acreditado) o `02_DIAGNOSTICO_NO_VERIFICADO.csv` (ensayo) en órdenes `datra:point` / `datra:edge`.
- `cad_runtime.lsp` crea los bloques y los textos de cada componente en `Model`, mediante `INSERT`, `TEXT` y `LWPOLYLINE`; el viewport y los rótulos de control se preparan en el layout de salida.
- Un encuadre equivocado **no demuestra** coordenadas erróneas. Primero verificar las posiciones y distancias de objetos de Model contra el CSV fuente, después mirar las cámaras de Paper.
- Una captura obtenida en `Layout1` **no es comparable automáticamente** con el plot que el runtime declara como `DATRA_A1`.

## 2. Fórmulas actuales — evidencia directa del código

**`cad.py` (aprox. líneas 133-146):**

```python
scale = max((xmax-xmin)/410, (ymax-ymin)/445, 0.01)
height_model = max(scale * 3.0, 0.05)
```

Esta misma variable `datra:*height*` alimenta las alturas de TEXT y, mediante los factores 41/42/43, la escala de los bloques. Por tanto, cambiar la extensión de puntos puede cambiar **simultáneamente** textos y símbolos; no son parámetros independientes. La escala calculada es una **propuesta visual** y no una aprobación de legibilidad.

**`cad_runtime.lsp` (aprox. líneas 302-334):**

- Fija un viewport de Paper Space entre `(145,70)` y `(675,535)` mm, tamaño nominal **530 × 465 mm**.
- Crea `MVIEW`, entra a `MSPACE`, activa `UCS World` y `PLAN World`.
- Usa `ZOOM Center` con una altura calculada como `465*scale`.
- Desplaza el centro a +`50*scale` en X para dar margen a los textos situados al este de sus símbolos; verificar el resultado sobre el PDF, no asumir que el margen basta para cadenas largas.
- Bloquea el viewport con `MVIEW Lock On`.

**`cad_runtime.lsp` (aprox. líneas 174-182):**

- Crea un bloque de tipo P/C/E, texto de identificación y coordenada textual en `Model`.
- El número de etiqueta está ligado al `elemento_id`, no a la secuencia espacial.
- En densidad elevada habrá solapamiento incluso si cada coordenada WCS es correcta.

## 3. Riesgos que la evidencia visual debe discriminar

| Hipótesis | Qué medir | Qué NO hacer aún |
|---|---|---|
| H-V01: layout equivocado | `CTAB`, nombre layout trazado en log PDF y metadatos `LAYOUT` | Alterar Model para que `Layout1` se vea bien |
| H-V02: bbox contaminado por puntos extremos | Bbox total, p1/p99 y distancias al grupo; matriz de outliers | Borrar, desplazar o excluir puntos solo por estética |
| H-V03: mapa y puntos en marcos distintos | 2 controles físicos WCS↔WGS84 + tolerancia residual + `INSUNITS` | Inventar offset, escala global o CRS |
| H-V04: símbolos grandes/chicos | Tamaño de INSERT en unidades Model y tamaño impreso mm | Ajustar de forma irreversible el DWG base |
| H-V05: texto amontonado | Pares de bounding boxes de TEXT, capas, tamaño impreso, recortes | Reducir tamaños arbitrariamente sin prueba A1 |
| H-V06: plantilla incompleta | Cajetín, referencias, fuentes, leyenda y 5 paneles | Reemplazar por esquemas no homologados marcados como definitivos |
| H-V07: diferencias por plot | Comparar DWG, layout, viewport, PDF vectorial y raster de QA | Usar solo screenshots como verificación geométrica |

## 4. Experimentos sin cambiar reglas de negocio

Generar sobre COPIAS cuatro variantes de diagnóstico para el mismo lote: (A) mapa con símbolos sin textos; (B) símbolos+IDs; (C) símbolos+coordenadas; (D) presentación actual completa. **Solo (D)** es candidato a entrega si supera todas las validaciones; las otras son lentes de diagnóstico. Mantener los mismos IDs y coordenadas en todas. Exportar imágenes de una misma zona a idéntica escala para aislar el componente que genera el desorden.

La presentación final seguirá siendo **una A1 horizontal** hasta decisión expresa del owner. Si todos los elementos y coordenadas no caben legiblemente, registrar bloqueo de P-08 y proponer alternativas formales; no ocultar etiquetas ni aumentar páginas sin aprobación.

## 5. Referencias verificables

- `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/blob/0267abf/AuditoriaCFE/src/auditoriacfe/cad.py`
- `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/blob/0267abf/AuditoriaCFE/src/auditoriacfe/cad_runtime.lsp`
- `https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/blob/0267abf/AuditoriaCFE/Codex/03_PR1_Piloto_Mirador/ACTA_TRABAJO.md`
