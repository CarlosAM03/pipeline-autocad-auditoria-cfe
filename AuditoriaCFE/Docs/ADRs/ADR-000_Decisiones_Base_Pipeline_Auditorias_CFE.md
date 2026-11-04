# ADR-000 — Decisiones base del pipeline de auditorías CFE para DATRA

| Campo | Valor |
|---|---|
| Identificador | ADR-000 |
| Estado | **Aceptado como línea base**, con decisiones operativas pendientes identificadas expresamente |
| Fecha | 2026-11-04 |
| Ámbito | Reconstrucción y automatización de auditorías de infraestructura de fibra óptica en AutoCAD convencional |
| Autoridad de negocio | Responsable del proyecto (usuario); respuestas A01–A14, B01–B07, C01–C10 y D01–D02 del 2026-11-04 |
| Antecedentes | Reconstrucción AS-IS 2026-11-03; especificación TO-BE v0.1; diagnóstico Codex Fase 1A (7 entregables) y revisión técnica |
| Naturaleza | Registro de decisiones; **no es un permiso para programar ni una especificación detallada de pruebas** |
| Ruta sugerida en el repositorio | `AuditoriaCFE/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md` |

## 1. Contexto, objetivo y límites

DATRA necesita elaborar auditorías de infraestructura para CFE a partir de libros Excel XLSX originales de levantamiento, que pueden contener fotografías, fórmulas, columnas auxiliares, subrutas, versiones repetidas y formatos heterogéneos. Los CSV históricos `STD-MIRADOR.csv` y `STD-OTAY-FLORIDO.csv` son **salidas ya normalizadas**, no los originales. Los tres planos de auditoría anteriores son evidencia de regresión, no una plantilla aprobada que deba clonarse sin cambios.

**Objetivo:** un proceso reproducible que consolide y valide todos los XLSX de la auditoría seleccionada, genere un CSV de elementos únicos y trazables, prepare las conexiones confirmadas, cree exactamente dos scripts de AutoCAD y produzca un plano basado en una **plantilla editable propia de DATRA**, derivada de la referencia CFE y reutilizando el mapa vectorial de Tijuana.

**Ámbito de operación:** herramienta local sencilla, sin infraestructura cloud, backend, base de datos ni interfaz gráfica propia. La CLI en Python es la opción base; la elección definitiva de librerías y la reutilización de código histórico serán objeto de evaluación técnica posterior. El análisis de scripts JavaScript recuperados es una actividad **separada de este ADR** y sus hallazgos no se incorporan como decisiones aprobadas sin revisión.

## 2. Decisiones arquitectónicas de línea base ya acordadas

