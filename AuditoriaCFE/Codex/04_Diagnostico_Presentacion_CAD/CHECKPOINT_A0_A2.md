# Checkpoint recuperable A0–A2 — presentación CAD CFE/DATRA

Fecha: 2026-11-05, contexto horario America/Tijuana. **Alcance reducido por el
owner durante la ejecución. Trabajo detenido al completar este documento.**
No autoriza continuar A3–A6, publicar cambios ni aprobar diseño, CRS o campo.
Las rutas siguientes son relativas a la raíz del repositorio actual.

## 1. Resumen ejecutivo y alcance efectivo

Se completó el preflight, se recuperó una inspección nativa de dos copias ya
lanzada antes de la redirección y se analizaron sus resultados en memoria.
Desde la redirección no se modificó código, LISP, SCR, configuración ni tests;
solo se realizaron lecturas, cálculos diagnósticos ligeros y este documento.
No se ejecutaron suites/benchmarks, variantes, nuevas impresiones ni operaciones
Git de escritura. No se comenzó A3, A4, A5 o A6.

Los 493 INSERT de Mirador corresponden uno a uno a los IDs del CSV diagnóstico,
sin faltantes, extras, duplicados ni tipos distintos. El máximo residuo X/Y
observado es 9.313225746154785e-10 unidades Model; **no son 493 igualdades binarias**:
98 posiciones coinciden exactamente como float y 395 presentan diferencias
del orden de la precisión de representación/serialización. No se reparó ni
reproyectó ningún dato. Esto no acredita alineamiento geográfico con el mapa.

`DATRA_A1` tiene cámara y plot diferentes de `Layout1`. Las alturas medidas en
el viewport DATRA son 3 mm para IDs y 2.5 mm para coordenadas. Los grandes números
en Model no prueban símbolos desproporcionados en papel. Hay concentración de
puntos y 122441 intersecciones potenciales entre cajas de textos; no procede
atribuir todo el problema a coordenadas erróneas ni reducir tamaños sin aprobación.

Los 213 archivos preexistentes del inventario de custodia conservan SHA-256,
tamaño y mtime_ns. Incluyen 161 archivos de las otras tres auditorías. Las copias
nuevas de inspección sí fueron guardadas por el trabajo previamente lanzado;
no sustituyen el DWG operativo ni los productos del piloto.

## 2. A0 — Git, autoridad y procedencia

- Rama: `codex/etl-unificado-auditoria-js`.
- HEAD inicial y de cierre: `0267abf312d8cbc6da9b927211f7ae4ca96f7524`.
- Último commit: `test(ci): normaliza ruta temporal del fixture en Windows`.
- Diferencia frente al corte solicitado: ninguna. `HEAD...origin/...` devuelve
  `0 0` frente a la referencia remota local. No se hizo fetch ni push.
- `git diff --name-only`: vacío; no hay archivos rastreados modificados.
- PR #1 consultado durante preflight: abierto, sin merge, head 0267abf. No se
  actualizó su descripción, estado ni checks.

Lecturas realizadas: AGENTS completo; los siete Markdown del paquete
`CFE_CONTINUIDAD_PRESENTACION_CAD_0267abf_v1/`; ADR000 y ADR001; TO-BE v0.3;
P09 v1; los tres documentos de `Codex/03_PR1_Piloto_Mirador/`; code review
histórico `temp/CODE_REVIEW_PR1_PIPELINE_CFE_2026-11-05.md`; `cad.py`, runtime
y pruebas existentes del generador. SHA256SUMS del paquete de continuidad
verificado. No se alteraron normas ni se adoptaron decisiones visuales nuevas.

Discrepancias documentales resueltas conservadoramente:

- AGENTS conserva un aviso antiguo sobre README_ENTREGA_Y_PASOS.md eliminado;
  el archivo está restaurado y Git no muestra eliminación. No se tocó.
- El paquete de continuidad declara que no tenía acceso al ZIP privado del
  piloto; **en esta máquina sí existe** y se verificó. Su limitación describe
  la preparación de aquel documento, no una ausencia local actual.
