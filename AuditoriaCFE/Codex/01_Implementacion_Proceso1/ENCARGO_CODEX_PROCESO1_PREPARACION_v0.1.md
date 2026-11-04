# ENCARGO CODEX — Proceso 1 de preparación XLSX → CSV de auditoría

**Estado:** encargo de implementación preparado para ejecución por el owner. **No** autoriza Fase 1C (dos SCR) ni ejecución AutoCAD. Fecha: 2026-11-04.

## 0. Leer primero y validar rutas

Trabajar con la carpeta abierta `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria` y sus rutas **relativas al repositorio**.

Lecturas obligatorias, en orden:
1. `AGENTS.md` (raíz).
2. `AuditoriaCFE/Docs/ADRs/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md`.
3. `AuditoriaCFE/Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.2.md`.
4. `AuditoriaCFE/Codex/00_Diagnostico/01_Excel_Origen/01_inventario_xlsx.md`, `02_perfiles_hojas.md`, `03_familias_y_mapeo_columnas.csv`, `04_calidad_y_anomalias.md`, `05_contrato_XLSX_a_CSV_propuesto.md`, `06_regresion_con_csv_historicos.md`, `07_checkpoint_para_aprobacion.md`.
5. `AuditoriaCFE/Docs/Specs/Contrato_Salidas_Proceso1_PROPUESTA.md` y `AuditoriaCFE/Codex/01_Implementacion_Proceso1/CHECKLIST_REVISION_PROCESO1.md`.

Si algún archivo obligatorio falta, **detener la etapa afectada e informar**, no buscar nombres parecidos, no sobrescribir fuentes. El árbol histórico `Auditorias-20261104T035633Z-1-001` es exclusivamente de lectura.

## 1. Definición de terminado para este PR/lote

Implementar en Python CLI un **Proceso 1 de preparación** que reciba la carpeta de una auditoría (`Natura`, `Mirador`, `Otay-Florido`, `Tijuana-General` o nueva), reconozca **cuatro familias** XLSX, consolide y deduplique entidades aéreas, preserve todo el linaje y genere:

1. **`01_elementos_normalizados.csv`** — tres columnas exactas aprobadas.
2. **`02_elementos_proyectados.csv`** — solo tras CRS/controles aprobados; en caso contrario, NO generar archivo falsamente validado, declarar `CRS_PENDIENTE` en manifiesto/reporte.
3. **`summary.csv`** — detalle trazable de componentes y comparaciones informativas (contrato propuesto anexo).
4. **`linaje_y_calidad.jsonl`** — ocurrencia por fila fuente válida/revisable/duplicada/fuera alcance.
5. **`reporte_incidencias.csv`** — problema específico y evidencia fuente.
6. **`asociaciones_elemento_ruta.csv`** — un componente puede pertenecer a varias subrutas sin duplicar objeto físico.
7. **`topologia_propuesta.csv`** — aristas candidatas opcionales, SIEMPRE no confirmadas; si aún no hay base suficiente, archivo vacío con encabezado más razón explícita.
8. **`resumen_conteos.csv`** — totales conciliables, más POSTE/CAJA_EMP/EXCEDENTE únicos.
9. **`manifiesto_ejecucion.json`** — entrada/hashes, estado, versión, configuración, CRS y advertencias.

`topologia_confirmada.csv` es **entrada humana versionada**, jamás algo que el sistema apruebe por sí mismo.

No implementar, escribir ni probar `01_configurar_plano.scr`, `02_dibujar_auditoria.scr`, DWG, DWT ni PDF final. Terminar con checkpoint de revisión; no fusionar decisiones nuevas sin aprobación.

## 2. Estructura de proyecto y modo de ejecución

Crear únicamente dentro de `AuditoriaCFE/`, por ejemplo:

```text
AuditoriaCFE/
  preparar_auditoria.py
  src/auditoriacfe/{cli,config,source_ooxml,schemas,coordinates,normalization,dedup,quality,projection,reporting,topology}.py
  tests/{unit,integration,fixtures}/
  auditorias/<nombre>/
    entrada/                       # originales locales copiados por operador (ignorados por Git)
    configuracion.json              # versionable, rutas relativas y precedencia explícita
    topologia_confirmada.csv        # solo si el operador la valida
    salida/                        # ignorada por Git
```