| Código | Decisión vigente | Consecuencia / límite |
|---|---|---|
| ARQ-01 | **Dos procesos secuenciales:** preparación fuera de AutoCAD y construcción del plano en AutoCAD. | No mezclar limpieza de Excel con ejecución CAD. |
| ARQ-02 | En preparación: **1A ETL XLSX→CSV y calidad**, **1B topología**, **1C compilación de instrucciones CAD**. | Los nombres `1A/1B/1C` designan etapas funcionales; la Fase 1A de diagnóstico ya ejecutada es un hito distinto. |
| ARQ-03 | **Dos scripts operativos en AutoCAD**, `01_configurar_plano.scr` y `02_dibujar_auditoria.scr`, en ese orden. | Los recursos DWT/DWG son estáticos, no ejecuciones extra. |
| ARQ-04 | **Abrir una plantilla DWT reutilizable** que ya incluya la cartografía de Tijuana y el marco DATRA/CFE. | El Script 01 configurará/verificará el dibujo y no duplicará el mapa ya presente. |
| ARQ-05 | AutoCAD **convencional**, con scripts `.scr` ejecutados mediante `SCRIPT`; evitar dependencia de `MAPIMPORT` de Map 3D. | Verificar comandos, idioma y versión exacta sobre el AutoCAD instalado antes de aceptación. |
| ARQ-06 | Geometría en **Model Space a coordenadas reales** y presentación A1 en **Paper Space**. | No trasladar ni deformar puntos para encajarlos; ajustar viewport/escala. |
| ARQ-07 | **Mapa vectorial DWG de Tijuana** reutilizado de los entregables históricos como base preferida; referencia PDF CFE para la composición. | Seleccionar donador CAD, confirmar sistema de referencia, unidades, capas y permisos; PDF no es DWT editable. |
| ARQ-08 | WGS84/UTM zona 11N (`EPSG:32611`) es **hipótesis de CRS**, no calibración ya aprobada. | Verificar contra mapa y controles antes de insertar geometría; no copiar desplazamientos históricos. |
| ARQ-09 | XLSX de entrada **inmutables**, procesamiento de memoria acotada, lectura de hojas reales y sin cargar fotografías para el ETL. | Conservar hash/archivo/hoja/fila; no confiar en rango Excel sobredimensionado. |
| ARQ-10 | Contrato mínimo de salida: CSV con `Ruta,Elemento de Red,Coordenadas` y **linaje/calidad separados**. | No introducir imágenes ni columnas de control en el CSV mínimo. |
| ARQ-11 | Identidad física y conectividad **separadas**: elementos no son aristas. | El orden de filas o la cercanía geográfica no acreditan conexiones reales. |
| ARQ-12 | Una CLI listará carpetas de auditoría y permitirá seleccionar una; procesará recursivamente los XLSX que le correspondan. | Mostrar archivos incluidos y generar salidas dentro de esa auditoría. No crear servicio adicional. |
| ARQ-13 | El formato final se acercará al modelo visual CFE, pero con **cajetín DATRA editable** y datos reales acreditados. | No copiar responsables, valores, cantidades o zonas de la plantilla de otra ciudad. |
| ARQ-14 | **Prioridad de entregas:** Natura, Mirador y Otay–Florido; Tijuana-General como cuarta entrega complementaria. | Todas compartirán plantilla y motor de generación. |
| ARQ-15 | La entrega se revisará antes de considerarse final; generar DWG y después PDF. | La automatización no equivale a aceptación técnica sin control de calidad. |

## 3. Reglas de alcance, extracción, limpieza y consolidación (A01–A14)