- El code review de temp corresponde a 97731f5. H01–H10 ya tienen resolución
  en el corte 0267abf; no se reabrieron ni reimplementaron en esta intervención.

Estado previo conocido, **heredado y no reejecutado aquí**:

- `tests/_runtime/pr1_piloto/suite_final.txt`: 93 tests en 79.182 s, OK; cierre
  anterior reporta 93 aprobadas, cero fallidas/omitidas localmente.
- `tests/_runtime/pr1_piloto/ci_estado.json`: dos runs del SHA 0267abf, push y
  pull_request, cuatro jobs success cada uno. No es una consulta nueva de CI.
- El cierre anterior conserva nueve omisiones históricas por job público;
  las pruebas CAD/GUI no se deducen del estado verde de GitHub Actions.

AutoCAD Core Console 2026 existe localmente y fue usado por el trabajo ya
lanzado. El reporte nuevo mide `ACADVER=25.1`; logs identifican el motor W.122.
No se inició GUI en esta intervención ni se inspeccionó su disponibilidad actual.
Los fallos de acceso GUI del piloto son información heredada, no prueba actual.

## 3. Actividades ejecutadas antes de la redirección

1. Creación del acta preliminar `ACTA_DIAGNOSTICO.md`, del exportador nuevo
   `src/auditoriacfe/cad_diagnostics.lsp` y de dos helpers privados en `_runtime`.
2. Snapshot de 213 archivos y verificación del manifiesto operativo, fuentes
   declaradas, configuración, ZIP previo, dos SCR y dependencias.
3. Copias únicas bajo `salida/resultados_cad/presentacion_4aae673bfc/`:
   `antes.dwg` desde el DWG de trabajo del piloto y `base.dwg` desde la copia
   DATRA en entrada. **No se alteró ninguna de esas dos fuentes.**
4. Primer intento nativo fallido: carga del runtime cancelada por ruta de carga
   no incluida y función DATRA:GUARD ausente. El log quedó preservado. Un intento
   intermedio fue rechazado por el chequeo léxico de paréntesis antes de lanzar
   AutoCAD. Se corrigieron los auxiliares mientras el alcance original lo permitía.
5. Se lanzó de nuevo el trabajo de inspección de ambas copias. Al recibir la
   redirección se dejó terminar ese trabajo: retornó `antes EXTRAIDO` y
   `base EXTRAIDO`, exit 0, sin errores AutoLISP en los logs aceptados. No se
   iniciaron nuevos trabajos nativos desde la redirección.

El exportador cambia temporalmente CTAB/TILEMODE y activa viewports para medir
transformaciones WCS→Paper; el wrapper guarda **las copias nuevas** con QSAVE.
Por ello no debe describirse como apertura DWG sin escritura a nivel de copia.
No inserta componentes ni altera intencionalmente geometría de auditoría.
No se ejecutaron de nuevo SCR01/SCR02 en este trabajo: se inspeccionó su resultado
ya existente. Los dos SCR auxiliares de inspección no son productos operativos.

## 4. A1 — Estructura CAD observada

Fuente principal: `presentacion_4aae673bfc/antes.jsonl`, lectura **cp1252**.
No convertirlo ni reescribirlo para leerlo como UTF-8; sus hashes son de bytes.

| Espacio/layout | Observación | Estado / procedencia |
|---|---|---|
| Model | Contiene 493 INSERT propios, 986 TEXT propios; 414 POSTE,20 CAJA_EMP,59 EXCEDENTE | CONFIRMADA, extracción nativa nueva |
| Layout1 | Existe; papel 841×594 mm; plot numerator=1,denominator=0.0393700787401575; otro viewport y cámara; atributos de conteos `--` | CONFIRMADA, antes.jsonl:3 y atributos |
| DATRA_A1 | Existe; papel 841×594 mm; plot 1:1, DWG To PDF.pc3; viewport principal y conteos 414/20/59 | CONFIRMADA, antes.jsonl:4,114 y atributos |
| Layout utilizado por pipeline | `cad.layout=DATRA_A1`; se emite en configure/begin y se usa en finish | CONFIRMADA, configuración/manifiesto y código |
| PDF conocido del piloto | Title DATRA_A1; acta/log previos indican plot DATRA_A1, una A1 horizontal | CONFIRMADA como evidencia archivada, no impresión nueva |
| Cinco paneles y ubicación | Vacíos en la vista completa existente; encabezado heredado «DETALLES APROBADOS» no acredita contenido | CONFIRMADA en imagen previa inspeccionada; validación humana P07 pendiente |
| Simbología | Runtime EXCEDENTE usa círculo+cruz; leyenda base muestra triángulo | CONFIRMADA por código e imagen previa; armonización pendiente |

