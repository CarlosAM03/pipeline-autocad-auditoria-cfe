# TO-BE v0.3 — Implementación integral de Pipeline CFE/DATRA

**Estado:** base de implementación aprobada por decisiones Q01–Q75 (2026-11-05), **con gates de evidencia**.
**Autoridad:** ADR-000 conservado + ADR-001 como enmienda para aspectos expresos + contrato P-09 v1.
**Rama técnica:** `codex/etl-unificado-auditoria-js`, punto de partida `f306074`.

## 1. Objetivo, alcance y definición de terminado

Herramienta offline para transformar una **auditoría** seleccionada con XLSX heterogéneos en dos SCR ejecutables en AutoCAD 2026 inglés, encima de la plantilla DATRA reutilizable; produce reportes y deja DWG y PDF A1 horizontal a cargo de la operación y validación humana. Se trabaja con las auditorías Natura, Mirador, Otay–Florido, Tijuana-General. Bomberos solo después, independiente.

**Implementación terminada:** módulos/CLI/contratos y dos SCR funcionales probados offline, pruebas CI, generadores de recursos CAD y procedimiento de ensayo real documentados. **Validación CAD terminada:** DWT nacida de base DATRA con WCS/CRS acreditados, perfil de AutoCAD ensayado en copia y una A1 sin errores de recursos. **Entrega física FINAL:** solo cuando el owner valida coordenadas, aristas reales, captura AutoCAD y DWG/PDF obtenidos, sin incidencias bloqueantes.

## 2. Arquitectura y cuatro checkpoints

```text
entrada/ originales copiados XLSX (read-only) ─────────────────┐
  + opcionales KMZ/KML/GeoJSON, resoluciones y topologia ──────┤
configuracion.json (excepción versionable sin datos privados)  │
                                                                ▼
     CP-01: extracción OOXML → normalización de tipos/coords → identidad exacta
                       ├─ 00_elementos_unificados.csv
                       ├─ 00_elementos_revision.csv [nuevo auxiliar]
                       └─ linaje, incidencias, summary, conteos
                                                                ▼
     CP-02: admisión P-03 → 01_elementos_normalizados.csv
             └─ validación P-06 contra DWG → 02_elementos_proyectados.csv
                  + correspondencias KMZ, aristas propuestas y confirmadas
                                                                ▼
     Compilación de instrucciones CAD fuera de AutoCAD
             ├─ CP-03: 01_configurar_plano.scr
             └─ CP-04: 02_dibujar_auditoria.scr
                                                                ▼
     Abrir COPIA de Plantilla DATRA en AutoCAD convencional
          └─ ejecutar SCR01 → SCR02 → revisar → guardar DWG → PDF A1
```

Los checkpoints no equivalen a cuatro procesos. Mantener **Proceso 1 = preparación + compilación de SCR** y **Proceso 2 = construcción/revisión del plano con AutoCAD**.

### CP-01 — XLSX → inventario deduplicado

- Leer cuatro familias OOXML de fuentes declaradas y sus hojas reales, preservar fórmulas/cachés como evidencia sin recalcular ni procesar fotos.
- La desorganización de filas o libros **no establece dirección de la ruta**. Precedencia de libros estable solo para prevalencia y reproducibilidad; debe constar en manifiesto y puede revisarse explícitamente.
- Normalizar etiquetas semánticamente inequívocas a POSTE, CAJA_EMP o EXCEDENTE; Registro fuera de alcance.
- Identidad física por tipo+latitud+longitud Decimal exactas, salvo excepción con ID externo confiable de equipos co-localizados; conservar cada ocurrencia y ruta vinculada.
- CSV 00 de 12 campos ya ratificado, sin duplicados adicionales; los grupos identificables pueden conservar estado P03 pendiente sin ser aptos para 01. Bandeja auxiliar `00_elementos_revision.csv` contiene trabajos pendientes y descartes por evidencia, sin perder grupo/ocurrencia.
- Resolver anomalías únicamente mediante `resoluciones_manual.csv` entrada con SHA de fuente, fila, valor previo/nuevo, tipo, motivo, evidencia, responsable, fecha y acción. Rechazos históricos enumerados se excluyen de CAD; no borrar origen.
- `Postes_CFE.xlsx` solo maestro informativo para los planos individuales; como entrada única para General v1. Sin baseline histórica acreditada, novedad NO_DETERMINADO.

### CP-02 — Admisión geográfica y geodesia