El ejemplo de estructura no obliga a esos nombres de módulos. Priorizar simplicidad: CLI Python, sin DB, web ni nube.

CLI requerida: lista interactiva y `--auditoria <nombre>` para pruebas. Antes de procesar, imprimir el número y nombre de archivos detectados. `--dry-run` debe mostrar rutas, precedencia y validaciones pendientes sin escribir productos finales.

No mover o modificar datos del histórico. Si se desea una prueba real, pedir al owner que copie XLSX a `entrada/`, o leer el histórico en modo prueba **solo si el path es explícito, registrado y readonly**. No cargar 185 MB en memoria ni descomprimir `postes.zip`.

## 3. ETL 1A: esquema y validación

- Reconocer: F1 `Nombre/elemento/coordenandas completas` A/B/C; F2 `Ruta/Elemento de Red/Coordenadas` A/B/C con foto D; F3 `Numero/Ruta/Elemento/Coordenadas` A/B/C/D y foto E, incluidos encabezado de Canal 12 D1 vacío; F4 Natura ruta B/tipo C/coord D sin Numero A. Confirmar con perfiles y no hardcodear detección solo por nombre de archivo.
- Procesar hojas reales, filas ocultas, columnas auxiliares N/W; saltar únicamente filas sin registro operativo y documentar decisión. No contar dimensiones formateadas como registros. No interpretar imágenes ni cargar payload multimedia.
- Parsear decimal hemisférico N/S/E/W según gramática aprobada, variantes inequívocas de espacios/símbolos, sin inventar punto decimal y sin redondear. Salida geográfica en grados decimales N/W para las fuentes existentes; valores fuera de rango mundial son incidencia.
- Si coord completa falla y auxiliares N/W son inequívocos y consistentes, recuperarla con `RECUPERADO_AUXILIAR` y conservar los tres textos, procedencia y motivo.
- Tipos `POSTE`, `CAJA_EMP`, `EXCEDENTE` son dibujables. `Registro` es fuera de alcance por decisión A09. Desconocidos son `REVISAR`, sin dibujar. `POSTE` no implica material.
- Deduplicar **dentro del plano**: tipo+coordenadas decimales exactas, no por redondeo o distancia. Si dos cajas idénticas poseen identificadores confiables distintos, exigir regla explícita documentada. Conservar todas las ocurrencias y prevalencia según `fuentes_en_orden` de config; sin orden explícito, fallar **corrida productiva** con mensaje claro.
- Archivos antiguos/copias incluidos se comparan, pero los duplicados no se exportan dos veces. Si un poste participa en varias subrutas, registrar asociaciones.
- No excluir componentes presentes en `Postes_CFE.xlsx` de un plano de Natura/Mirador/Otay. Maestro solo como referencia en summary cuando se declara y está disponible. `nuevo/existente` solo frente a baseline de la auditoría indicada; cuando no se configura, `NO_DETERMINADO`.
- Continuar con registros válidos ante errores, estado de salida `PRELIMINAR`, registro específico de cada incidencia y conteos auditables. No hacer salvamento automático de geoposiciones remotas sin regla aprobada.
- Escribir CSV UTF-8 sin BOM con encabezados y escape estándar, mismo orden determinista para inputs iguales, sin datos de otros contextos.

## 4. Preparación espacial 1B, sin dibujar rutas

- Tratar `EPSG:32611` como candidato, NO como sistema aprobado por el código o por el nombre visible de AutoCAD. `configuracion.json` declara `crs_validado` y **evidencia del control**; por defecto false.
- Si `crs_validado=false` o falta evidencia: producir ETL/reportes, indicar `CRS_PENDIENTE` y **no** crear `02_elementos_proyectados.csv` con un rótulo de validado.
- Con CRS aprobado por owner y controles CAD documentados, transformar lon/lat a Este/Norte mediante `pyproj` con `always_xy=True`, sin usar fórmula JS anterior ni compensación manual +11.5m. Verificar cardinalidad/identidad entre CSV canónico y proyectado.
- Mantener `topologia_propuesta.csv` separada de `topologia_confirmada.csv`, jamás marcar enlaces por proximidad como aprobados. Si se implementa un algoritmo candidato, reportar distancia/razón y `PENDIENTE_CONFIRMACION`. No generar polilíneas.
- Si no hay aristas confirmadas, el proceso sigue siendo útil para insertar puntos en una etapa futura, pero no estará «listo para trazar rutas».