Ambiente inicial en la copia del piloto (`antes.jsonl:1`): CTAB DATRA_A1,
TILEMODE 0, INSUNITS 4, UCSNAME vacío, WORLDUCS 1, origen UCS cero y ejes X/Y
mundiales; PDFSHX 0. INSUNITS 4 es metadato de inserción, no acredita CRS ni
justifica aplicar un factor geográfico. La copia base comienza en Layout1
con los mismos INSUNITS/UCS (`base.jsonl:1`).

Se inventariaron seis entidades VIEWPORT en el resultado y cinco en la base.
No equivalen a seis ventanas imprimibles: hay una entidad global de Paper,
entidades inactivas y una VIEWPORT residual listada en Model. La ventana principal
DATRA es handle `B125A`; Layout1 conserva `AB4F4`, otra pequeña `ABD5F` y la
entidad global `A9AED`. No borrar estos objetos por inferencia en una reanudación.

El fondo heredado conserva 124 registros de muestreo en Model en ambas copias:
91 INSERT,17 TEXT,10 LINE,5 CIRCLE,1 LWPOLYLINE. Las secuencias de tipo/capa/puntos
exportadas coinciden. Esto es una comprobación de muestras, **no una auditoría
exhaustiva de geometría anidada de los 91 bloques**. El motor registró EXTMIN/
EXTMAX generales de Model en `base.jsonl:258` y `antes.jsonl:1749`.
Esos extents incluyen anotaciones y objetos heredados, no una delimitación
semántica aprobada de la cartografía de Tijuana. Su aislamiento exacto permanece
PENDIENTE. La intersección de rangos no valida superposición geodésica.

## 5. A2 — Algoritmo, mediciones y límites

### Cálculo existente, sin cambios

`cad.py:133–146` calcula el bbox con todos los registros del CSV usado por CAD:

```text
bbox = [min(X),min(Y),max(X),max(Y)]
s = max((xmax-xmin)/410, (ymax-ymin)/445, 0.01)
h = max(s*3.0, 0.05)
```

`cad_runtime.lsp:174–181` utiliza **h tanto para escala X/Y/Z del bloque como
para altura de ID y desplazamientos (+h,+h)/(+h,-h)**. La altura geográfica es
h×2.5/3. No hay separación de parámetros visuales implementada. Los bloques
POSTE/CAJA tienen anchura nominal 0.9; EXCEDENTE alcanza 1.3 por la cruz
(`cad_runtime.lsp:60–74`).

`cad_runtime.lsp:302–334` crea MVIEW entre (145,70) y (675,535): 530×465 unidades
Paper. Usa UCS World y PLAN World, calcula el mismo s, aplica ZOOM Center con:

```text
centro = ((xmin+xmax)/2 + 50*s, (ymin+ymax)/2)
altura de vista Model = 465*s
```

Después bloquea el viewport. El término +50*s mueve la **cámara**, no las
coordenadas de los postes. Coordenadas absolutas y centros exactos se conservan
en los anexos privados; aquí se documentan fórmulas y magnitudes agregadas.

### Valores observados del lote

