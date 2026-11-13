# Plan de implementación autónoma integral — Codex

**Punto de partida:** rama existente `codex/etl-unificado-auditoria-js`, commit `f306074`.
**Criterio de avance:** tareas técnicas no bloqueadas continúan; los gates humanos de CRS, topología y AutoCAD se documentan sin inventar aprobación.
**No autoriza** merge a `main` ni modificación destructiva del histórico.

## Fase 0 — Preflight y congelación de contexto

**Entrada:** Q01–Q75 y ADR-001/TO-BE v0.3/Contrato P09.
**Tareas:** leer `AGENTS.md` actualizado, comprobar rama/HEAD/remoto, `git status`, `git ls-files`, `git check-ignore`; documentar archivo rastreado `README_ENTREGA_Y_PASOS.md` actualmente eliminado y copia en `temp/` ignorado. Decidir en esta fase una de dos opciones *conservadoras* sin pérdida: restaurar el archivo original o moverlo con `git mv` a `AuditoriaCFE/Codex/00_Diagnostico/` preservando el contenido; elegir movimiento documental solo si comprueba hash/contenido y deja historial recuperable. No usar git clean/reset destructivos. Auditar patrón gitignore respecto a topología/configs privadas; no incluir datos de campo en commit.

**Resultado/commit:** `docs(harness): cierra decisiones e inicia plan integral`; acta y docs, diff revisado, baseline de 43 tests.

## Fase 1 — Contratos, limpieza y selección de entradas (CP-01 extendido)

1. Introducir vistas/`00_elementos_revision.csv` sin alterar los 12 campos de 00 ni las tres columnas del 01.
2. Crear y probar `resoluciones_manual.csv` con SHA+fila+evidencia y mecanismo de exclusión sin pérdida de linaje.
3. Normalizar variantes inequívocas de tipo de fuente; asegurar catálogo exacto de tres clases.
4. Crear copias de los archivos declarados de históricos a `entrada/` de cuatro auditorías: Mirador (STD, Canal, copia), Otay (Vía Rápida, FLO final, Protección Civil), Natura (un libro), General (Postes_CFE.xlsx). Orden para identidad fijo/versionado, nunca orden de grafo. Comparación maestra separada.
5. Conciliar reportes/duplicados y asegurar que valores erróneos listados quedan fuera de dibujo con motivos. Conservar 494/749 grupos como controles históricos antes de aplicar nuevas resoluciones y cambios de alcance.
6. Implementar esquema GeoJSON/KML de perímetro y opción de excepciones; no asumir polígono autorizado si todavía no existe archivo de zona acreditado.

**Salida:** CP-01 + revisión claros, fixtures de prueba sintética y cuatro configuraciones declaradas, regresiones y manifiesto.
**Commit:** `feat(cp01): incorpora resoluciones y bandeja de revision`.

## Fase 2 — Geodesia, CP-02 y compatibilidad

1. Recuperar desde `recursos` la base DATRA `PlantillaMarcoDatraMapaTijuana.dwg`, DXF marco y mapas, trabajando en copias. Contrastar con Mirador en metros y UTM84-11N, y `146468` como herencia CFE.
2. Preparar LISP/instrucciones de captura de dos controles WCS y WGS84 con validación contra `pyproj`; **Codex no elige por intuición puntos que no puede identificar**. Si no hay GUI, documenta control manual y continúa módulos independientes.
3. Usar lat/lon geográficas solamente en CP-01 y 01 cuando pasen P03. CSV02 solo con controls. Evaluar caso `INSUNITS=4` base vs `INSUNITS=6` histórico: no escalar a mano sin prueba.
4. Evolucionar 02 v1→v2 con `ruta_id` verdadero + `ruta_nombre`, migración y fixtures.
5. Crear modo diagnóstico explícito CRS candidato sobre copia, con rótulo imposible de confundir con entrega final y SIN sustituir CSV02 validado.
6. Migrar manifiestos para que los persistentes residan bajo salida y ampliar verificador, conservando lectura de ejecutados 0.2.0.

**Commit:** `feat(cp02): valida geodesia y contratos versionados`.
**Gate separado:** evidencia real de CRS. Si no existe, CP-02 productivo = PENDIENTE_EVIDENCIA, no falla del software.

## Fase 3 — Integración KMZ y topología auditada

1. Buscar solo la ruta local **expresamente autorizada** del KMZ. Si no está bajo los paths declarados, registrar `KMZ_NO_DISPONIBLE` y continuar con pruebas sintéticas; no buscar otras carpetas privadas automáticamente.
2. Importador KML/KMZ seguro: ZIP sin traversal/bomb, tamaños máximos, no extracción innecesaria; Point/LineString/MultiGeometry/ExtendedData, coordenadas lon,lat,alt; identidad y rutas de origen trazables.
3. Matching KMZ↔CSV 00 por IDs externos acreditados y por geometría como CANDIDATOS con tolerancia configurable; no usar número de fila Excel como autoridad.
4. Producir propuestas de aristas y controles de calidad, conectividad desconectada, ciclos/los tres anillos **si acreditados**, ramales y troncal diagnóstico.
5. Cargar topologia_confirmada.csv aprobada humanamente y rechazar aristas inventadas/incompatibles; modo solo-puntos si ninguna arista acreditada.
6. Probar bifurcaciones, cruces visuales sin unión, ciclos, subrutas compartidas, casos con extremos desconocidos y B06 como advertencia.