## 5. Plan de pruebas obligatorio

1. Fixtures sin medios grandes para las cuatro familias, incluida Natura desplazada, auxiliar N/W, tipo `Registro`, hoja vacía y fila oculta.
2. XLSX sintético con dimensión de hoja inflada (1,048,576) y pocas filas útiles; verificar extracción acotada en memoria.
3. Coordenada con doble espacio; N/W sin espacio inequívoco; `No detectado`; falta W; valor fuera de mundo; auxiliar W sin decimal; fuera de Tijuana pero mundialmente válido.
4. Duplicados exactos entre libros/filas, subrutas diferentes, mismo punto con tipos distintos, IDs verificados de dos equipos físicos; cercanos no se fusionan.
5. Precedencia reproducible frente a orden alterado de directorio; guardar hashes y conteos. Repetir corrida y comparar bytes de CSV/JSONL de datos, separando timestamps variables del manifiesto.
6. Contraste con CSV históricos **antes de aplicar nueva deduplicación/exclusiones**, según `06_regresion_con_csv_historicos.md`: Mirador 551 registros, Otay 969; diferencia de doble espacio, encabezado ausente de Mirador y anomalías preexistentes. No exigir igualdad literal al CSV de salida nuevo: reglas cambiaron.
7. Maestro solamente informativo; baseline ausente = `NO_DETERMINADO`; `Registro` excluido; no repetir símbolos por coincidencias históricas.
8. CRS no validado: bloqueo explícito del CSV proyectado; CRS validado en fixture: proyección `always_xy`, sin 11.5m de offset ni precisión truncada.
9. Reconciliación por ocurrencia, grupo de duplicado y conteos por clase. Archivo temporal e interrupción no dejan salida mal rotulada como completa.
10. No tocar histórico y no añadir fotos, ZIP, XLSX ni salidas a Git.

### Criterios verificables de calidad

- Fallar con código de salida no cero ante config inválida o familia no reconocida; documentar modo preliminar cuando solo hay incidencias por filas.
- Registrar `sha256`, relativa a `entrada/`, hoja y fila original por cada ocurrencia.
- Validar que `postes + cajas + excedentes` = únicos dibujables aceptados y que las razones explican las demás ocurrencias.
- No resolver la discrepancia 56 vs 58 de duplicados Mirador inventando equivalencias: registrar método de conteo.
- Aceptación no se basa en ejecutar AutoCAD ni en inspeccionar screenshots; termina al generar los datos verificables con pruebas.

## 6. Decisiones abiertas: mecanismo de resguardo (sin bloquear todo)

- **P-01 precedencia:** elegir configuración **obligatoria** como mecanismo técnico sin atribuir orden de negocio; owner fija lista para casos reales.
- **P-02 baseline:** opcional, si falta marcar `NO_DETERMINADO`.
- **P-03 perímetro geográfico:** parametrizar y tratar fuera de área como `REVISAR` cuando no se haya acordado perímetro final; no inventar valores de coordenadas.
- **P-04 liberación final:** no declarar `FINAL` automáticamente si hay incidencias abiertas; estado `PRELIMINAR`.
- **P-05 topología:** propuestas nunca confirmación automática.
- **P-06 CRS:** no generar proyectado validado sin controles.
- **P-09 esquema exacto summary/linaje:** usar documento de contrato **PROPUESTA**, implementar estructura mínima consistente y presentar cambios de esquema para revisión; no alterar ADR.
- **P-11 duplicados Mirador:** incluir informe comparativo de definición y resultados antes de convertir un conteo en aserción rígida.

## 7. Entrega y parada

Al terminar, informar:
- Árbol de archivos nuevos y modificados, justificación de dependencias.
- Muestras representativas (no sensibles) de cada salida, conteos de fixtures y corridas de prueba.
- Comandos de instalación/ejecución en PowerShell, tests ejecutados y resultados.
- Matriz contra `CHECKLIST_REVISION_PROCESO1.md`: aprobado/no aprobado/bloqueado con evidencia.
- Qué faltó para producir `02_elementos_proyectados.csv` validado, si falta CRS.
- Cualquier nueva regla de negocio que necesite decisión del owner.

**Detenerse en el checkpoint de revisión del Proceso 1. No iniciar compilación de SCR, dibujo AutoCAD, cambio de DWT, commit o merge sin autorización expresa.**