| Magnitud | Resultado | Naturaleza |
|---|---:|---|
| Span bbox X/Y | 88452.91104571 / 54482.31672517 unidades Model | CONFIRMADA, CSV y posiciones nativas |
| s del compilador | 215.73880742855977 unidades Model/unidad Paper | CONFIRMADA por cálculo y viewport |
| Altura de cámara | 100318.5454542803 unidades Model | CONFIRMADA, antes.jsonl:114 |
| h / escala de INSERT | 647.2164222856792 | CONFIRMADA, todos los INSERT |
| Altura de coordenada en Model | 539.3470185713994 | CONFIRMADA, 493 TEXT |
| Factor Paper/Model DATRA | 0.004635234670661383 | CONFIRMADA, viewport y anchors nativos |
| Altura ID / coordenada en A1 DATRA | 3 / 2.5 mm | CONFIRMADA por medición y conversión 1:1 |
| Anchura POSTE/CAJA / EXCEDENTE en A1 | 2.7 / 3.9 mm | INFERIDA de definición de bloque y escala medida |
| Offset X y ±Y del texto en A1 | 3 mm | CONFIRMADA por posiciones y escala |
| Cámara DATRA | Dirección +Z, target cero, twist 0; ortográfica; bloqueo sí; no clip no rectangular | CONFIRMADA, flags y DXF |

La conversión se corroboró con anclas WCS→DCS→PSDCS calculadas por AutoCAD:
`antes.jsonl:1750–1751`, no solo por una fórmula Python. El exportador usa un
paso ficticio de 1000 unidades para medir la transformación; **no es control
físico CRS ni geometría insertada**.

### Diferencia decisiva entre layouts

El viewport AB4F4 de Layout1 tiene 21.6078373×21.0602865 unidades Paper y altura
Model 20793.5267033. Su relación Paper/Model es distinta; el plot multiplica
por **25.4** al usar denominator 0.0393700787401575. La ventana imprimiría
aproximadamente 548.839×534.931 mm. Sus flags no muestran el bloqueo de zoom.

**Predicción INFERIDA, sin nuevo PDF de Layout1:** los mismos textos h del lote
se imprimirían allí con ID≈16.6502 mm y coordenada≈13.8752 mm, y un símbolo
nominal≈14.9852 mm. Esa diferencia puede explicar una captura con símbolos
grandes aunque Model no se haya movido. No consta de qué layout procedían
las capturas de otros chats; esa atribución sigue PENDIENTE.

### Posiciones, extremos, colisiones y recortes

- Comparación por ID contra `02_DIAGNOSTICO_NO_VERIFICADO.csv`: 493/493;
  tipos correctos; sin duplicados. Residuo máximo X/Y=9.313225746154785e-10
  unidades Model, 98 igualdades float exactas. No se confunde proximidad numérica
  con igualdad Decimal de identidad ni con validación geográfica.
- Cuantiles marginales interpolados p1/p99: span X=19192.13007898 e
  Y=7670.09504211 unidades Model. Al factor DATRA esto ocupa aproximadamente
  88.96×35.55 mm frente al bbox total mucho mayor.
- 20 puntos están fuera del rectángulo marginal p1/p99; 14 se señalan con
  cercas 1.5×IQR por cualquiera de los ejes. **Son criterios exploratorios
  declarados, no reglas de rechazo/admisión ni aprobación de outliers.** Todos
  se conservan y no se exportó una nueva lista operativa.
- Se midieron 986 TEXT de Model con `textbox`, posición y rotación nativas.
  Todas las rotaciones de esos textos son cero en la muestra completa medida.
  Intersecciones AABB de área positiva, sin doble contar pares: coordenada–
  coordenada 42360, coordenada–ID 34223, ID–ID 45858; total **122441**.
  Participan 978 textos. Las cajas pueden contener espacios de glifos: se
  reportan **colisiones potenciales**, no intersecciones exactas de trazos.
- Cero cajas de esos 986 textos rebasan el rectángulo del viewport principal.
  Esto **no prueba** que todo el mapa, símbolos, marcos o glifos se impriman sin
  recortes ni que los textos sean legibles. No se hizo un PDF nuevo.
- La imagen completa archivada confirma conglomerado oscuro de textos sobre
  el fondo y amplio vacío en A1. La causa combinada de extremos, bbox global,
  textos obligatorios y cartografía densa es consistente con las mediciones;
  no hay autorización para eliminar etiquetas ni escoger otro encuadre.

