# Pipeline local CFE / DATRA

Python >=3.10, extracción OOXML secuencial sin imágenes. CP-01/02 y compiladores CP-03/04 integrados bajo ADR-000 + ADR-001, TO-BE v0.3 y contrato P-09 v1. [ADR-002](Docs/ADRs/ADR-002_Presentacion_Multipagina_Y_Rutas_v1.md) enmienda rutas y presentación para A4.1. La aprobación de evidencia y el plano FINAL siguen siendo humanos. No se ejecuta AutoCAD al correr el ETL.

## Instalación y pruebas

```powershell
python -m venv AuditoriaCFE/.venv
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip install -r AuditoriaCFE/requirements.txt
& ./AuditoriaCFE/.venv/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
& ./AuditoriaCFE/.venv/Scripts/python.exe -m compileall -q AuditoriaCFE/src AuditoriaCFE/tests AuditoriaCFE/herramientas
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip check
```

En este equipo se conservó la `.venv` preexistente inaccesible y se usó `.venv-cp01` con Python 3.10.11. Sustituir ese nombre en los comandos si corresponde. Dependencias: pyproj/PROJ para geodesia y Shapely para polígonos/corredores. No requiere Excel, openpyxl, pandas ni decodificador de fotos. Node.js solo se necesita para las cinco pruebas de auditoría JS, sobre copias temporales sin MAIN. Las cuatro pruebas de extracción histórica y las cinco JS se omiten explícitamente en CI pública sin originales, no se declaran aprobadas.

La suite original de **43 pruebas** permanece intacta. Se ampliaron pruebas de resoluciones, polígonos, migración, versiones de 02, KMZ, grafos, CAD y operación. Resultados reales de cierre: [acta fase 6](Codex/02_Harness_Integral/acta_fase_6.md). El [oráculo congelado](tests/fixtures/README.md) de reporting 7baa82c mantiene hash y comparación de bytes sin necesitar Git ni historial profundo.

## Operación individual y batch

```powershell
# Si se tienen los históricos en sus rutas exactas autorizadas:
python AuditoriaCFE/preparar_auditoria.py --preparar-entradas --auditoria Natura
python AuditoriaCFE/preparar_auditoria.py --auditoria Natura --dry-run
python AuditoriaCFE/preparar_auditoria.py --auditoria Natura
python AuditoriaCFE/preparar_auditoria.py --batch
python AuditoriaCFE/preparar_auditoria.py --batch --verificar-paquete
# Ensayo voluntario CRS candidato, siempre COPIA + NO VERIFICADO:
python AuditoriaCFE/preparar_auditoria.py --batch --diagnostico
```

Sin `--auditoria` se selecciona por consola. `--dry-run` inventaría y muestra XLSX y precedencia sin abrir celdas ni escribir. `--entrada-prueba` conserva pruebas históricas readonly y estado PRUEBA; no se admite junto a batch. Códigos: 0 ejecución técnica (puede estar PRELIMINAR), 2 fallo, 130 interrupción. Batch continúa después de un fallo y devuelve 2 si cualquiera falla.

Las cuatro auditorías son Natura (un XLSX, 14 subrutas), Mirador (STD, Canal, copia), Otay-Florido (Vía Rápida, FLO final, Protección Civil y Bomberos, en ese orden) y Tijuana-General (solo Postes_CFE). `intake.py` contiene las rutas exactas, copia sin sobreescribir cambios y registra SHA. No busca directorios privados ni descomprime respaldos. Maestro derivado separado en CSV informativo; su fecha de copia no se presenta como fecha del levantamiento ni baseline histórica.

```text
auditorias/<auditoria>/
  configuracion.json              # estructural, real ignorada; no publicar coordenadas
  entrada/                       # copias XLSX, recursos, KMZ, aristas/resoluciones/evidencias
  salida/                        # CSV, SCR, reportes, checklist, acta, manifiesto
    manifiesto_ejecucion.json     # autoridad v2 activa
    manifiestos/<id>.json         # historial migrado sin pérdida
    resultados_cad/               # DWG/PDF/evidencia nativa mutable, preservada
    fallos/                       # incidencias de ejecuciones posteriores, preservadas
  temporales/                    # staging y recuperación efímeros
```

