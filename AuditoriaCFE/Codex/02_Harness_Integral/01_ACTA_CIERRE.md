# Acta de cierre funcional y técnico — 75 respuestas

**Fecha:** 2026-11-05. **Rama/commit de referencia:** `codex/etl-unificado-auditoria-js` / `f306074`.
**Fuente primaria:** `00_RESPUESTAS_ORIGINALES.md`, preservada textualmente; este acta resume e interpreta las respuestas y NO suplanta el texto de origen.
**Autoridad:** responsable del pipeline, conforme a las respuestas Q01–Q75. Contradicciones con ADR-000 se registran como enmienda explícita en ADR-001.

## Resultado del cierre

- 52 acuerdos operativos explícitos (C).
- 18 acuerdos de procedimiento cuyo resultado exige **evidencia externa o ensayo** (V).
- 5 respuestas que necesitan una **interpretación técnica conservadora** para conservar contratos y evitar pérdida de datos (I). No justifican detener tareas independientes.

**C** = decisión aplicable; **V** = forma de proceder aceptada, el hecho no comprobado; **I** = interpretación implementable que necesita validación contra el contexto completo y debe quedar trazada en la entrega.

| Pregunta | Estado | Cierre o interpretación |
|---|---|---|
| Q01 | C | Objetivo implementación E2E: software + CSV + dos SCR + DWT/WCS acreditadas y ensayo CAD; la aceptación final DWG/PDF sigue siendo humana. |
| Q02 | C | E2E de Natura, Mirador, Otay–Florido y Tijuana-General; Bomberos queda como candidata independiente posterior. |
| Q03 | C | Mirador incluye STD, Canal 12 y la copia de STD; copia como antecedente deduplicable. |
| Q04 | C | Mirador: precedencia STD → Canal 12 → copia; hoja vacía reconocida, sin elementos. |
| Q05 | I | Otay: el desorden de puntos NO codifica topología; conservar orden técnico determinista de fuentes para reproducibilidad/A05, no como orden de ruta. |
| Q06 | C | Natura: solo Natura - Datra.xlsx, con sus 14 subrutas literales. |
| Q07 | C | General v1: solo Postes_CFE.xlsx; versión consolidada de ampliaciones por separado. |
| Q08 | V | Los DWG/DXF de recursos son BASE CAD, no baseline de novedades históricas; sin una comparación histórica de datos se conserva NO_DETERMINADO. |
| Q09 | C | Rutas de Excel literales; alias únicamente en presentación mediante tabla explícita. |
| Q10 | C | Contrato de 12 columnas CSV 00 ratificado con versión y semántica de manifiesto. |
| Q11 | I | Separar vista deduplicada limpia y bandeja/CSV de REVISAR, sin perder grupos pendientes por P-03 ni vaciar CP-01; definir vistas versionadas. |
| Q12 | C | CSV 01 de tres columnas literal; CSV 02 técnico versionado, compatibles con flujos previos. |
| Q13 | C | ruta_id estable en contrato nuevo, conservar nombre literal visible y migración versionada. |
| Q14 | C | Un único bloque/etiqueta por componente; asociaciones a subrutas separadas. |
| Q15 | C | Número original Excel es metadato; no ID físico fiable por defecto. |
| Q16 | V | IDs de equipo reales pueden distinguir cajas co-localizadas; el ID normalizado generado NO certifica dos equipos distintos. |
| Q17 | C | Archivo auditado de resoluciones manuales por fila/hash/evidencia/responsable/fecha; originales inmutables. |
| Q18 | C | Coordenada primaria válida prevalece; auxiliares solo en recuperación inequívoca sin especulación. |
| Q19 | C | Catálogo físico final solo POSTE/CAJA_EMP/EXCEDENTE; mapear variantes inequívocas de XLSX y revisar desconocidos. |
| Q20 | V | Área por auditoría/corredor con evidencia, no municipio completo arbitrario. |
| Q21 | C | Polígono o corredor GeoJSON/KML aprobado; rectángulo solo diagnóstico o límite provisional indicado. |
| Q22 | V | Autoridad de área: archivo espacial versionado + responsable y evidencia; no inferir de los mismos puntos. |
| Q23 | C | Fuera de ámbito mundialmente interpretable: revisión separada; no promover a 01 sin excepción acreditada. |
| Q24 | C | Errores históricos enumerados: excluir del dibujo/CSV admitido y documentar cada omisión; nunca borrar fuente o linaje. |
| Q25 | C | FINAL requiere acta, validaciones necesarias y cero incidencias bloqueantes abiertas para el artefacto. |
| Q26 | I | Permitir pruebas visuales con CRS candidato solo en COPIAS, rotuladas NO VERIFICADO; nunca etiquetar como 02 validado/DWG FINAL sin P-06. |
| Q27 | C | Correcciones individualizadas con evidencia; perímetro puede aprobarse por lote. |
| Q28 | V | Codex propone cercanos_m diagnóstico; owner lo valida en ensayo manual final. |
| Q29 | C | Base para operar: PlantillaMarcoDatraMapaTijuana.dwg; 146468_PLANOTIJUANA.dwg referencia de origen CFE. |
| Q30 | C | DWG DATRA actual y DXF empresarial del marco; ajuste pendiente del marco no bloquea desarrollo de código. |
| Q31 | C | DWT con mapa embebido; sin XREF externo obligatorio en primera entrega. |
| Q32 | V | Codex prepara selección asistida de dos controles independientes WCS contra WGS84; usuario selecciona/valida si GUI requiere interacción. |
| Q33 | V | Mirador muestra UTM84-11N y metros; DWG DATRA no acreditado; EPSG:32611 sigue sujeto a prueba. |
| Q34 | V | Tolerancia técnica se mide y documenta según controles y finalidad, sin inventar cota normativa. |
| Q35 | C | No aplicar corrección artificial de offset/escala/traslación; detener certificación si controles fallan. |
| Q36 | C | Vías principales; nombres opcionales; mapa limpio reversible y no destructivo. |
| Q37 | V | DWT se prepara una vez, se prueba con DWG nuevo, mapa, A1, controles, bloques, detalles y ploteo; luego se reutiliza. |
| Q38 | V | KMZ empresarial existente con postes/IDs y rutas: importar solo copia; determinar qué geometrías contienen conectividad real. |
| Q39 | C | Si no hay aristas confirmadas, emitir dos SCR capaces de dibujar solo puntos PRELIMINAR, sin PLINE inventada. |
| Q40 | C | Aprobación en topologia_confirmada.csv con evidencia y validación visual en mapa/AutoCAD. |
| Q41 | V | Inicios/finales reales desconocidos: no asignar extremos como hechos; registrar candidatos hasta evidencia. |
| Q42 | C | Troncal declarada por autoridad; mayor cantidad de postes solo diagnóstico B06. |
| Q43 | C | Solo postes como soportes de grafo por defecto; cajas/excedentes asociados separadamente. |
| Q44 | C | Soportar ciclos, cruces, conexiones múltiples y componentes aislados; infraestructura global tiene tres anillos de redundancia. |
| Q45 | C | Aristas versionadas con IDs origen/destino, ruta/tramo, clase, evidencia; no una PLINE única DFS. |
| Q46 | C | Distancia plana para todas las aristas físicas confirmadas; redondeo solo visual. |
| Q47 | C | Proponer aristas por proximidad y/o KMZ como candidatas con score/razón, nunca como confirmadas automáticamente. |
| Q48 | C | Alertas configurables: saltos, aislados, cruces, ciclos, troncal/ramales, desconexiones; no excluir por cercanía. |
| Q49 | C | AutoCAD 2026 convencional en inglés; soporta SCR y LISP; usar comandos globales y ensayar prompts. |
| Q50 | C | Codex autorizado a ensayar CAD en copias; si no puede usar GUI, continúa con tareas offline y marca gate manual. |
| Q51 | C | Dos SCR operativos exactos; LISP de apoyo empaquetado sin tercer paso manual. |
| Q52 | C | DWT contiene mapa, papel y recursos estáticos; SCR01 configura/verifica sin insertar mapa doble. |
| Q53 | V | Bloques por tipo, preferir simbología CFE aplicable; comparar referencia antes de congelar diseño. |
| Q54 | C | Numeración P-001/C-001/E-001 por clase estable por elemento_id, no por recorrido. |
| Q55 | C | Etiqueta abreviatura+número+lat/lon fuente; CRS de dibujo en leyenda, precisión sin modificar identidad. |
| Q56 | V | Recuperar cinco detalles constructivos aplicables; si no hay original, esquema propio genérico sujeto a revisión, nunca detalles reales inventados. |
| Q57 | V | Cajetín DATRA editable; datos reales solo si acreditados; campos ausentes vacíos. |
| Q58 | C | General A1 única; probar recuadros/tabla/escala; si ilegible emitir bloqueo FINAL y proponer excepción ADR sin aplicarla. |
| Q59 | V | Perfil ploteo A1, CTB/STB, grosores/escala/nombres probados en AutoCAD. |
| Q60 | V | Antes de publicar nuevos mapas/DWT/logos comprobar permisos/licencias; si no está acreditado, mantener binarios no públicos. |
| Q61 | I | El usuario cree cubiertos datos privados por .gitignore; verificar qué configuraciones/topología son trackeables y bloquear fugas en git preflight. |
| Q62 | C | Codex puede LEER originales ignorados y COPIARlos a entrada por auditoría con hashes, sin escribir histórico. |
| Q63 | C | Codex puede generar recursos canónicos en AuditoriaCFE/recursos desde copias con respaldo/manifest. |
| Q64 | C | Autonomía de ingeniería dentro de contratos; no inventar negocio/CRS/conectividad/final. |
| Q65 | C | Ante gate físico bloqueado continuar fases independientes, registrar evidencia y no declarar FINAL ficticio. |
| Q66 | C | Continuar en rama actual codex/etl-unificado-auditoria-js; commits por checkpoint; push y PR listo, SIN merge autónomo. |
| Q67 | V | Suite completa + CI GitHub Actions + protección de ramas; si API no autoriza la regla, pasos manuales exactos. |
| Q68 | C | Modo --batch después de CLI individual estable, auditorías aisladas y reporte global. |
| Q69 | V | Benchmark/suite de rendimiento mide tiempos/RAM y permite fijar SLA después, sin inventarlo antes. |
| Q70 | C | Usuario aprueba checkpoints y planos finales; acta con evidencias, hashes, fecha y estado. |
| Q71 | C | TO-BE v0.3 corrige inversión ordenar/trayectoria y consolida CP-01..CP-04; ADR-000 se conserva. |
| Q72 | I | Artefactos operativos persistentes en entrada/salida; documentos del agente bajo Codex; excepción explícita para código/configuración/docs oficiales; migrar manifiestos sin romper atomicidad. |
| Q73 | C | 56/58 Mirador: reconciliar definición técnicamente sin bloquear CP-02 por cifra AS-IS no reproducible. |
| Q74 | C | Checklist por auditoría: pruebas, hashes, conteos, capturas CAD, DWG y PDF A1. |
| Q75 | C | Autoridades nuevas: ADR-001, TO-BE v0.3, P-09, AGENTS y recursos canónicos verificados; carpeta histórica ignorada NO es canónica versionada. |