## 6. Matriz de hallazgos y siguientes acciones

| ID | Hallazgo | Evidencia | Estado | Impacto | Siguiente acción |
|---|---|---|---|---|---|
| A0-01 | HEAD 0267abf y referencia origin local iguales | git log/status/rev-list 0 0 | CONFIRMADA | No hay avance de código que migrar | Mantener rama y revisar cambios no rastreados |
| A0-02 | 213 archivos previos preservados, incluidos 161 de otras auditorías | snapshot y cotejo SHA/bytes/mtime_ns | CONFIRMADA | Custodia conservada | Reutilizar baseline, no regenerar originales |
| A1-01 | Tres espacios/layouts con configuraciones diferentes | antes.jsonl:1–4 | CONFIRMADA | Capturas no comparables sin CTAB/plot | Registrar layout de cada futura captura |
| A1-02 | Viewport principal DATRA 530×465, ortográfico y bloqueado | antes.jsonl:114,1751 | CONFIRMADA | Cámara conocida | Reutilizar métricas; no mover geometría |
| A1-03 | Conteos 414/20/59 solo en DATRA; Layout1 muestra -- | ATTRIB nativos, runtime:194–217 | CONFIRMADA | Cajetines distintos según layout | Revisar DATRA_A1, no copiar valores por estética |
| A1-04 | Extents generales no aíslan el mapa de bloques/anotaciones | base.jsonl:258; 91 INSERT heredados | PENDIENTE | No se acredita CRS/alineación | Investigar bloques/capas con nuevo alcance |
| A2-01 | 493 IDs/tipos corresponden; residuo numérico máximo 9.31e-10 | CSV diagnóstico + owned INSERT | CONFIRMADA | No evidencia de desplazamiento visual de Model | Preservar ID/XY y medir controles reales P06 |
| A2-02 | Símbolo, ID, coordenada y offsets comparten h | cad.py:140–143, runtime:174–181 | CONFIRMADA | Escalas acopladas | Proponer separación solo en fase autorizada |
| A2-03 | DATRA presenta ID3mm/coord2.5mm; números Model grandes son esperables | altura nativa y escala viewport | CONFIRMADA | No justifica reducir tamaños automáticamente | Someter dimensiones a owner |
| A2-04 | Plot Layout1 podría imprimir ID16.65mm y símbolo≈14.99mm | cámara/plot nativos; cálculo sin impresión nueva | INFERIDA | Explicación posible de desproporción | Contrastar un PDF Layout1 si se autoriza |
| A2-05 | Extremos amplían bbox; 122441 pares AABB potencialmente superpuestos | cálculos read-only sobre 493/986 registros | CONFIRMADA | Legibilidad A1 bloqueada | Variantes y política de encuadre pendientes |
| A2-06 | 0 recortes AABB de TEXT no equivale a 0 defectos del plano | cajas de textos y PNG previo | CONFIRMADA | Evitar falsa aprobación por métrica parcial | Revisar glifos/mapa/símbolos en A3 autorizada |
| A2-07 | CRS/offset físico no se deduce de inspección visual | faltan controles reales; INSUNITS4 | PENDIENTE | P06 abierto | Dos controles físicos y tolerancia aprobados |
| A2-08 | Paneles vacíos y leyenda EXCEDENTE distinta del bloque v1 | vista previa existente + runtime:60–74 | CONFIRMADA | P07/P08 pendientes | Decisión del owner; no homologar automáticamente |

## 7. Evidencias persistentes y hashes

Lote operativo intacto: `AuditoriaCFE/auditorias/Mirador/salida/`.
Ejecución: `c8005ffde04d30bdcf5e0b3ff5d768a9b31f4f6aae91766b4e682ad855990951`.
DWG operativo que **no se sobrescribió**:
`salida/resultados_cad/piloto_PR1_Mirador_v1.dwg`.

Trabajo nuevo: `AuditoriaCFE/auditorias/Mirador/salida/resultados_cad/presentacion_4aae673bfc/`.
Contiene antes/base .dwg, .bak, .jsonl, .log y .scr auxiliares. No publicar estos
archivos: los JSONL contienen posiciones e identidades reales. No hay PDF nuevo.