| ID | Decisión aceptada | Efecto vinculante |
|---|---|---|
| **A01** | Auditorías principales **Natura, Mirador y Otay–Florido**; **Tijuana-General** adicional. | Un contexto de auditoría por carpeta seleccionable. |
| **A02** | Mostrar **toda la ruta actualizada**, no solo el delta. Identificar elementos nuevos frente a históricos en un **CSV de resumen interno**. | La marca de novedad es informativa y no excluye de la lámina los elementos existentes. |
| **A03** | `Postes_CFE.xlsx` es la **fuente maestra de referencia** para el plano general; las auditorías individuales usan los XLSX de sus carpetas. | Comparar la tabla unificada de cada auditoría con el maestro **después** de deduplicar, solo para su `summary`; no incorporar registros del maestro automáticamente al plano individual. |
| **A04** | Regla inicial de coincidencia: **mismo tipo normalizado + mismas coordenadas normalizadas**, sin importar archivo ni subruta **dentro de una auditoría**. | Reportar coordenadas cercanas sin fusionarlas; igualdad no debe depender de redondeo arbitrario. |
| **A05** | Para determinar original dentro de una auditoría, prevalece **la primera fuente analizada según un orden explícito y reproducible**. El maestro no sustituye esa prioridad interna. | Consolidar fuentes locales primero; después consultar el maestro solo informativamente. Nunca usar fecha de modificación como autoridad automática. |
| **A06** | Dos cajas de empalme con coordenadas idénticas se consideran una por defecto, **salvo identificadores confiables** que prueben dos equipos diferentes. | Mantener excepción documentada y verificable; no descartar equipos distintos con ID acreditado. |
| **A07** | Ante coordenadas inválidas irresolubles, **continuar con los registros válidos** y generar **plano preliminar**; consignar incidencia específica en el summary. | No ocultar errores ni presentar el preliminar como inventario completo. Política formal de liberación final aún por precisar. |
| **A08** | Usar columnas auxiliares N/W si la coordenada completa presenta error **solo cuando el reemplazo sea inequívoco y consistente**. | Registrar valor original, valor elegido, motivo, fuente y fila en el summary/linaje. No inventar dígitos ni separadores. |
| **A09** | `Registro` describe infraestructura de **ruta subterránea** y **no es auditable para esta entrega CFE**. | Excluir de dibujo y conteo CFE; registrar exclusión por fuera de alcance (no como error de coordenadas). |
| **A10** | **Natura es una única auditoría lógica** aunque sus Excel incluyan múltiples nombres internos de ruta. | Preservar subrutas y origen en el summary, sin multiplicar láminas por cada nombre. |
| **A11** | Si hay versiones anteriores/copias en `entrada/`, se procesan y deduplican; la precedencia se reporta. | La copia no autoriza duplicar objetos CAD; todas las ocurrencias quedan trazadas. |
| **A12** | Tipos canónicos internos: `POSTE`, `EXCEDENTE`, `CAJA_EMP`. Exportación configurable a códigos históricos solo para compatibilidad/regresión. | La salida estándar nueva utilizará tipos canónicos; no perpetuar `cajadedmpalme` en el contrato principal. |
| **A13** | Normalizar variaciones sintácticas inequívocas N/W y espacios, **sin redondear ni reparar separadores inventados**. Coordenadas fuera de ámbito Tijuana requieren corroboración. | Conservar coordenada literal y registrar transformación. Validar tanto rango mundial como ámbito local. |
| **A14** | Leer filas ocultas con registros operativos; ignorar fotografías y celdas exclusivamente auxiliares para la geometría. | Mantener referencia de procedencia; no confundir filas formateadas con activos reales. |

**Interpretación imprescindible de A04–A06:** “descartar duplicados” significa **no incluir ocurrencias repetidas en el CSV dibujable ni generar símbolos repetidos**, conservando **todas** las ocurrencias, su estado, grupo de equivalencia, razón de descarte y el registro prevalente en un archivo de trazabilidad. Para dos clases diferentes en la misma coordenada (por ejemplo, un poste y una caja), **no** fusionar automáticamente. Para un mismo poste compartido entre subrutas, un objeto físico puede tener varias asociaciones lógicas de ruta.

**Comparaciones separadas:**
1. **Unificación local:** versiones y archivos de `entrada/` → componentes únicos de esta auditoría.
2. **Comparación con maestro:** componentes locales frente a `Postes_CFE.xlsx` → solo resumen informativo, **sin excluir del dibujo individual**.
3. **Delta histórico de auditoría:** nuevo/existente respecto a una línea base anterior del mismo plano → resumen informativo. La fuente y fecha exactas de esa línea base deben fijarse en la configuración; **no equiparar “ausente en maestro” con “nuevo desde la auditoría anterior”**.

### Contrato mínimo de salida acordado

```csv
Ruta,Elemento de Red,Coordenadas
```