## Seis reconciliaciones fundamentales

### R-01 — Q05, orden de fuente ≠ orden del recorrido

El usuario afirma que las coordenadas están desordenadas. Esto **no deroga** la exigencia A05 de un orden determinista de fuentes para resolver prevalentes. Para Otay mantener o definir lista estable de fuentes (la de las configuraciones de prueba es un punto de partida), pero usarla **solo para desempate y linaje**; jamás para construir trayectorias. Si dos fuentes aportan atributos incompatibles que alteran la identidad, dejar incidencia y prueba, no escoger un trazado físico arbitrario. No usar `mtime`.

### R-02 — Q08, base CAD ≠ baseline de novedad

Los DWG/DXF del directorio `recursos/` son la base cartográfica y visual actual. No son automáticamente una base *de componentes anteriormente auditados* para marcar NUEVO/EXISTENTE. `baseline_historica=null` y `NO_DETERMINADO` persisten hasta aportar una fuente de inventario anterior, su fecha y correspondencia. Sí usar Mirador para contraste geodésico histórico, **no como calibración automática**.

### R-03 — Q11, CSV limpio y revisión separada

Mantener `00_elementos_unificados.csv` **con su identidad y 12 columnas ratificadas (Q10)** y garantizar que no contiene duplicados físicos adicionales ni registros imposibles. Producir **`00_elementos_revision.csv`** como bandeja separada de cualquier ocurrencia/caso que requiera acción. Una revisión global P-03 pendiente no convierte automáticamente un componente interpretado y deduplicado en un *dato inválido*: conservarlo visible en 00 con `apto_csv_01=NO`, pero en el auxiliar documentar que necesita aprobación geográfica. Casos con defecto individual no pueden entrar a 01 hasta resolución.

