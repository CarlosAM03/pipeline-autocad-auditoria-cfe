# Auditoría CFE / DATRA — Revisión técnica de A4.2 y plan de cierre A4.2.1–A4.2.2

**Fecha de revisión:** 2026-11-09  
**Repositorio:** `CarlosAM03/pipeline-autocad-auditoria-cfe`  
**Rama / HEAD revisado:** `codex/etl-unificado-auditoria-js` / `6a02513ec840b4be796463146321e4ba63e2469f`  
**PR #1:** abierto, sin merge  
**Estado de este documento:** dictamen independiente; A4.2 técnicamente ejecutado, **no aceptado todavía como plantilla maestra definitiva**.  
**Ámbito:** presentación y recursos visuales de tres rutas, custodia de plantilla, transferencia de datos a tablas; no valida CRS, topología ni campo.

## 1. Bases documentales y evidencia revisada

- Tres PDF A4.2 proporcionados: `Natura_A4_2.pdf`, `Mirador_A4_2.pdf`, `Otay-Florido_A4_2.pdf` (16, 10 y 12 páginas, respectivamente). Se inspeccionaron las páginas de forma visual y por estructura PDF.
- Publicación GitHub del commit `6a02513`, sus 21 archivos cambiados desde `be103b4`, documentos `A4_2_Plantilla_Maestra/*`, ADR-003 y los módulos CAD; workflow GitHub Actions `42614772313`, cuatro jobs exitosos.
- Cierre aprobado `CIERRE_CHECKPOINT_A4_1_1_Y_A4_1_2026-11-09.md`: radio de proximidad **300 m** como predeterminado para perfiles diagnósticos multipágina de Natura, Mirador y Otay–Florido.
- Árbol local de recursos y de auditorías suministrado por el owner. Los archivos locales DWG/DWT privados de A4.2 se conocen por manifiestos y actas de Codex; **no fueron abiertos aquí**: la verificación independiente del DWG queda expresamente pendiente.

### Verificación de PDF y CI

| Ruta | Páginas A1 horizontal | Identidades de origen | Elementos mostrados | No mostrados (trazados) | Resultado |
|---|---:|---:|---:|---:|---|
| Natura | 16 | 438 | 438 | 0 | PDF estructuralmente válido; logo y mini-mapa ausentes |
| Mirador | 10 | 493 | 472 | 21 | PDF estructuralmente válido; logo y mini-mapa ausentes |
| Otay–Florido, con Bomberos | 12 | 749 | 741 | 8 | PDF estructuralmente válido; logo y mini-mapa ausentes |
| **Total** | **38** | **1680** | **1651** | **29** | No constituye validación de infraestructura física |

- Dimensiones PDF examinadas: aproximadamente **841.02 × 594.08 mm** por hoja; cartografía principal dibujada como vectores (numerosos trazos).
- La primera página de cada PDF tiene **cero objetos `Image` raster embebidos** según `PyMuPDF.get_images(full=True)`. El recuadro de «Ubicación de zona» se ve vacío en la columna derecha. El texto **DATRA** en el cajetín no reemplaza el logo corporativo real `logo_datra.png`.
- Esta observación **no significa que falte el mapa base urbano**: aparece vectorialmente en la región central y se conservó en las comparaciones reportadas por Codex.
- GitHub confirma el workflow `42614772313` exitoso en Windows/Linux. Codex documenta suite local 103/103 y tres ensayos CAD nativos, sin auditoría manual de DWG por el revisor.

## 2. Qué logró A4.2

1. Recuperación editable de detalles históricos de **tensión (D01), suspensión (D02), empalme (D04) y otros elementos (D05)**, sobre una copia de `AuditoriaCFE2.dwg`.
2. **Derivación (D03) pendiente**: el diagrama histórico adicional corresponde a un cambio de dirección, no demuestra derivación. Se conservó por separado; no es correcto inventar contenido técnico.
3. Candidata de maestro `Plantilla_DATRA_CFE_A1_v1_0_0.dwg` (SHA publicado `62abf37880f95c0e895cfa0f6e3ef95fb7e620e4560586fc38cc72eda3901728`) y DWT derivada con SAVEAS nativo (SHA `51eb05563b77925276b94e5a1c8e92701869369452ebc839a5a98b684933748c`). Ambas permanecen en `AuditoriaCFE/tests/_runtime/a4_2/entrega_v2/`.
4. Tres rutas regeneradas en `AuditoriaCFE/auditorias/_a4_2/` con dos SCR, 300 m por defecto y resultados por identidad coincidentes con A4.1.1; formatos 16/10/12 páginas.
5. Comparación de los 38 planos: Codex reporta coincidencia píxel a píxel de mapa y cajetín a **50 dpi**. Eso prueba estabilidad de esas zonas al nivel ensayado, **no legibilidad final a 100% de tamaño de papel**.
6. Se eliminó en la candidata dos referencias raster rotas del layout legado. Esa limpieza evitó enlaces rotos, pero dejó sin restaurar los dos elementos visuales solicitados por el owner.
7. El default de **300 m** aparece documentado en ADR-003 y el módulo de visibilidad. El override permanece disponible y el filtro **no equivale a topología**. Las 29 identidades no representadas siguen en CSV, XLSX, linaje y reportes.