- El CSV de dibujo tendrá **una fila por componente admitido y único de la auditoría**, con los tres campos y tipos canónicos indicados. Conservar precisión geográfica de origen siempre que sea interpretable; no redondear para deduplicación.
- La tabla canónica de trabajo y el linaje lateral conservarán `auditoria`, `ruta/subruta`, `archivo`, `hoja`, `fila`, coordenada literal y normalizada, tipo literal y canónico, estado, exclusión, duplicado y registro prevalente.
- La **tabla resumen del plano** contará los elementos **únicos efectivamente dibujados**, por `POSTE`, `CAJA_EMP` y `EXCEDENTE`. Excepciones, diferencias con maestro, otras categorías e incidencias se conservarán **solo en el summary interno**.
- Se requiere un `summary.csv` por auditoría que permita rastrear conteos y comparaciones; su **esquema definitivo** se aprobará con las pruebas del ETL. También habrá evidencia detallada por registro; un summary agregado no basta para auditar la deduplicación.
- Reglas técnicas propuestas por el contrato de Fase 1A que no cambian la semántica aprobada: CSV UTF-8, encabezado obligatorio, escape CSV estándar, orden de fuentes determinista, lectura OOXML secuencial y estados distinguibles entre válido, revisar, inválido, duplicado y fuera de alcance.

## 4. Red y trayectorias (B01–B07)

| ID | Decisión aceptada | Efecto vinculante |
|---|---|---|
| **B01** | Las coordenadas de los Excel pueden estar **desordenadas**. | No usar orden de filas como ruta física. |
| **B02** | No hay inicios/finales formalmente identificados en los recursos actuales. Los extremos de los CSV son solo **candidatos tentativos**. | La topología no queda confirmada por el CSV; exigir validación del recorrido antes de la trayectoria final. |
| **B03** | El sistema puede **proponer conexiones** por análisis espacial; se validan antes de dibujar. | Las aristas propuestas no son automáticamente aristas aprobadas. |
| **B04** | Una auditoría puede tener **tramos desconectados**. | Dibujarlos como componentes independientes, sin puentes ficticios. |
| **B05** | Si dos rutas comparten un poste, habrá **un único elemento físico** con varias relaciones/conexiones. | Deduplicar geometría, no la conectividad legítima. |
| **B06** | Troncal con más postes que ramales: **comprobación**, no regla que altere un trazado confirmado. | Advertir si se incumple; no reordenar ni suprimir ramales para forzarla. |
| **B07** | Mostrar **distancias planas entre postes conectados**, diferenciadas de longitudes reales de cable/fibra. | No presentar suma de distancias proyectadas como metraje real de cable con reservas. |

La conectividad validada se modelará en un archivo/tabla aparte de los elementos. La búsqueda de vecinos o un DFS no prueban por sí solos el recorrido real ni autorizan dibujar saltos; el generador deberá usar **aristas confirmadas** y representar ramas sin conexiones falsas de retorno.

## 5. Formato, plantilla y entregas CAD (C01–C10)

| ID | Decisión aceptada | Efecto vinculante |
|---|---|---|
| **C01** | **Una sola lámina A1 horizontal por auditoría.** | No fragmentar automáticamente una auditoría en varias hojas. Si no cabe legible, reportar la limitación para revisión de presentación, sin modificar la regla sin autorización. |
| **C02** | `poste` sin material/transformador usa **símbolo genérico provisional**; los XLSX no contienen material identificador. | No afirmar poste de concreto/madera/acero por inferencia. |
| **C03** | Numeración visible **independiente, generada por el pipeline**. | Conservar número original como metadato cuando exista, sin tomarlo como secuencia física autoritativa. |
| **C04** | Etiqueta visible por componente con **abreviatura de tipo + número + coordenada**. | Priorizar legibilidad y minimizar solapamientos; no eliminar datos exigidos para mejorar estética. |
| **C05** | Cajetín **editable**, con datos DATRA solo si existen. Aprovechar prioritariamente el marco ya adaptado en los DWG de **Mirador/Otay–Florido**, apegándose a la composición de la plantilla CFE. | No inventar razón social, logos, responsables, direcciones ni firmas. |
| **C06** | Conservar detalles constructivos de la referencia cuando **correspondan** a la instalación real. | No copiar detalles ADSS/herrajes si no aplican o carecen de respaldo. |
| **C07** | Entregar **DWG y PDF**, siendo el PDF generado **después de ejecutar scripts y validar el plano**. | Verificar tamaño A1, escala, ploteo, áreas y legibilidad antes de dar por terminado. |
| **C08** | Primero `01_configurar_plano.scr`, después `02_dibujar_auditoria.scr`. Plantilla DWT con diseño estático. | El segundo script inserta elementos y completa campos del plano. |
| **C09** | Resumen impreso: **postes, cajas de empalme y excedentes** como mínimo. Otros elementos/cálculos, **solo en summary interno**. | `Registro` subterráneo no forma parte del recuento auditable CFE. |
| **C10** | Mantener composición y simbología aplicable de CFE; **personalizar identificación empresarial y datos de cada auditoría**. | La base DATRA debe ser reusable y editable; no calcar datos ficticios. |