Si tras observar prototipos el owner requiere que los `REVISAR` identificables desaparezcan de 00, no perder su identidad: mantener un snapshot consolidado no destructivo e introducir una vista filtrada, **sin sobreescribir de modo silencioso el contrato CP-01 de 0.2.0**. Esta es la interpretación más compatible con la petición original de no volver vacío el primer CSV.

### R-04 — Q24/Q26, descartes y CRS de prueba

“Eliminar” coordenadas evidentemente erróneas significa **excluir de CSV 01/02 y CAD**, no suprimir filas originales, linaje ni incidentes. El usuario permite una visualización con CRS candidato cuando falten controles: se podrá generar un **ensayo CAD explícitamente marcado DIAGNOSTICO_CRS_NO_VERIFICADO sobre una COPIA**, usando EPSG:32611 como candidato y sin presentarlo como ubicación cierta. El 02 productivo mantiene el gate P-06; ningún plano FINAL se declara sin CRS verificado.

### R-05 — Q16/Q38, ID de equipo vs ID interno

`elemento_id` calculado es una clave de software para una identidad inferida por regla aprobada; **no prueba** que existan dos cajas en el mismo punto. La excepción multi-equipo exige ID externo acreditado (etiqueta/inventario/KMZ corroborado) y fuente. El KMZ puede ofrecer geometrías de rutas o solamente marcadores: debe inspeccionarse en copia sin afirmar conectividad hasta su validación.