| Archivo o referencia | SHA-256 |
|---|---|
| ZIP piloto EVIDENCIAS_CODE_REVIEW_MIRADOR_0267abf.zip | 04e6eb255ca997685c88fb58c587ab8ec48a4f186182300d37ef2b47b8ba5684 |
| salida/manifiesto_ejecucion.json | 5b03543f616c0c2e87c64c4166b993cf9c554e3bf0c91bd5ca664cd07c59df58 |
| salida/02_DIAGNOSTICO_NO_VERIFICADO.csv | df30cacc7280eea1cb9fb18c1691f6c1c5590b3dc5085f2a56082dde825b9498 |
| salida/01_configurar_plano.scr | ba463fa373db82b7ddb4c6a004dbe59a69d3ba352500f45178fa6eaffef9c693 |
| salida/02_dibujar_auditoria.scr | e5da7ce5921766c82dc3a7e2439ec3caea2ea92c9212ddf9607f3893614e0c1b |
| salida/cad_datos.lsp | b6c63df3b03806ce19205233c1e8b87995a2387d3396699a79460dde8a48bb0c |
| src y salida/cad_runtime.lsp | 9b78d7dcc4e442cf7f95b3d6933860f0ae8f63364433f75c50926a796d468693 |
| src/auditoriacfe/cad.py | 288825bc35ac72b8492d4348397599952c4c5b0190a39ff3cf20cc2f5ccc4e6a |
| nuevo antes.jsonl, 985896 bytes | 311bf4ade17f86e9a0a04c23062bcc72005472bb7ef9e756efd7c1338796d567 |
| nuevo base.jsonl, 33529 bytes | a9e80b61c5f56fbc19f66a52ed57b91b63d98ee8069e368855086fee39e251f5 |
| antes.log aceptado | 7197f81acb71e4ecfcf94d989ef653f7a2a8cd563ed8c38ae0938f511ae195b5 |
| base.log aceptado | 29fad3b6d50d68c4f52e24c5de6ec88e7a89097c01d8f487f07701cdae31efd3 |
| antes_intento_previo_0.log fallido | f86976a8fea46dd3f52b2e5244329f2e1e1f9d55945521375b6bc2294d8690ee |

Preflight privado: `AuditoriaCFE/tests/_runtime/presentacion/`:

- `custodia_antes.json`, 49300 bytes, SHA
  b1e47e3f29fbb8859fbdd00532cc57749950f9f2963048fb1eef6230b0430607.
- `estado.json`, SHA
  57e05c46eb2e95d1d337418e43279a27820497ca38f0b7d4ac5f12ebc8f2c96a.
- El cotejo final de los 213 archivos se hizo en memoria; no se creó un reporte
  nuevo después de la redirección. Distribución de otros lotes: Natura54,
  Otay-Florido55, Tijuana-General52, sin diferencias SHA/bytes/mtime_ns.

Evidencia visual antigua inspeccionada: `salida/evidencias_review/vistas/`
(`mirador_pagina_completa.png`, recortes y cajetín). PDF previo auténtico:
`salida/evidencias_review/planos/MIRADOR_DIAGNOSTICO_A1.pdf`, SHA
e10eec36c606c0c654d9b185d69bb210e79952ddd01402561fd1edacc135e421.
No confundirlo con impresiones nuevas de este checkpoint: no se produjeron.
El ZIP previo fue verificado con el verificador existente y no se descomprimió.
Ningún ZIP histórico completo se volvió a analizar.

CI archivado `tests/_runtime/pr1_piloto/ci_estado.json`, SHA
231d9a07c5e55aac5dfc630d2ab7e37b608855ca46a5e68e1452a55ee3921dae.
Suite archivada `tests/_runtime/pr1_piloto/suite_final.txt`, SHA
36c02c24bcac5ef2471fbcfcf9ef99fab08a315435d19b2f2f4da6b99cc8b1d0.

## 8. Archivos no publicados y límites técnicos

Preexistentes del owner, conservados sin staging:

