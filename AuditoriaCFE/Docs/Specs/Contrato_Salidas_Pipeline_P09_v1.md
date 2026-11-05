# P-09 — Contratos operativos versionados de Pipeline CFE/DATRA

**Estado:** reglas funcionales ratificadas Q10–Q19, Q72; detalles internos pendientes de implementación y prueba de compatibilidad.
**Precedencia:** ADR-000 + ADR-001. El archivo v0.2 existente sirve como oráculo, no se reescribe silenciosamente.

## 1. Compatibilidad y reglas comunes

- CSV UTF-8 sin BOM, estándar `csv.writer`, CRLF estable, encabezado obligatorio, orden determinista. No utilizar `split(',')` ni parsear nombres como coordenadas.
- Precisión decimal para identidad; no redondeo como clave física. Un elemento puede tener varias rutas pero solo una fila física deduplicada.
- Los registros originales y sus descartes permanecen íntegros en `linaje_y_calidad.jsonl` y `reporte_incidencias.csv`.
- Todo CSV lleva versión del esquema en **manifiesto**, no encabezados extra que rompan el archivo 01.

## 2. CP-01 — `00_elementos_unificados.csv` (v1)

**Ratificado sin cambiar el encabezado de 12 campos ya implementado:**

```csv
elemento_id,ruta_prevalente,tipo,coordenada_original,coordenada_interpretada,estado_preparacion,admision_geografica,apto_csv_01,archivo_prevalente,hoja_prevalente,fila_prevalente,ocurrencias
```

Sigue siendo la vista deduplicada de grupos **identificables**: incluye grupos aún pendientes de aprobación P-03, porque el primer checkpoint no puede vaciarse cuando falta el perímetro. `apto_csv_01=NO` impide uso CAD. No contiene rechazos imposible identificar ni entidades fuera de alcance. Mantener `elemento_id` y los conteos anteriores estables cuando los inputs no cambien.

### Nuevo `00_elementos_revision.csv` (auxiliar, no quinto checkpoint)

Contrato v1 propuesto:

```csv
revision_id,elemento_id,ocurrencia_id,auditoria,archivo,hoja,fila,tipo_original,coordenada_original,codigo_incidencia,estado_actual,accion_requerida,fuente_evidencia,resolucion_id
```

Su objetivo es una **bandeja clara** con casos no admitidos, anulaciones explícitas, geografía fuera de zona, identificadores ambiguos y rechazos; no contiene filas de producción duplicadas para inflar inventario. La revisión P-03 **global** puede reflejarse como tarea de lote y/o filas vinculadas sin hacer desaparecer del CSV 00 los elementos con coordenadas interpretables. Nunca introducir `revision_id` en el CSV 01.

## 3. CP-02 — `01_elementos_normalizados.csv` (v1, INALTERABLE)

```csv
Ruta,Elemento de Red,Coordenadas
```

Una fila única por componente admitido, ruta prevalente literal, tipos POSTE/CAJA_EMP/EXCEDENTE, posición geográfica en N/W normalizada sin pérdida de precisión de identidad. Sin P-03 aprobado, solo encabezado si no hay admitidos. Las excepciones aprobadas se documentan en resoluciones e incidencia.

## 4. CP-02 — `02_elementos_proyectados.csv` v1 y v2

**v1 existente, mantener lector y oráculo:**

```csv
elemento_id,ruta_id,tipo,latitud,longitud,este_m,norte_m,crs
```

En v1, `ruta_id` contenía nombre literal. **No cambiar su significado bajo la misma versión**.

**v2 nueva, explícita en manifiesto para generador CAD:**

```csv
elemento_id,ruta_id,ruta_nombre,tipo,latitud,longitud,este_m,norte_m,crs
```

`ruta_id` se calcula de forma estable sobre auditoría + nombre literal normalizado de modo inequívoco con versión de algoritmo; `ruta_nombre` conserva el literal prevalente. Asociación de rutas múltiples se modela aparte. La migración no cambia `elemento_id` ni crea duplicados. El código debe aceptar v1/2 durante transición, **no forzar una ruptura silenciosa del archivo 02 sin reportarlo**.

**CRS gate:** sin evidencia CAD de dos controles, NO generar este CSV como validado. Una proyección candidata puede vivir en un archivo de diagnóstico de nombre diferente, visible como no aprobada, sin entrar en downstream productivo.

## 5. Entradas de revisión (ignorado por Git si contienen datos reales)

### `entrada/resoluciones_manual.csv`