### R-06 — Q61/Q72, ubicación de salidas vs custodia Git

Los **artefactos persistentes generados** (CSV, SCR, informes operativos, manifiestos por corrida, capturas para esa auditoría) vivirán dentro de `auditorias/<nombre>/salida/`, y los insumos operativos copiados dentro de `entrada/`. Código, configuración estructural, documentación normativa y herramientas quedan en sus carpetas explícitas de repo; informes/planes producidos por Codex van a `AuditoriaCFE/Codex/`. Se permite temporal de trabajo **efímero** fuera de `salida/` para conservar publicación atómica, nunca como lugar permanente de artefactos. Migrar manifiestos antiguos a una ubicación nueva de manera verificable y retrocompatible.

La transcripción íntegra `00_RESPUESTAS_ORIGINALES.md` es **local/confidencial** y se ignora mediante `.gitignore` del harness. Los datos reales de conectividad/perímetros/configuraciones potencialmente sensibles **no están automáticamente ignorados** por Git si se guardan en raíz de una carpeta auditora. Usar `entrada/` ignorada o configuración pública sin detalles sensibles; verificar `git status --ignored` y `git diff --cached` antes de push. No asumir protección por el nombre del archivo.

## Gates de evidencia que siguen abiertos aun con 75 respuestas

1. **GEODESIA:** `PlantillaMarcoDatraMapaTijuana.dwg` debe comprobarse en WCS contra dos puntos espaciales reales independientes; Mirador visible como UTM84-11N y metro no basta. Tolerancia se propone con medición; usuario autoriza el método, no un número arbitrario.
2. **KMZ/TOPOLOGÍA:** el KMZ mencionado no figura en el inventario local aportado; Codex debe recibir su **ruta exacta autorizada** cuando el archivo esté disponible. Importación no equivale a aristas aprobadas. Inicios/finales no conocidos.
3. **MARCO:** 90 % listo según usuario, pero la DWT canónica y los detalles imprimibles A1 requieren prueba final en AutoCAD. El ajuste restante no impide escribir el compilador.
4. **PUBLICACIÓN:** comprobar licencia/permiso antes de versionar nuevas versiones del DWG/DWT/logo/mapa en un repo actualmente público.
5. **ACEPTACIÓN:** el pipeline puede quedar implementado y probado offline con gates CAD o de campo pendientes; nunca etiquetar FINAL automáticamente.

## Alcance fijo de entrega

Prioridad de integración: **Natura → Mirador → Otay–Florido → Tijuana-General**. Bomberos permanece opción separada, no requisito para cierre de la primera entrega. Un solo DWG/PDF A1 por auditoría, a partir de la base DATRA, sin inserción duplicada del mapa; dos scripts y operación manual de guardado/ploteo. Tres anillos de redundancia existen en la infraestructura como conocimiento de campo del owner, **no deben dibujarse como tres ciclos sin que el KMZ y las aristas lo acrediten**.