- `AuditoriaCFE/Codex/02_Harness_Integral/.gitignore`.
- `AuditoriaCFE/Codex/02_Harness_Integral/05_PROMPT_MAESTRO_CODEX.txt`.
- `AuditoriaCFE/Codex/02_Harness_Integral/06_INVENTARIO_PAQUETE.json`.
- Directorio `CFE_CONTINUIDAD_PRESENTACION_CAD_0267abf_v1/`.

Agregados antes de la redirección, **sin revertir, sin commit y sin aprobación
como producto de producción**:

- `src/auditoriacfe/cad_diagnostics.lsp`, SHA
  07df33570eb202daceba1e69ed61b259d9e318cb843745b4e21c9465004fae7b.
- `Codex/04_Diagnostico_Presentacion_CAD/ACTA_DIAGNOSTICO.md`: acta preliminar
  anterior al cambio de alcance; este checkpoint es la referencia de cierre.
- `tests/_runtime/presentacion_preflight.py`, SHA
  f041c6fc1d7a160eb8be6b3bca67795af72301a50549da43ead45775b1a89c3f.
- `tests/_runtime/presentacion_native.py`, SHA
  4495ef0757c39e7232a0b56895b6a8f12962d05d244d2624c645618a83130f08.
- Copias, logs, SCR de diagnóstico y JSONL privados antes enumerados.

Único archivo creado después de la redirección: **este CHECKPOINT_A0_A2.md**.
No hay modificaciones rastreadas. No se alteraron `cad.py`, runtime operativo,
configuración, contratos, CSV/XLSX, linaje ni manifiestos del piloto.

Riesgos al reutilizar el inspector: exportación cp1252 en este entorno; control
de rutas de carga necesario; datos WCS privados; textbox requiere interpretación
de rotación/normal para generalizar a otras entidades; extents de bloques anidados
no cubiertos por las muestras; estados de viewport dependen del layout activo;
las transformaciones se midieron en copias y no validan CRS. No se añadieron
pruebas de regresión del inspector ni se certificó su uso genérico.

## 9. Trabajo A3–A6 pendiente y reanudación concreta

**A3–A6 NO ejecutadas y NO autorizadas por la redirección vigente.** No hay
variantes sin textos, nuevos PDF, refactor de parámetros, nueva suite/benchmark,
ZIP de esta intervención ni commit/push/actualización PR. Las alternativas de
dimensiones, márgenes, zonas densas y encuadre requieren autorización posterior.
P03/P05/P06/P07/P08/P04 continúan abiertos; no hay plano FINAL.

Cuando el owner autorice una nueva sesión:

1. Leer primero este checkpoint y la nueva instrucción; no ejecutar scripts
   existentes automáticamente. Verificar HEAD/status y hashes de los anexos.
2. Usar los JSONL existentes (cp1252) para continuar, sin repetir A0/A1 salvo
   cambio de fuentes. Comparar INSERT por ID, y separar tipos/estados de viewport.
3. Mantener `cad.py` y `cad_runtime.lsp` en su corte 0267abf hasta autorizar una
   corrección. No corregir coordenadas para compensar cámaras o INSUNITS.
4. Aislar cartografía y bloques anidados si se requiere su bbox semántico;
   identificar layout de capturas externas. No atribuirles Layout1 por su aspecto.
5. Solo si se autoriza A3: copias independientes y variantes diagnósticas,
   siempre conservando la versión completa, ID/XY y una A1. Solo después valorar
   parametrización independiente con defaults anteriores y regresiones.
6. Resolver datos físicos P03/P06 con evidencia del owner; propuesta de diseño,
   paneles, leyenda y legibilidad no se aprueban mediante métricas automáticas.
7. Revisar los archivos no rastreados antes de cualquier staging futuro: no
   publicar copias, JSONL, datos operativos ni paquete de continuidad del owner
   por el solo hecho de estar en el repositorio.

**Último punto seguro:** inspección nativa cerrada, evidencias persistentes en
presentacion_4aae673bfc, cálculos A2 documentados y originales verificados sin
cambios. La ejecución se detiene aquí; no continuar automáticamente.
