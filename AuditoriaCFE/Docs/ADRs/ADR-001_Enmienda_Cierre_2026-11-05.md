# ADR-001 — Enmienda de alcance y decisiones para automatización integral CFE/DATRA

| Campo | Valor |
|---|---|
| Estado | **Aceptado como autorización de implementación** sobre Q01–Q75; verificaciones físicas explícitamente condicionadas |
| Fecha | 2026-11-05 |
| Línea base de código | `f3060742e9a2ce90d186802ab3de5a4ccd968633` |
| Autoridad | Respuestas documentadas en `AuditoriaCFE/Codex/02_Harness_Integral/00_RESPUESTAS_ORIGINALES.md` |
| Antecesor | `ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md` (conservar sin reescribir) |

## 1. Decisión de ejecución

Se autoriza a Codex a **terminar el pipeline completo** en la rama existente `codex/etl-unificado-auditoria-js`, con commits por checkpoint, pruebas offline y, si el entorno lo permite, ensayos de AutoCAD 2026 en copias. Puede generar archivos bajo `AuditoriaCFE/recursos/` y `auditorias/*/salida/`, pero jamás alterar los históricos ni aceptar por cuenta propia un control geográfico, conexión física, permiso de publicación o acta FINAL.

Los dos procesos arquitectónicos del ADR-000 se conservan; CP-01–CP-04 son hitos de evidencia y productos, no cuatro procesos autónomos. Dos scripts operativos siguen siendo obligatorios: `01_configurar_plano.scr`, `02_dibujar_auditoria.scr`.

## 2. Extensiones acordadas

- Cuatro auditorías obligatorias: Natura, Mirador, Otay–Florido, Tijuana-General. Bomberos queda posterior y separado.
- ETL conserva `00_elementos_unificados.csv`, genera bandeja adicional `00_elementos_revision.csv` (con contrato nuevo) y no cambia silenciosamente el archivo 01 mínimo.
- Variantes tipográficas de nombres de elementos en XLSX se normalizan a tres clases canónicas cuando el mapeo es inequívoco. Tipos ambiguos requieren revisión.
- Se habilita archivo versionado **por contrato** para resoluciones documentadas de incidencias, sin editar XLSX originales.
- Se soporta área por auditoría/corredor con archivo espacial y revisión individual de excepciones.
- Proyección productiva mantiene controles CAD verificables; el modo CRS candidato, si se implementa, es únicamente diagnóstico no publicable.
- La referencia de trabajo CAD es `AuditoriaCFE/recursos/PlantillaMarcoDatraMapaTijuana.dwg`; `146468_PLANOTIJUANA.dwg` es donador/referencia original; Mirador se usa para comparar las convenciones históricas UTM84-11N, metros y desviaciones, sin offset automático.
- La plantilla final DWT se obtiene **una sola vez** desde recursos DATRA probados, preferiblemente cartografía embebida. Después cada auditoría utiliza copias del DWG base, dos SCR, revisión, DWG y PDF A1.
- El KMZ completo se investiga como fuente de topología **candidata**; aristas confirmadas exigen evidencia y aprobación humana. Si no existen, el SCR de dibujo puede representar solo puntos PRELIMINAR.
- El grafo admite ciclos, postes compartidos, ramificaciones y componentes desconectados; hay tres anillos de redundancia declarados por usuario, no confirmados todavía por aristas inspeccionadas.
- Las rutas se pueden proponer por proximidad/KMZ pero **no confirmar** por algoritmo. La troncal con más postes es un diagnóstico, no regla que reescribe una topología aprobada.
- Se aceptan bloques CAD por tipo, etiquetas P/C/E con numeración estable, coordenadas geográficas de origen, distancias planas en aristas confirmadas y leyenda/cajetín DATRA editables.
- Se añaden CI GitHub Actions, pruebas de rendimiento, `--batch`, checklists de entrega y política de PR listo sin merge automático.

## 3. Enmiendas y aclaraciones al ADR-000

**A05/P-01:** la ausencia de orden físico de postes no modifica la necesidad de un criterio determinista para prevalencia entre archivos. Se separan explícitamente ambas nociones.

**P-02:** el DWG base no se considera baseline de novedad de inventario. Si no hay inventario histórico datado, `NO_DETERMINADO`.

**P-03:** el área geográfica se amplía conceptualmente para admitir polígonos y corredores con evidencia; un rectángulo diagnóstico no se declara autoridad sobre cobertura local.

**P-04:** la eliminación de coordenadas defectuosas significa excluirlas de geometría final y registrar motivo, sin borrado de linaje.

**P-06:** queda autorizado el estudio de un CRS candidato en copias de prueba. El estado de salida **no puede ser VALIDADO ni FINAL** sin controles reales WCS/WGS84 acordes a tolerancia documentada.

**P-09:** ratificar contrato existente CSV 00 de 12 columnas y 01 mínimo; proponer nuevo contrato 02 con `ruta_id` verdadero más nombre legible y compatibilidad; agregar 00 revisión. Manifiestos y artefactos **operativos** deben residir en `salida/` al completar la migración, con publicación por lote y verificador actualizado.

**P-10:** AutoCAD 2026 inglés confirmado. Se permite LISP como dependencia de los **dos** SCR, empaquetado e invocado sin tercer paso manual.

**C06/P-07:** detalles técnicos recuperados de los recursos aplicables. Si faltan, se permiten **prototipos esquemáticos** del mismo estilo para revisión; no afirmar herrajes o parámetros reales sin evidencia y aprobación.

**C01/C04/P-08:** una sola A1 con etiquetas exigidas; legibilidad imposible provoca incidencia y propuesta formal de excepción, nunca páginas adicionales automáticas.

**Custodia:** los productos y manifiestos persistentes residen en salida; los documentos del agente en Codex; el resto de rutas oficiales mantienen sus excepciones explícitas. Las configuraciones reales con datos sensibles no se publican solo por existir una plantilla rastreada.

## 4. Reglas NO derogadas

Permanecen inmutables: dos procesos, dos SCR, AutoCAD convencional sin Map 3D, XML streaming, no fotos, no heurísticas geográficas como autoridad, dedup exacta sin pérdida de linaje, Registro fuera de alcance, referencias maestras informativas, una A1, revisión DWG/PDF humana, históricos inmutables.

## 5. Incompatibilidades que la implementación debe migrar

- `AGENTS.md` anterior prohíbe SCR/recursos; este ADR autoriza actualizarlo.
- `topologia_propuesta.csv` actual vacío: generador de sugerencias futuro requiere contrato explícito y no puede producir confirmadas sin aprobación.
- `config.py` actual solo acepta geografía rectangular; incorporar archivos espaciales y migra configs de prueba sin romperlas.
- `reporting.py` actual publica manifiestos fuera de `salida/`: migrar esquema y verificador de forma recuperable, sin perder corridas antiguas.
- TO-BE v0.2 atribuye retorno DFS al script equivocado; v0.3 documenta: `ordenar.js` retorna, `trayectoria.js` no retorna.

## 6. Aprobación por evidencia

El usuario es aprobador del pipeline. Se aceptan decisiones técnicas en este ADR; quedan **pendientes de medición** controles WCS, tolerancia geodésica, KMZ real, geometría/troncales confirmadas, prueba AutoCAD y licencia de publicación. Codex debe continuar los trabajos independientes y no falsear estos gates.