La plantilla debe incorporar el mapa de Tijuana sin que las posteriores auditorías tengan que volver a insertarlo manualmente. La obtención del DWG/DWT canónico exige auditar primero las geometrías y layouts reutilizables de los DWG históricos y resolver el CRS.

## 6. Plano general de infraestructura (D01–D02)

| ID | Decisión aceptada | Efecto vinculante |
|---|---|---|
| **D01** | Crear inicialmente una versión **exclusivamente desde `Postes_CFE.xlsx`**; después, una **versión consolidada** con ampliaciones verificadas. | El maestro es candidato a cobertura completa de la infraestructura auditada, **no cobertura total comprobada**. Las dos versiones deben distinguirse por nombre/versión. |
| **D02** | Un componente presente en el maestro **también debe aparecer** en el plano individual de su ampliación. | Deduplicar **dentro de cada plano**, nunca excluir de una auditoría porque también existe en la general. |

## 7. Operación esperada y directorios

```text
C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria\
├── AuditoriaCFE\                               # proyecto de pipeline; escribir solo aquí
│   ├── 00_Diagnostico\                         # existente, referencia
│   ├── recursos\                              # futura DWT + DWG vectorial
│   └── auditorias\                            # carpetas seleccionables por consola
│       ├── Natura\entrada\...\salida\
│       ├── Mirador\entrada\...\salida\
│       ├── Otay-Florido\entrada\...\salida\
│       └── Tijuana-General\entrada\...\salida\
└── Auditorias-20261104T035633Z-1-001\       # evidencia histórica, SOLO LECTURA
    ├── postes\                               # originales XLSX
    └── Auditorias\                           # DWG/PDF/CSV/TXT de referencia
```

La estructura interna `auditorias/` es una **convención aceptada de operación**, pero las carpetas aún pueden no existir. Cada entrada contiene uno o más XLSX. El proceso ofrece el nombre de carpeta, indica cuántos archivos procesará, normaliza y valida, informa incidencias, genera los CSV/summaries y prepara, una vez confirmada la topología, los dos SCR. No procesar todos los históricos por defecto ni modificar originales.

## 8. Consecuencias, salvaguardas y criterios de calidad

1. **Deduplicación sin pérdida de auditoría:** cantidad de filas/ocurrencias de entrada = suma de estados de procesamiento explicados; cada componente dibujado tiene fuente prevalente y todas las referencias duplicadas. El total impreso se obtiene de únicos dibujados, no de filas originales.
2. **Errores visibles:** coordenadas inválidas, fuera de ámbito o sustituidas desde auxiliares generan registro específico. Un plano preliminar puede producirse con parte válida; no declarar inventario completo por omisión silenciosa.
3. **Cambios frente al pasado:** validar extracciones contra CSV históricos por separado de las reglas nuevas (tipos canónicos, exclusiones y duplicados); reproducciones literales antiguas pueden contener errores.
4. **No confundir geografía y red:** no inferir enlaces automáticos por proximidad ni reconstruir la troncal solo por los extremos del archivo.
5. **Una lámina A1:** escala y etiquetas deben verificarse para que quepan. Si no hay legibilidad suficiente, elevar una incidencia de diseño, no producir subláminas sin aprobación.
6. **Custodia:** lecturas a `Auditorias-20261104T035633Z-1-001` solo de lectura, outputs solamente en `AuditoriaCFE`, y evitar que Git rastree fotos, fuentes gigantes y archivos de bloqueo de AutoCAD.
7. **Compatibilidad:** verificar en AutoCAD que los dos `.scr` sean ejecutables en el entorno real y que el DWG/PDF coincidan con la hoja y los conteos.

