# Contrato de salidas del Proceso 1 — PROPUESTA técnica v0.1

**Estado: propuesta de implementación, no ADR aprobado.** Gobernado por ADR-000 y TO-BE v0.2. Los nombres principales están fijados por la especificación; los campos secundarios que siguen se validarán al checkpoint P-09. No añadir columnas al CSV mínimo.

## Directorio y orden

Cada ejecución elige `AuditoriaCFE/auditorias/<nombre>/entrada/` y escribe exclusivamente en `AuditoriaCFE/auditorias/<nombre>/salida/`. Orden de libros **declarado en `fuentes_en_orden`**, orden de hojas explícito cuando hay varias, filas crecientes. Sin manifestación del orden, no emitir una «corrida productiva».

## 01_elementos_normalizados.csv — estricto

Encabezado **exacto**:

```csv
Ruta,Elemento de Red,Coordenadas
```

- `Ruta`: nombre de la subruta de la ocurrencia prevalente; asociaciones adicionales en archivo separado. Natura puede contener 14 subrutas dentro de una auditoría lógica.
- `Elemento de Red`: solo `POSTE`, `CAJA_EMP`, `EXCEDENTE`.
- `Coordenadas`: latitud y magnitud de longitud WGS84 en grados decimales, N/W. Preservar precisión representable y no redondear para la identidad. Ejemplo de formato, no dato acreditado: `32.52229449N 117.02010997W`.
- Una fila por **elemento físico único admitido de la auditoría**. No exportar `Registro`, duplicados adicionales, inválidos ni elementos con revisión bloqueante.
- UTF-8 sin BOM, con encabezado, campo CSV escapado correctamente. No introducir `id`, lat/long, código de estado ni foto en el CSV mínimo.

## 02_elementos_proyectados.csv — condicionado por CRS

Encabezado técnico propuesto:

```csv
elemento_id,ruta_id,tipo,latitud,longitud,este_m,norte_m,crs
```

- Solo generarlo y etiquetarlo como validado tras evidencia de CRS y puntos de control. Sin validación: manifiesto `CRS_PENDIENTE`, **archivo no generado**.
- Misma cardinalidad de entidades únicas del CSV mínimo, salvo incidencia espacial documentada. IDs deterministas y estables con reglas de serialización versionadas.
- `crs` explícito en cada fila y manifiesto. Un CRS candidato mostrado en el software CAD **no acredita la georreferenciación de las entidades**.
- Proyección con `pyproj.Transformer.from_crs(..., always_xy=True)` y validación de controles. Nunca sumar/descontar 11.5 metros arbitrariamente.

## Archivos auxiliares obligatorios

| Archivo | Esquema mínimo propuesto | Restricción |
|---|---|---|
| `summary.csv` | `elemento_id,auditoria,tipo,ruta_prevalente,estado,coordenada,archivo_prevalente,hoja_prevalente,fila_prevalente,ocurrencias,coincide_maestro,novedad_vs_baseline,observaciones` | Uno por único/caso trazable; no confundir coincidencia con maestro y novedad histórica. |
| `linaje_y_calidad.jsonl` | `ocurrencia_id,elemento_id,archivo_sha256,archivo_relativo,hoja,fila,ruta_original,tipo_original,coordenada_original,latitud,longitud,tipo_canonico,estado,incidencias,prevalente_id` | Una entrada por ocurrencia; duplicados no desaparecen. |
| `reporte_incidencias.csv` | `incidencia_id,codigo,severidad,archivo,hoja,fila,valor_original,valor_elegido,motivo,estado_revision` | Error/recuperación/exclusión con contexto y sin corrección especulativa. |
| `asociaciones_elemento_ruta.csv` | `elemento_id,auditoria,ruta_original,archivo,hoja,fila` | Varias asociaciones para un mismo soporte. |
| `topologia_propuesta.csv` | `propuesta_id,origen_id,destino_id,ruta,tramo,distancia_plana_m,metodo,estado,justificacion` | `estado=PENDIENTE_CONFIRMACION`, nunca confirmado por proximidad. Puede estar vacío con encabezado. |
| `resumen_conteos.csv` | `metrica,valor` | Debe reconciliar ocurrencias, clases únicas, duplicados, exclusiones y revisiones. |
| `manifiesto_ejecucion.json` | `auditoria,estado,fuentes_ordenadas,hashes,version_pipeline,config_hash,crs,crs_validado,baseline,maestro_ref,conteos,advertencias,artefactos` | Distinguir `PRELIMINAR`, `CRS_PENDIENTE`, fallas y estado de aprobación humana. |

**Importante:** `topologia_confirmada.csv` es una **entrada de la auditoría**, no un resultado autoaprobado. Al final del Proceso 1 puede que existan coordenadas proyectadas aptas para puntos sin conectividad aprobada para rutas.

## Estados para trazabilidad

- `VALIDO`: admitido y prevalente.
- `DUPLICADO`: ocurrencia referida a prevalente; no otro objeto CAD.
- `FUERA_ALCANCE`: registro de infraestructura subterránea u otro tipo formalmente excluido.
- `REVISAR`: ambiguo/no corroborado; no dibujar automáticamente.
- `RECHAZADO`: inválido irrecuperable; no dibujar.
- `RECUPERADO_AUXILIAR`: marca de evento/transformación; puede coexistir con `VALIDO`, no sustituye el estado del registro.
- `PRELIMINAR`: estado del lote ante incidencias abiertas.

Evitar mezclar en un solo campo estados por ocurrencia y estados por lote.

## Configuración sugerida (ejemplo, NO datos reales)

```json
{
  "auditoria": "Mirador",
  "fuentes_en_orden": ["STD HACIA CNAL 12.xlsx", "Ruta canal 12 level antes 2014 Completo.xlsx"],
  "hojas_por_fuente": {},
  "maestro_informativo": null,
  "baseline_historica": null,
  "crs_candidato": "EPSG:32611",
  "crs_validado": false,
  "evidencia_crs": null,
  "geografia_permitida": null
}
```

Las rutas dentro del ejemplo se entenderían **relativas al `entrada/` de esa auditoría**, no al histórico ni a carpetas del escritorio. El operador debe ajustar nombres exactos; el ejemplo no autoriza seleccionar archivos por semejanza.

## Reconciliación obligatoria

- Una sola fila `01_elementos_normalizados.csv` por único exportable.
- Toda ocurrencia registrada exactamente una vez en linaje.
- Cada descartado por duplicado apunta a un ID prevalente real; ninguna clase diferente se fusiona por compartir coordenadas.
- El número de dibujables por clase suma el total de CSV mínimo.
- Solo comparar con maestro **después** de unificar y no usarlo como filtro de planos individuales.
- Si faltan baseline o CRS, reflejar `NO_DETERMINADO` o `CRS_PENDIENTE`, respectivamente; nunca simular certeza.