```csv
resolucion_id,archivo_sha256,archivo_relativo,hoja,fila,valor_original,campo,accion,valor_nuevo,motivo,evidencia,responsable,fecha,aprobada
```

Acciones: `EXCLUIR`, `CORREGIR_COORDENADA`, `CORREGIR_TIPO`, `EXCEPCION_AMBITO`, `ID_EQUIPO_ACREDITADO`; cada una tiene precondiciones, precisión y motivo. `CORREGIR_*` exige evidencia individual verificable; `EXCLUIR` no suprime registro/linaje. Resolver conflictos de varias acciones sobre la misma fila como error, no aplicar última silenciosamente. No aceptar `aprobada=true` solo porque la escribió el algoritmo; proviene del owner y debe llevar fecha/soporte.

### `entrada/topologia_confirmada.csv`

```csv
arista_id,origen_id,destino_id,ruta_id,tramo_id,clase,evidencia,responsable,fecha_aprobacion,estado
```

Solo `estado=CONFIRMADA` y evidencia identificable autorizan dibujo de ruta física. IDs de elementos deben existir en CSV 00/01/02 admitidos; origen≠destino, deduplicar arista sin perder pertenencia a subrutas. Fuentes KMZ y proximidad nunca escriben por sí solas una confirmación. `topologia_propuesta.csv` incorpora origen, destino, ruta, score/método, distancia y geometría fuente, siempre `NO_CONFIRMADA`.

### `entrada/ambito_geografico.geojson` o KML aprobado

Polígono/corredor por auditoría, CRS y versión conocidos, aprobador, fecha y evidencia verificable. CRS esperado de GeoJSON WGS84; validar anillos, antimeridiano si aplica, límites globales y exclusión de geometrías inválidas; no desplazar automáticamente coordenadas. Rectángulos de configuración existentes siguen funcionando con advertencia si no tienen evidencia.

## 6. Otros auxiliares (conservar y ampliar sin borrar)

- `summary.csv` conserva campo de novedad vs baseline, coincidencia con maestro informativa, prevalente e incidencias.
- `linaje_y_calidad.jsonl` por ocurrencia con SHA, fuente, hoja, fila, original, modificaciones autorizadas y estado.
- `reporte_incidencias.csv`, `asociaciones_elemento_ruta.csv`, `resumen_conteos.csv`, `coordenadas_cercanas.csv`.
- `topologia_propuesta.csv` puede estar vacío si falta evidencia. No ocultar vacío ni dibujar líneas ficticias.
- `perfiles_hojas.jsonl` y `filas_no_operativas.jsonl`, sin cargar medios.
- `reporte_validacion_cad.json`, `reporte_topologia.json`, `reporte_papel_A1.json`, `checklist_entrega.md` por auditoría cuando corresponda.
- `01_configurar_plano.scr`, `02_dibujar_auditoria.scr` generados solo con inputs/verificaciones permitidos.

## 7. Manifiestos y publicación (Q72)

Destino futuro: `auditorias/<auditoria>/salida/manifiesto_ejecucion.json` (activo) y `salida/manifiestos/<ejecucion_id>.json` (historial), contenidos en la publicación por lote. **No incluir el hash del manifiesto dentro de su propia lista** para evitar autorreferencia. El verificador valida hashes/tamaños de artefactos, schema, procedencia, estado, modo diagnóstico, versión/config, y que la publicación provenga de una sola ejecución. Temporales técnicos efímeros se conservan fuera de salida si son necesarios para `os.replace` y se limpian sin afectar corridas.

Los manifiestos antiguos fuera de entrada/salida deben leerse y validarse para una migración reversible. Si la migración falla, no destruir ni sobrescribir el activo anterior. Solo al confirmar resultado mover la autoridad al manifiesto en `salida`.

## 8. Reconciliación y privacidad

- Total ocurrencias = prevalentes + duplicados + revisiones sin identidad + rechazados + fuera de alcance; cada código tiene motivo auditable.
- Grupos de 00 y filas de revisión se reconcilarán sin dobles conteos de componentes físicos.
- Filas 01 = únicos admitidos; filas 02 productivo = filas 01 cuando hubo aprobación P-06.
- Conteos por símbolos CAD deben coincidir con entidades realmente insertadas, no con ocurrencias históricas ni `POINT` heredados.
- Los datos operativos (KMZ, coordenadas privadas, aristas, resoluciones, salida y manifiestos) están ignorados por Git por directorio; verificar **qué paths son realmente rastreados** antes de crear un PR público.