El resumen batch reside en `auditorias/_batch/salida/resumen_batch.json`. Cada lote tiene identidad y hashes propios. `--verificar-salida` y `--verificar-paquete` verifican artefactos, manifiesto, configuración y entradas para consumo. Para preparar un lote nuevo se permite que las entradas hayan cambiado, después de comprobar la integridad de los artefactos anteriores. La migración falla sin destruir la autoridad anterior; una interrupción recupera `salida_anterior`. Los resultados CAD mutables se conservan, y no se confunden sus posibles ediciones con artefactos del compilador reproducible. Deben inspeccionarse por separado para aceptar el plano.

## Configuración

Conservar `configuracion.ejemplo.json` como perfil legacy; para arnés integral declarar `schema_02: 2`. `fuentes_en_orden` es obligatoria, cubre TODOS los XLSX de entrada y fija prevalencia. `hojas_por_fuente` declara todas las hojas de libros múltiples, incluidas vacías, en orden. No se usa mtime ni orden de coordenadas como conectividad. Excepción de Canal: `excepciones_cabecera: {"archivo.xlsx":{"Hoja1":"F3_D_VACIA"}}`; no autoriza adivinar columnas de otros libros.

- `geografia_permitida:null`: grupos identificables en 00, 01 sin no admitidos. Rectángulo legacy: lat_min/max, lon_min/max, aprobada y evidencia. No se autoaprueba una ventana exploratoria.
- Polígono/corredor: `geografia_permitida:{archivo:"ambito.geojson",aprobada:true,crs:"EPSG:4326",version:"v1",evidencia:"...",responsable:"...",fecha:"YYYY-MM-DD"}`. Archivo en entrada, GeoJSON/KML; corredor lineal requiere `corredor_m`. Validación de anillos/huecos/rangos/antimeridiano, sin reparar geometría inválida.
- `ids_confiables`: archivo/hoja/fila/id/evidencia, o resolución individual acreditada. No asumir que Numero Excel es un ID. Cajas acreditadas con IDs distintos pueden coexistir; ambigüedad queda en revisión.
- `resoluciones_manual.csv` en entrada, contrato P-09: fila + archivo relativo + SHA + valor original exacto + acción + evidencia + responsable + fecha + aprobada. Acciones EXCLUIR/CORREGIR_COORDENADA/CORREGIR_TIPO/EXCEPCION_AMBITO/ID_EQUIPO_ACREDITADO. Conflictos bloquean; no se edita XLSX ni desaparece linaje.
- `maestro_informativo` y `baseline_historica`: archivo/fecha, la segunda exige auditoria igual. Comparación informativa, no filtro; baseline ausente o incompleta no acredita novedades por ausencia.
- `crs_validado:false`, `crs_candidato:"EPSG:32611"`. Para 02 productivo, `evidencia_crs` requiere archivo, aprobado_por, fecha, crs concordante, unidades m, tolerancia_m y al menos dos controles distintos {id,latitud,longitud,este_m,norte_m}. `pyproj` verifica residuales; no aplica offsets. No aprobar datos reales con controles sintéticos.
- `kmz:{archivo:"rutas_candidatas.kmz",tolerancia_m:0}`: umbral solo diagnóstico; carga segura sin extraer ni acceder a NetworkLinks. `mapa_ids` apunta a CSV aprobado de ID externo→elemento. Correspondencias y aristas propuestas permanecen NO_CONFIRMADAS.
- `cad:{base_dwg:"base_trabajo.dwg",copia:true,layout:"DATRA_A1",unidades_verificadas:false}`. Requiere copia explícita en entrada. El compilador prepara otra copia mutable con nombre derivado del hash, y nunca sobreescribe una edición existente. Sin metros acreditados no se habilita dibujo productivo.
- `diagnostico:false`: solo `--diagnostico` o configuración explícita habilita ensayo candidato. No cambia decisiones P-03/P-06.

## Contratos y geometría