**Commit:** `feat(topologia): integra KMZ y aristas verificables`.
**Gate:** sin confirmaciones no se dibujan rutas definitivas.

## Fase 4 — Plantilla DATRA canónica y CP-03

1. No reconstruir el mapa desde cero; basarse en `PlantillaMarcoDatraMapaTijuana.dwg` con la edición de marco pendiente. Inspeccionar primeramente capa/Model/Paper, `INSUNITS`, WCS/UCS, bloques, fonts, dependencias, legibilidad y A1.
2. Reutilizar recursos CFE/DATRA y cinco detalles cuando haya evidencia; si no existen, crear prototipo esquemático marcado no homologado. No inventar cable/herraje real.
3. Generar o especificar la DWT de nombre canónico `Plantilla_Auditoria_CFE_Tijuana.dwt`. Guardar con AutoCAD nativo cuando esté disponible; nunca afirmar DWT creada por una copia renombrada a .dwt.
4. Crear `01_configurar_plano.scr` determinista, idempotencia/estado, comandos globales, LISP autoinvocado empaquetado cuando sea necesario. No duplicar mapa ni insertar postes.
5. Validar en copia de DWG nacida de DWT, imprimir A1 si AutoCAD es accesible; documentar gate GUI de otro modo.

**Commit:** `feat(cp03): configura plantilla DATRA AutoCAD`.
**Gate:** DWT canónica requiere prueba nativa real.

## Fase 5 — CP-04, símbolos, trazado y pruebas CAD

1. Generar exactamente `02_dibujar_auditoria.scr` consumiendo 02 validado + aristas confirmadas; en ausencia de aristas, puntos preliminares.
2. Bloques tipo POSTE/CAJA_EMP/EXCEDENTE, IDs P/C/E por categoría, coordenadas fuente legibles, dedup física, capas, conteos, cajetín.
3. Polilíneas por **aristas confirmadas** sin saltos ni regresos falsos DFS; ciclos, ramas y desconectados; longitudes planas mostradas para aristas confirmadas.
4. Validar número de INSERTs y líneas respecto a CSV/manifiesto. No usar PDMODE global como símbolo por entidad.
5. Probar A1 horizontal en Natura, Mirador, Otay; General es prueba de estrés visual. Si colisionan etiquetas, usar escala/cajetines/tablas auxiliares en misma lámina sin suprimir el requisito; bloquear FINAL si imposible.
6. Si CAD GUI es inaccesible, ejecutar validación estática/integradora con parser de SCR + fixtures y registrar lista de pasos manuales exactos, **sin afirmar que AutoCAD ha ejecutado el archivo**.

**Commit:** `feat(cp04): compila dos SCR y rutas confirmadas`.

## Fase 6 — Experiencia operativa, batch, CI, rendimiento y cierre

1. CLI individual y `--batch` de cuatro auditorías, secuencia y salidas independientes, resumen de estados por CP/entidad.
2. Workflows GitHub Actions: lint/compile, unit/integration fixtures sin históricos, matrices Python permitidas, prueba de contratos y seguridad de archivos, comparador de oráculo v1; pruebas históricas/CAD etiquetadas locales no ejecutadas en CI pública.
3. Añadir benchmark de memoria RSS/tiempo/IO para XLSX con millones de filas XML + miles de componentes; documentar baseline, sin SLA numérico inventado.
4. Revisar gitignore/paths para evitar exponer datos en GitHub público, verificar permiso antes de agregar DWG/DWT canónicos.
5. Crear checklist por auditoría, logs, hashes, lista de capturas y pasos de DWG/PDF A1. Registrar PENDIENTE_EVIDENCIA donde falten controles o aprobación.
6. Solicitar/proponer protección de `main` (PR + checks requeridos + revisión) si la API permite administración. Si no, entregar instrucciones de configuración manual; no afirmar protección creada.
7. Correr suite completa, casos locales con fuentes ignoradas, verificadores, y revisar diffs. Commits por fase, PUSH a la misma rama autorizado; preparar PR a `main` si existe acceso, SIN merge.

**Commit:** `chore(ci): completa validaciones y entrega E2E`.

## Dependencias y autonomía

| Componente | Puede ejecutarse sin WCS real | Sin KMZ | Sin AutoCAD GUI | Condición FINAL |
|---|---|---|---|---|
| CSV00/01 con geofence aprobada | Sí | Sí | Sí | incidencias/ámbito aprobados |
| CSV02 productivo | **No** | Sí | Sí (si hay controles externos acreditados) | WCS↔WGS84 válido |
| Importador KMZ y pruebas sintéticas | Sí | Sí | Sí | relaciones/casos reales aportados |
| Aristas confirmadas reales | Sí | No, salvo otra evidencia | Sí | validación owner |
| Compilador SCR01/02 | Sí para código/pruebas estáticas | Sí, modo solo-puntos | Sí para offline | AutoCAD probado sobre DWT |
| DWG/PDF final | No | Según rutas requeridas | **No** | owner valida |

## Control Git y entregas

Antes de cada commit: `git status`, stage por ruta explícita, `git diff --cached --stat` y `git diff --cached --check`, escaneo de archivos XLSX/KMZ/XLS/DWG privados, tests pertinentes. No `git add .` en raíz; no reset/clean ni borrar originales. Reportar SHA y salida de pruebas. Push permitido en rama actual; PR borrador si es posible, sin reescritura de commits y SIN merge. Si hay cambios previos ajenos, conservar y aislar.