## 9. Puntos aún abiertos: no confundir con decisiones aprobadas

| ID pendiente | Pregunta de cierre | Cuándo se necesita |
|---|---|---|
| P-01 | ¿Cómo se fija **de forma determinista** el “primer archivo analizado”: manifiesto de precedencia explícito, orden visible confirmado por usuario u otra convención? | Antes de deduplicar productivamente. |
| P-02 | ¿Cuál será la **línea base histórica exacta** para marcar “nuevo” en A02 y cómo se etiqueta cuando no existe? | Antes del summary comparativo. |
| P-03 | ¿Cuál es el perímetro/umbral geográfico esperado de Tijuana y la política de alerta por posiciones remotas pero mundialmente válidas? | Antes del validador final. |
| P-04 | ¿Cuál es el criterio formal de **liberación final** cuando existen incidencias de coordenadas sin resolver? A07 solo autoriza continuar en modo preliminar. | Antes de declarar entregables finales. |
| P-05 | ¿Cómo se declaran/convalidan inicios, extremos, aristas y ramificaciones en ausencia de topología formal? | Antes de generar rutas CAD. |
| P-06 | ¿Qué DWG donará mapa/marco, cuál es su sistema geodésico real y cómo se resuelve la discrepancia geográfica previa? | Antes de crear DWT y Script 01. |
| P-07 | ¿Qué información empresarial acreditada se proporcionará para cajetín y qué componentes de la referencia CFE sí aplican? | Antes de congelar DWT final. |
| P-08 | ¿Cómo asegurar etiquetas legibles y escala en una sola hoja A1 para auditorías extensas? ¿Qué hacer si resulta físicamente inviable? | Antes de aceptar el render final. |
| P-09 | Confirmar esquema detallado de `summary.csv`, reporte de duplicados/linaje, criterios de presentación y convenciones deterministas de exportación. | Al cerrar contrato e implementar ETL. |
| P-10 | Verificar en una corrida CAD la versión/configuración real de AutoCAD 2026, idioma de comandos, impresión A1 y exportación PDF. | Antes de automatización CAD final. |
| P-11 | Reconciliar la diferencia histórica de conteos de duplicados (56 vs. 58 para Mirador) explicando la clave y ámbito exactos. | Antes de usar cifras históricas como criterio de regresión. |

Los pendientes no anulan las decisiones aprobadas ni deben contestarse todos ahora. Solo bloquean la **etapa que los necesita**. Ningún ajuste derivado de la inspección de scripts heredados sustituirá silenciosamente este ADR: se documentará como nueva decisión o enmienda aprobada.

## 10. Estado y próximos hitos

- **Completado:** diagnóstico XLSX Fase 1A, reconstrucción documental AS-IS, propuesta TO-BE y aprobación del presente conjunto A/B/C/D.
- **Siguiente hito:** evaluación técnica, **en conversación y sin documento independiente por ahora**, de los scripts JavaScript y sus CSV para extraer patrones reutilizables y detectar incompatibilidades.
- **Después:** validar los pocos contratos técnicos pendientes, recuperar la base CAD y aprobar la versión canónica DATRA; preparar el encargo de implementación para Codex de **ETL 1A** primero, sin autorizar anticipadamente 1B/1C/CAD.

**Regla de gobierno:** cuando una nueva decisión contradiga este ADR, registrar la sustitución, el motivo, la fecha y la aprobación del responsable; no modificar este historial como si nunca hubiera existido.