| Archivo | Semántica |
|---|---|
| 00_elementos_unificados.csv | 12 columnas ratificadas, una fila por identidad exacta; no equivale a aptitud CAD. |
| 00_elementos_revision.csv | Bandeja por incidencia/ocurrencia, separada del inventario físico. |
| 01_elementos_normalizados.csv | Exactamente `Ruta,Elemento de Red,Coordenadas`, UTF-8 sin BOM, CSV escapado/CRLF; solo admitidos. |
| 02_elementos_proyectados.csv | v2: elemento_id,ruta_id,ruta_nombre,tipo,latitud,longitud,este_m,norte_m,crs. Solo P-06 acreditado. |
| 02_DIAGNOSTICO_NO_VERIFICADO.csv | Archivo diferente, candidato sobre copia, jamás sustituye al 02 validado. |
| summary/linaje/incidencias/asociaciones/conteos | Prevalentes y cada ocurrencia, descartes, referencias y rutas compartidas reconciliadas. |
| topologia_propuesta.csv | v2, geometría fuente y score; no habilita líneas. |
| reporte_topologia.json | Componentes, ciclos, extremos candidatos, B06 informativo; no inventa inicio/final. |

El 02 v1 sigue leyéndose: su ruta_id era el nombre literal, se interpreta bajo versión 1; v2 tiene ID estable separado del nombre. El esquema se declara en manifiesto. Los 00/01 no cambian de encabezado ni cardinalidad por incorporar CAD.

La única autoridad de líneas es `entrada/topologia_confirmada.csv` con contrato de P-09: arista_id,origen_id,destino_id,ruta_id,tramo_id,clase,evidencia,responsable,fecha_aprobacion,estado. Solo CONFIRMADA, extremos POSTE admitidos, sin autobucles ni desconocidos; conserva subrutas pero dibuja cada par físico una sola vez. Cajas/excedentes no son conectores por defecto. Segmentos independientes representan ciclos/ramas sin saltos falsos DFS ni retornos duplicados. Distancia plana no equivale al metraje real de cable.

## Presentación A1 para las rutas prioritarias

En el perfil CAD, `"presentacion":{}` habilita ADR-002. Los perfiles sin esa clave conservan el comportamiento anterior. Se puede configurar `escala_detalle` (unidades de Model por mm de papel), `poste_mm`, `caja_mm`, `excedente_mm`, `coordenada_mm`, `identificador_mm` (cero oculta el ID gráfico), `separacion_mm`, `margen_mm` y `lider_max_mm`.

El compilador intenta una hoja. Cuando la extensión o la colocación de etiquetas exige dividir el inventario, crea una vista general y hojas de detalle. `presentacion_paginas.json` contiene las cámaras y el orden para publicar. `indice_presentacion.csv` conserva ID completo, tipo, coordenada y página primaria. Para repetir un plan distinto de hojas, generar una nueva copia del DWG. Publicar los layouts declarados, en ese orden, como un solo PDF A1 horizontal. Consultar las [instrucciones A4.1](Codex/04_Diagnostico_Presentacion_CAD/A4_1_Presentacion_Rutas/INSTRUCCIONES_OPERADOR.md).

## Operación AutoCAD

1. Verificar paquete y abrir **solo** la copia indicada en `reporte_validacion_cad.json`.
2. Ejecutar `SCRIPT` → `01_configurar_plano.scr`; después `SCRIPT` → `02_dibujar_auditoria.scr`. El LISP se carga automáticamente. Si AutoCAD pide confianza, comprobar hash y aprobar esa ruta concreta; no desactivar SECURELOAD global.
3. Revisar `resultados_cad/reporte_nativo.txt`, conteos reales, mapa, WCS/UCS, bloques, estilos y dependencias. SCR02 es idempotente para entidades de esta auditoría; no borra cartografía ni entidades ajenas. Los bloques son esquemáticos, no homologan instalaciones.
4. Imprimir solamente DATRA_A1 horizontal, una lámina, revisar IDs y WGS84 de todos los elementos y conteos dibujados. Si General no permite lectura, bloquear FINAL y proponer excepción al owner.
5. Guardar DWG/PDF como PRELIMINAR hasta aceptación humana. La DWT canónica `Plantilla_Auditoria_CFE_Tijuana.dwt` solo se acredita tras SAVEAS nativo, reapertura y validación de WCS/papel/recursos. No se produce por renombrado.

`DATRACONTROLES` captura dos selecciones WCS, pero el owner debe identificar sus WGS84, evidencia y tolerancia antes de declarar CRS. El [checklist nativo](Codex/02_Harness_Integral/CHECKLIST_CAD_NATIVO.md) detalla los pendientes. Una prueba Core Console no certifica la presentación visual en GUI.