## 3. Observaciones expresas del owner — decisiones para cerrar la plantilla

| ID | Observación / decisión | Estado / efecto |
|---|---|---|
| O-01 | Falta el **logo DATRA** auténtico. Debe verse en el cajetín de cada hoja. | **Bloqueante A4.2.1**; imagen local `AuditoriaCFE/recursos/logo_datra.png`. |
| O-02 | Falta la **imagen de mapa de ubicación de zona** en el recuadro derecho, distinta del mapa vectorial principal. | **Bloqueante A4.2.1**; fuente `AuditoriaCFE/recursos/MapaTijuanaParaMARCO.png`. Si no permite señalar la zona real, conservar base y dejar referencia pendiente, no inventar ubicación. |
| O-03 | La plantilla anterior `PlantillaMarcoDatraMapaTijuana.dwg` era **preliminar**. La candidata A4.2 debe sustituirla como base operativa, no coexistir como plantilla activa ambigua. | **Autorizado con sustitución controlada, respaldo y rollback**; nueva maestra propuesta v1.0.0, aceptación formal al validar A4.2.1/A4.2.2. |
| O-04 | Los recursos se administran desde `AuditoriaCFE/recursos/`, pero la copia de trabajo de cada auditoría debe encontrarlos automáticamente. | Exige staging y rutas **relativas a la copia DWG** o solución realmente portable; registrar huella y dependencias. |
| O-05 | Mantener separadas la plantilla y las fuentes privadas de auditoría. | Un maestro limpio; no almacenar postes/rutas específicas en la base. |
| O-06 | Hará falta una **página de tablas** inspirada en la plantilla oficial de CFE, con datos estrictamente comprobables desde reportes internos. | **A4.2.2 posterior**: inventario de campos, tabla «disponible/derivable/no acreditado», sin rellenar con valores ficticios. |
| O-07 | El owner realizará lectura final de PDF y revisión manual de los tres DWG. | **Pendiente de aceptación física**; no inventar aprobaciones. |
| O-08 | Los tres perfiles aprobados mantienen escala, 300 m y PDF multipágina. | Invariante: 438/472/741 visibles; 0/21/8 exclusiones; 16/10/12 páginas **antes de añadir la hoja tabular A4.2.2**. |

## 4. Criterios para A4.2.1 — consolidación visual y distribución portable de recursos

**Objetivo:** sustituir la plantilla preliminar por la candidata con cuatro paneles válidos y referencias gráficas restauradas, manteniendo la separación de la futura hoja de tablas.