- Admitir ámbito por auditoría como polígono/corredor GeoJSON/KML con evidencia y versión aprobadas; soportar rectángulo legacy para compatibilidad y diagnóstico, no como autoridad automática.
- Fuera de ámbito → REVISAR/EXCLUIDO del 01 hasta excepción individual corroborada. Mundo imposible o coordenada desconocida → rechazos documentados.
- CSV 01 **exactamente** `Ruta,Elemento de Red,Coordenadas`, una fila por entidad única admitida.
- CSV 02 solo con CRS de DWG acreditado mediante **al menos dos controles WCS↔WGS84 independientes**, tolerancia documentada y biblioteca geodésica estándar `pyproj`. `EPSG:32611` es candidato compatible con UTM84-11N nominal del histórico; Mirador permite contraste pero su algoritmo JS conocido tiene ~11.5 m de error en Norte.
- Para ensayo sin controles: una vía **opt-in de SOLO DIAGNÓSTICO sobre una COPIA** puede proyectar el candidato y crear SCR de puntos marcados no verificados. **No** emitir el CSV02 productivo validado ni proclamar FINAL.
- Formalizar `ruta_id` determinista y `ruta_nombre` sin romper lectores v1; marcar `schema_version` en manifiesto. Usar `elemento_id` del CP01 como llave estable, nunca concatenar índices de posición.

### Geometría y topología — preparación previa a CP-04

- Soportes físicos: POSTE por defecto; cajas/excedentes como elementos con relaciones, no aristas inventadas.
- Importar KMZ en copia con controles de tamaño/seguridad; inspeccionar estructura KML (Placemark, Point, LineString, MultiGeometry, ExtendedData) y resolver correspondencias de IDs a entidades del CP-01. Sin KMZ presente, continuar con otras fases y modo puntos.
- Generar `topologia_propuesta.csv` con origen/destino y evidencia (geometría KMZ, proximidad diagnóstica, distancia, razón/confianza); **sin establecer conectividad física por cercanía**. Inicios/extremos desconocidos son candidatos, no hechos.
- Leer `topologia_confirmada.csv` solo como **entrada aprobada** por owner con IDs existentes, ruta/tramo, clase de arista, evidencia, aprobación y fecha. No generarla como autoaprobación.
- Soportar ciclos/anillos, intersecciones, bifurcaciones, postes compartidos y componentes desconectados. Tres anillos globales declarados no son tres ciclos implementables hasta acreditarlos.
- Troncal = aristas declaradas; mayor número de postes solo alerta de consistencia B06. Cada arista confirmada se dibuja una sola vez, por segmentos/series sin saltos ni regresos DFS.
- Longitud impresa = distancia **plana** en CRS entre extremos realmente conectados, separada del metraje real de fibra.

### Preparación CAD y DWT canónica (una sola vez)

- Reutilizar `AuditoriaCFE/recursos/PlantillaMarcoDatraMapaTijuana.dwg` como base de trabajo y `MARCO_DATRA_A1_EMPRESA_v0_2.dxf` como origen de marco editable. `146468_PLANOTIJUANA.dwg` referencia CFE; Mirador es comparativo WCS y contenido de layout.
- Clonar en recursos de trabajo, nunca editar origen histórico. Validar entidades/capas, `INSUNITS`, WCS/UCS, vista, escala, XREF/rasters, fuentes, bloques, layouts, tabla, logo y cinco paneles.
- Convertir en DWT nativa **dentro de AutoCAD**, cuando se pueda ejecutar; `pyproj`, DXF o `.scr` no equivalen a generar DWT 2026 con garantías.
- Cartografía embebida primera versión; un solo layout A1 841×594 mm con viewport y mapa base no duplicado. Tope de detalle y nombres de calles reversibles.
- Detalles TENSION/SUSPENSION/DERIVACION/EMPALME/OTROS solamente cuando se acrediten como aplicables; diagramas propios genéricos se marcan PENDIENTE DE APROBACIÓN.
- El defecto final de marco no paraliza la codificación de CP-03/04; sí bloquea declarar canónica/final su DWT.

### CP-03 — `01_configurar_plano.scr`

- Precondición: AutoCAD 2026 inglés y COPIA de base DATRA abierta. Preferir comandos globales `_` y pruebas de prompts; LISP de apoyo empaquetado si se requiere.
- Definir/verificar unidad efectiva, capa, estilos, bloques, espacio/model/layout, orientación, paper A1 y existencia única del mapa. Configurar atributos globales seguros; registrar dependencias o verificaciones imposibles para SCR puro como precondiciones/controles manuales.
- No insertar postes, ruta ni mapa adicional; no cambiar CRS por etiqueta sin comparar WCS geográfica.