## Rendimiento, CI y custodia

`python AuditoriaCFE/herramientas/benchmark.py --filas-xml 1000000 --elementos 10000` mide tiempo/CPU/RSS/IO del proceso con datos ficticios. No fija un SLA sin medición acordada. GitHub Actions usa clones superficiales y fixtures públicos en Windows/Linux Python 3.10/3.12, compilación, lint, hash de oráculo, custodia y suite; omisiones históricas son explícitas.

`python AuditoriaCFE/herramientas/verificar_publicacion.py --staged` bloquea nuevos paths privados/binarios/salidas. Nunca usar `git add .`; revisar staging. Los tres perfiles demo antiguos y PDF de referencia heredado se conservan, no autorizan publicar nuevos datos. Los recursos reales DWG/DWT/KMZ son locales con hashes; pedir acceso al responsable. No se fuerza la transcripción privada al índice.

Cierre nativo y CI: [CIERRE_INTEGRAL_2026-11-05.md](Codex/02_Harness_Integral/CIERRE_INTEGRAL_2026-11-05.md). Los dos SCR cargan automáticamente `cad_runtime.lsp` y `cad_datos.lsp`; este último evita líneas SCRIPT gigantes en General. SCR01 configura **PDFSHX=0** en el perfil AutoCAD para conservar los glifos visibles sin generar decenas de miles de comentarios SHX. Es una preferencia de exportación persistente, documentada; no desactiva texto ni controles de seguridad.
# Revisión PR #1 y trazabilidad adicional

El [piloto focalizado](Codex/03_PR1_Piloto_Mirador/ACTA_TRABAJO.md) extiende
la validación del cierre previo sin alterar sus actas históricas. Añade dos
[libros de trazabilidad](Docs/Specs/Contrato_Adicional_Trazabilidad_XLSX_v1.md)
por perfil integral; todos los CSV conservan su contrato.

Para preparar solo una auditoría: `--preparar-entradas --auditoria Mirador`.
La preparación de las cuatro requiere `--preparar-entradas --batch`. El piloto
de revisión ejecuta únicamente Mirador y un fixture ficticio aislado.

En `configuracion.json`, `pipeline_integral: true` habilita trazabilidad,
topología, manifiesto v2 y compilación CAD, con independencia de `schema_02`.
Omitir el flag mantiene la inferencia de perfiles antiguos; declararlo elimina
esa ambigüedad. `cad.copia_nombre` permite una nueva copia de ensayo sin
sobrescribir la copia de trabajo previa del operador.

`--verificar-paquete` verifica entradas/configuración/artefactos inmutables.
`--verificar-evidencia-cad` verifica el acta nativa y hashes mutables por separado.
La firma humana y los datos físicos deben inspeccionarse; un hash no los aprueba.
`salida/evidencias_review/` y los ZIP privados de revisión son contenedores
externos al lote reproducible: tienen su propio manifiesto y SHA256SUMS. No
quedan aprobados ni verificados por `--verificar-paquete`.

Recuperación: ejecutar una corrida bajo el lock habitual. Si solo existe
`temporales/salida_anterior`, se restaura tras verificar su manifiesto canónico.
Si existen ambas carpetas y la activa es inválida, solo se restaura la anterior
si es íntegra; la activa se conserva en `temporales/salida_cuarentena_<uuid>`.
Si ninguna es íntegra, se bloquea sin eliminar ninguna. Revisar y recuperar
manualmente trabajo mutable de la cuarentena antes de eliminarla.

Ensayo nativo opt-in, únicamente en la copia declarada: `python
AuditoriaCFE/herramientas/ensayo_nativo.py --auditoria Mirador --pdf
MIRADOR_DIAGNOSTICO_A1.pdf`. El driver verifica doble SCR02, reapertura, XDATA,
conteos y atributos reales del cajetín; no habilita proyección sin controles.
`--rollback` es una prueba destructiva controlada de geometría **propia** en
copias de ensayo, recomendada solo para fixtures; nunca ejecutarla sobre el
archivo editado del operador. No prueba cortes físicos ni aceptación GUI.