- Verificar `logo_datra.png` y `MapaTijuanaParaMARCO.png` (existencia, tipo real, dimensiones, transparencia, SHA-256). Considerar `FASE3B_Integracion_Desde_PlanoTijuana/`, `MARCO_DATRA_A1_EMPRESA_v0_2.dxf` y el mapa DWG solo como referencias de composición, sin reconstruir el mapa base.
- Definir **fuente canónica** (recursos DATRA) y **dependencia transportable**: un paquete autocontenido junto al DWG mutable —por ejemplo `resultados_cad/recursos/`—. Asegurar que las referencias almacenadas en DWG resuelven respecto a su directorio; validar `DWGPREFIX` y rutas leídas por AutoCAD. La copia inicial en `entrada` y la copia mutable de `salida/resultados_cad` pueden estar en directorios distintos; probar ambas. El nombre exacto de carpeta es una decisión de implementación reversible, no un nuevo contrato público hasta formalización.
- No basta con que los PNG existan en el árbol del repositorio: validar en **DWG guardado, cerrado y reabierto**, en otra ruta sin acceso al proyecto, y en el PDF multipágina trazado desde esa ubicación.
- Colocar logo completo, sin estiramientos y con transparencia contrastada sobre fondo blanco; insertar mapa de ubicación de zona legible en el recuadro existente sin falsear marcadores. Confirmar que se repite en las 38 páginas.
- Evitar que los PNG se vuelvan invisibles por `IMAGEFRAME`, capas apagadas, clipping, `PLOT`, rutas absolutas u orden de impresión. Si se convierte una imagen a entidades vectoriales, registrar conversión y fidelidad; no usar texto como sustituto del logo.
- Conservar dos SCR en orden `01_configurar_plano.scr` → `02_dibujar_auditoria.scr`; las dependencias pueden autoprepararse por Python/AutoLISP sin tercer SCR manual.
- Promover la candidata de `tests/_runtime/a4_2/entrega_v2` a recurso operativo solo **después** de preflight, backup versionado del antiguo maestro, verificación de la nueva base limpia, actualización de las referencias `cad.base_dwg` en los tres perfiles y pruebas. Sustitución atómica/recuperable; registrar HASH_ANTERIOR/HASH_NUEVO/ROLLBACK. Nunca borrar archivos históricos ni tocar los 12 lotes A4.1.1.
- Revalidar 300 m por defecto, filas excluidas, inventario, índices, XDATA, idempotencia y la continuidad de las 38 hojas.
- Generar los tres nuevos PDF, tres DWG de copia y un ZIP de evidencia de hasta ~15 MiB, excluyendo originales privados de publicación; manifest hashes y recortes a resolución suficiente.

**Criterio de salida:** A4.2.1 `TECNICAMENTE_COMPLETO_PENDIENTE_APROBACION`: logo y mapa de ubicación aparecen realmente en todos los layouts/PDF, y se encuentran después de trasladar los DWG con su paquete de recursos. Si falta un recurso o no resuelve la ruta, A4.2.1 **no se aprueba**.

## 5. Qué NO puede cerrarse durante A4.2.1

1. **D03 derivación:** falta fuente técnica identificada. Mantener señalización pendiente, no asumir que «cambio de dirección» es «derivación».
2. **Información tabular CFE:** el formato/columnas pueden recuperarse del PDF oficial, pero valores de herrajes, calibres, certificaciones, aforos, distancias de línea, materiales o instalaciones pueden ser desconocidos. No rellenar con estimaciones. A4.2.2 debe clasificar cada campo.
3. **Imágenes con rutas de red:** deben sobrevivir fuera de la PC original. Un enlace absoluto a `C:\Users\...` no es solución aceptable.
4. **Revisión humana de CAD/PDF:** Core Console y apertura de PDF no reemplazan la inspección GUI y física del owner.
5. **Gates P-03/P-05/P-06/P-07/P-08/P-04:** no aprobados por la restauración de imágenes. En particular las conectividades deben quedar **no confirmadas**; la visibilidad de 300 m nunca certifica infraestructura.
6. **Publicación GitHub:** no publicar logo, mapas, DWG/DWT, PDF de cliente, XLSX ni otros recursos privados simplemente para facilitar rutas de despliegue. Mantener manifiestos públicos saneados.

## 6. A4.2.2 — hoja de tablas tipo CFE, contrato previsto

Tras aceptación de A4.2.1:

- Inspeccionar `Auditorias-20261104T035633Z-1-001/Plantilla (3)-ejemplo.pdf` y `AuditoriaCFE2.dwg` para extraer únicamente **estructura, encabezados y unidades** de las tablas oficiales; documentar versión y fuente, revisar permiso de uso.
- Hacer matriz por columna: `campo solicitado`, `definición`, `fuente`, `regla de agregación`, `unidad`, `nivel de evidencia`, `valor derivable`, `responsable de aprobar`.
- Candidatos basados en los reportes actuales (sujetos a contraste): auditoría/subruta, fecha de ejecución **distinta de fecha de levantamiento**, inventario POSTE/CAJA_EMP/EXCEDENTE, exclusiones visuales 300 m, conteos por fuente/ruta, incidencias/calidad, resumen de trazabilidad y páginas; **no inventar** longitud real de cable, enlaces físicos, materiales, herrajes o datos de campo.
- Generar **una o varias hojas tabulares A1 del mismo PDF** por ruta, después de las hojas existentes. Mantener una sola salida PDF por auditoría, índice/orden consistentes y plantilla preservada. No presentar 16/10/12 páginas como cantidad inmutable una vez agregadas tablas: son la **línea base cartográfica**, a la que se añaden hojas tabulares.
- Campos no disponibles: `NO DISPONIBLE / PENDIENTE EVIDENCIA` con justificación; nunca valores 0 como sustituto de desconocidos.
- Preparar revisión de las tablas con el owner antes de declarar paquete final para entrega a CFE.