### CP-04 — `02_dibujar_auditoria.scr`

- Consumir únicamente lote íntegro (hashes/manifest), proyección admitida o modo ensayo claramente rotulado, y aristas confirmadas si existen.
- Un bloque por `elemento_id`, clase y capa; numeración estable P/C/E; etiqueta abreviatura+número+coordenada geográfica, sin redondeo para identidad. Coordenadas planas en Model Space.
- Aristas únicas sin saltos o backtracking; ciclos y componentes independientes; distancias planas con formato visual. Sin conectividad, SOLO PUNTOS PRELIMINAR.
- Resumen impreso exclusivamente por POSTE/CAJA_EMP/EXCEDENTE **realmente dibujados**, campos de cajetín editables sin nombres inventados.
- Las etiquetas obligatorias y una única A1 son reglas cerradas. Para General con miles de elementos, probar escalas, recuadros y tablas; si no es legible, incidencia BLOQUEANTE FINAL y propuesta de excepción ADR, sin ocultar datos ni crear otra lámina automáticamente.

## 3. Operación por auditoría y directorios

```text
AuditoriaCFE/
  src/auditoriacfe/                   # código versionado
  recursos/                           # candidatos CAD y DWT canónica verificada
  Docs/ADRs|Specs/                  # normas versionadas
  Codex/02_Harness_Integral/         # planes, logs/hallazgos de Codex
  auditorias/<nombre>/
    configuracion.json               # configuración estructural; nunca publicar datos privados sin revisar
    entrada/                         # ignorada: XLSX copiados, KMZ, resoluciones, topología confirmada
    salida/                          # ignorada: CSV, SCR, informes, manifiesto activo+historial, pruebas CAD
    temporales/                      # efímero de staging/bloqueo para publicación atómica, no resultado permanente
```

La nueva ubicación canónica de manifiestos activos/históricos está **DENTRO de salida**. Migración: verificar antiguo primero, importar historial cuando sea seguro, staged publication, esquema no auto-referencial (manifiesto lista hashes de artefactos salvo sí mismo), `--verificar-salida` tolera legacy mientras se migra y nunca mezcla dos ejecuciones.

La entrada original de histórico fuera de `AuditoriaCFE/` sigue inmutable. Copiar XLSX/KMZ explícitos a cada `entrada/`, registrar fuentes/hash, no procesar automáticamente todos los originales. Versionar solo scripts, contratos, código, fixtures ficticios, docs y recursos CAD con permiso de difusión verificado.

## 4. Interfaz de operación (a implementar)

- `--auditoria <nombre>` conserva modo individual.
- `--batch` procesa Natura, Mirador, Otay y General por separado con estado propio y resumen consolidado, sin mezclar entradas o manifiestos.
- `--dry-run`, `--verificar-salida` continúan; agregar verificación de topología/manifiestos y opción explícita de previsualización diagnóstica, nunca implícita.
- Config de perfiles SCR/AutoCAD versionada y CLI de verificación del paquete previo a abrir CAD.
- Los estados reportados por CP y por auditoría son independientes: `COMPLETADO_TECNICO`, `PENDIENTE_EVIDENCIA`, `PRELIMINAR`, `FALLIDO`, `ACEPTADO_HUMANO` (este último mediante acta, no al correr código).

## 5. Pruebas y cierre

Todos los módulos se cubren con fixtures sintéticos y regresión histórica en máquina autorizada; el pipeline debe mantener las 43 pruebas anteriores, añadir CI portable en GitHub, benchmark de CPU/RSS/tiempo sobre tamaños representativos, pruebas de seguridad de rutas/ZIP/XML, y pruebas de CAD cuando el GUI esté disponible. Ninguna prueba CI pública obtiene originales ignorados; su ausencia nunca se cuenta como regresión real aprobada.

Un proceso E2E no se declara FINAL cuando faltan WCS acreditado, topología obligatoria, legibilidad A1, recursos CAD o aprobación del owner. Ante bloqueo externo, generar evidencias, pruebas offline y tareas manuales mínimas para su posterior cierre; avanzar los módulos que no dependan de esa prueba.

## 6. Corrección de interpretación histórica JS

`ordenar.js` hace DFS con retorno explícito al padre dentro de una PLINE: **duplicaciones** de aristas. `trayectoria.js` registra cada vértice solo al entrar y conecta consecutivos de ramas distintas: **atajos sin arista**. Ninguno es fuente de verdad topológica. Reutilizar conceptos de grafo y comandos CAD, sustituir parsing, cálculo geodésico y dibujo por aristas confirmadas.