## 7. Datos adicionales a solicitar al owner durante A4.2.1 (sin bloquear tareas técnicas)

| Necesidad | Para qué | Estado |
|---|---|---|
| Confirmar que `logo_datra.png` es el logotipo vigente y autorizarlo para plano corporativo | Branding | Ruta local entregada; vigencia/uso por confirmar |
| Confirmar que `MapaTijuanaParaMARCO.png` es el mapa correcto para «Ubicación de zona» y si requiere resaltado por ruta | Plano de ubicación | Archivo localizado, semántica por confirmar |
| Precisar qué tabla(s) concretas del ejemplo CFE deben reproducirse y si hay norma aplicable | Diseño A4.2.2 | Pendiente, se puede inventariar primero |
| Señalar fuente autorizada para D03 Derivación, o aceptar panel pendiente | Detalles constructivos | Pendiente |
| Metadatos de cajetín: nombre aprobado del plano, responsable, fecha de levantamiento, revisión, escala, contrato/folio si existe | Tablas y entrega | Pendientes; no sustituir con fecha de ejecución |
| Aprobación manual de los tres DWG resultantes y los PDF finales | Aceptación | Pendiente |

## 8. Checklist por checkpoint

| Control | A4.2 histórico | A4.2.1 previsto | A4.2.2 previsto |
|---|---|---|---|
| Cuatro detalles D01/D02/D04/D05 | Recuperados por Codex; sin certificación técnica | Preservar | Sin cambios |
| D03 | Pendiente fuente | Mantener aviso | Resolver por evidencia independiente si surge |
| Plantilla maestra | Candidata privada DWG/DWT; base preliminar aún operativa | Promoción controlada; hashes y rollback | Usar base aprobada |
| Logo DATRA | No visible | Incorporar y probar portabilidad | Preservar |
| Mapa de ubicación | Recuadro vacío | Incorporar/identificar alcance | Preservar |
| Cartografía principal | Visible vectorial | Conservar | Conservar |
| Radio 300 m | Integrado en diagnósticos | Validar de nuevo | Preservar |
| 38 hojas cartográficas | 16+10+12 | Mantener | Agregar hojas tabulares sin perderlas |
| Inventario de 1,680 | 1,651 visibles / 29 exclusiones | Sin cambios | Tablas con conteos diferenciados |
| Dos SCR | Ensayados | Mantener | Mantener |
| PDF legible y portable | Solo verificación parcial; sin logo/mapa | Validar nuevas imágenes/rutas | Validar paquete final |
| Tablas tipo CFE | Sin nueva página | Fuera de alcance | Generar según fuentes acreditadas |
| PR, CI y custodia | 4 jobs verdes; PR abierto | Tests + publicación segura | Tests + aceptación final |

## 9. Riesgos y criterios de bloqueo

- **R1 crítico:** mover el DWG rompe referencias a raster. Prueba de portabilidad en nueva ruta obligatoria.
- **R2 alto:** sustituir la base antes de validar, o sobreescribir un original. Backup + rollback obligatorios.
- **R3 alto:** logo o ubicación ausentes aunque imágenes estén en disco. Validar por PDF y referencias CAD reales.
- **R4 alto:** regenerar planos con distinta selección espacial. Comparar por ID, no solo por número de páginas.
- **R5 medio:** fuente `simplex.shx` sustituyó estilos históricos y puede afectar etiquetas constructivas. Inspección de detalles ampliados.
- **R6 alto:** tablas tipo CFE aparentan mediciones que no están acreditadas. Faltantes explícitos y aprobación.

## 10. Resultado y transferencia

**Dictamen:** A4.2 tiene evidencia de implementación y regresión técnica, pero **no se aprueba aún como plantilla operativa definitiva** porque faltan las dos imágenes gráficas solicitadas y la candidata sigue separada del recurso base preliminar. Continuar con **A4.2.1 (recursos, rutas y sustitución controlada)** y luego **A4.2.2 (tablas tipo CFE)**, dejando el cierre final v1.0.0 sujeto a revisión manual de DWG/PDF, validación de datos y gates geográficos independientes.

**Fuentes principales:** repositorio PR #1 SHA `6a02513`, workflow `42614772313`, actas públicas A4.2, los tres PDF A4.2 recibidos y observaciones del owner. Las copias DWG/DWT privadas no se inspeccionaron por este revisor, por lo que la aceptación CAD manual sigue pendiente.
