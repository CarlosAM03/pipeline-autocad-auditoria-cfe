# Resultado de implementación — Proceso 1

## Extensión vigente desde 7baa82c — CSV 00 y auditoría JS

**Versión 0.2.0 implementada y verificada.** El registro de la primera implementación se conserva debajo como antecedente. Este encargo sí autoriza un commit local específico; no autoriza push, PR ni generación CAD. Rama de trabajo: `codex/etl-unificado-auditoria-js`.

Cambios de código limitados a `dedup.py` (vista de prevalentes identificados, sin modificar consolidate), `reporting.py` (CSV 00 y conteos aditivos), `pipeline.py` (manifiesto/estados CP-01..CP-04) y versión del paquete. Los extractores, quality, comparación y proyección mantienen sus reglas. CSV 00 usa `IDENTIFICADO` como preparación y expresa admisión geográfica separadamente; nunca es autorización CAD.

Entregas nuevas: `AUDITORIA_JS_HISTORICOS.md`, `EXTENSION_ETL_UNIFICADO.md` y `PROPUESTA_CHECKPOINTS_CP01_CP04.md`. Se actualizan este resultado, pruebas, pendientes, checklist y README. Pruebas nuevas: `test_unificados.py`, `test_js_historicos.py`; herramientas de prueba: `js_audit_harness.cjs`, `audit_js_support.py`, `validar_extension_local.py`. `.gitignore` local excluye el entorno `.venv-cp01` sin modificar el `.venv` preexistente inaccesible. No cambian las configuraciones de las auditorías ni recursos CAD.

Resultados ejecutados: **43 pruebas OK, 0 fallos y 0 omisiones**, incluidas las 29 originales sin editar. CSV 00: **Mirador 494, Otay 749, demo 5 grupos**. CSV 01 y 02 reales mantienen sus bloqueos; demo conserva 4/4. Comparación byte a byte contra productos anteriores: artefactos previos idénticos salvo conteos ampliados; métricas antiguas idénticas. Dos corridas consecutivas de cada lote y manifiesto activo verificadas.

Auditoría JS ejecutada en copias: los 533/965 POINT se reconstruyen exactamente en secuencia; se documentan filtros, duplicados y errores de fórmula. Se confirmó que ordenar agrega padre al retorno y trayectoria hace preorden sin él, corrigiendo la atribución mediante propuesta separada, sin editar TO-BE. Ninguna reproducción genera SCR.

CP-01 completado sin P-03/P-06; CP-02 conservado y condicionado; CP-03/CP-04 no implementados. Continúan P-01 productivo, P-02 opcional, P-03/P-04/P-06 para admisión/liberación y P-05/P-07/P-08/P-10 para CAD; P-09 requiere revisar contrato de 00 y propuestas; P-11 no se cierra silenciosamente.

Custodia Git: única entrada previa ajena era `?? README.md` en raíz; se conserva por hash y queda fuera del commit. HEAD inicial 7baa82c y checkpoint 33364c1 no se alteran. Los productos, copias JS y snapshots permanecen ignorados; se hará staging explícito solo de los archivos de la extensión. El commit local de entrega se identifica con `git log -1`; mensaje requerido `feat(etl): agrega CSV unificado y auditoria de scripts historicos`.

Comandos actuales: entorno Python 3.10.11+pyproj 3.6.1/PROJ 9.3.0 en `.venv-cp01`, Node 22.16.0 solo para auditoría. Ver README y PRUEBAS_Y_VALIDACION para comandos completos y evidencia. Siguiente checkpoint: revisar 00/P-09 y la discrepancia documental JS, resolver precondiciones de CP-02 y autorizar por separado CP-03/CP-04. Sin push automático.

## Registro de la primera implementación (anterior a esta extensión)

Fecha: 2026-11-04, America/Tijuana. **Primera implementación funcional terminada y probada; pendiente de aceptación de datos/reglas operativas.** Se detiene antes de Proceso 2/CAD. No se realizaron commits.

Origen verificado: HEAD `33364c1aa2c94a751857c4d106ee826d8af17ac5`; el tag anotado `checkpoint/pre-codex-proceso1^{commit}` resuelve al mismo commit y no fue modificado. Se leyeron AGENTS, ADR-000, TO-BE v0.2, contrato PROPUESTA, encargo, siete entregables del diagnóstico XLSX y checklist. También se contrastó CHECKPOINT_PLANTILLA_BASE_v1: P-06 sigue pendiente, aun existiendo marco visual candidato.

## Implementación entregada

| Archivo o módulo | Comportamiento implementado / estado real |
|---|---|
| `preparar_auditoria.py`, `src/auditoriacfe/cli.py` | Selección interactiva; `--auditoria`, `--dry-run`, `--entrada-prueba` explícita readonly y `--verificar-salida`. Cantidad/lista antes de extracción. Probados. |
| `config.py` | Fuentes completas y orden obligatorio, hojas explícitas cuando múltiples, excepciones de cabecera, perímetro acreditado, referencias, IDs, controles CRS. Config inválida falla con diagnóstico. |
| `source_ooxml.py` | ZIP en lectura, streaming XML con liberación de cada fila; no max_row ni medios. Valores numéricos literales, sharedStrings, inlineString, fórmulas compartidas y cachés sin ejecución, filas ocultas. Límite de sharedStrings XML: 16 MiB; exceso falla explícitamente. |
| `schemas.py` | F1 ABC Nombre; F2 ABC Ruta/Foto D; F3 BCD con Numero A; F4 BCD sin Numero. D vacía en F3 exige excepción configurada. Perfiles de hojas, incluida vacía, y filas exclusivamente auxiliares. |
| `coordinates.py`, `quality.py` | Decimal exacto, formas inequívocas N/W, validación mundial/local, auxiliares consistentes, conservación íntegra del origen. POSTE/EXCEDENTE/CAJA_EMP; Registro FUERA_ALCANCE. Sin perímetro aprobado: REVISAR, sin exportación dibujable. |
| `dedup.py` | Tipo y coordenada exactos sin redondeo; primera ocurrencia por fuentes/hojas/filas declaradas. IDs estables versionados; excepción de cajas con ID/evidencia acreditados. Conflictos y ocurrencias sin ID ante dos equipos quedan en revisión. Mantiene grupos aun pendientes de admisión geográfica. |
| `comparison.py` | Maestro y baseline declarados, separados e informativos, después de consolidación. Baseline ausente: NO_DETERMINADO. Referencia incompleta no demuestra novedad por ausencia. Ningún filtro del plano individual por coincidencia maestra. |
| `projection.py` | pyproj/PROJ con always_xy y errcheck; evidencia archivada, responsable/fecha/unidades/CRS/tolerancia y dos controles diferentes. Residuales verificados. Funciona en fixture; proyección real BLOQUEADA P-06. |
| `topology.py` | Cercanía geodésica optativa con umbral explícito, sin fusión ni conectividad. `topologia_propuesta.csv` vacío con cabecera y razón documentada, permitido por contrato. No se genera topología confirmada. |
| `reporting.py`, `pipeline.py`, `util.py` | CSV/JSONL UTF-8, conteos reconciliados, hashes de fuentes/config/código/productos y versiones. Staging, bloqueo del SO, rollback, recuperación y verificación del manifiesto activo. Destinos con enlaces/alias rechazados para proteger entrada. |
| `tests/support.py`, `test_proceso1.py`, `test_historico.py` | Fixtures generados ligeros, 29 pruebas automatizadas ejecutadas, incluidas nueve fuentes reales readonly y dos CSV históricos. |
| `tests/crear_demo.py` | Demostración sintética revisable, 8 ocurrencias, 4 filas en cada CSV principal, 2 POSTE + 1 CAJA_EMP + 1 EXCEDENTE. Controles exclusivamente sintéticos. |
| `README.md`, `requirements.txt`, `configuracion.ejemplo.json`, `.gitignore` local | Instalación y operación PowerShell, contrato/configuración y exclusión de datos/productos generados de Git. |
| `auditorias/Prueba-Historica-{Mirador,Otay}/configuracion.json` y README | Configuraciones de PRUEBA, con raíces externas obligatoriamente explícitas. No constituyen precedencia de producción aprobada. |
| `auditorias/Demo-Sintetica/configuracion.json`, `CONTROLES_SINTETICOS.txt` | Configuración y evidencia analítica exclusivamente de fixture; no acreditan el mapa de Tijuana. |

## Instalación y ejecución comprobadas

El alias Windows `python` no fue utilizable. Se creó el entorno con el Python de Thonny instalado, sin alterar su instalación global:

```powershell
& 'C:/Users/Carl0/AppData/Local/Programs/Thonny/python.exe' -m venv AuditoriaCFE/.venv
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip install -r AuditoriaCFE/requirements.txt
& ./AuditoriaCFE/.venv/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
& ./AuditoriaCFE/.venv/Scripts/python.exe -m compileall -q AuditoriaCFE/src AuditoriaCFE/tests AuditoriaCFE/preparar_auditoria.py
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip check
```

Entorno ejecutado: Python 3.10.11, pyproj 3.6.1 (incluye PROJ), Windows 64 bits. ETL sin dependencia de Excel/pandas/openpyxl/Pillow. Solo la geodesia requiere pyproj. Primera descarga falló por red del sandbox; se completó con ejecución de instalación autorizada por el revisor automático. `pip check`: sin requisitos rotos. Las versiones efectivas de PROJ se conservan en manifiestos.

```powershell
# Ejemplo de operación con originales colocados por el operador:
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria MiAuditoria --dry-run
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria MiAuditoria
# Demostración ejecutada, íntegramente sintética:
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/tests/crear_demo.py
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Demo-Sintetica --verificar-salida
```

`MiAuditoria` es un ejemplo de uso; no se afirma haber ejecutado esa auditoría inexistente. Los comandos reales de Mirador/Otay y sus resultados están en PRUEBAS_Y_VALIDACION.md.

## Productos generados realmente

Existen salidas locales ignoradas por Git en `AuditoriaCFE/auditorias/{Demo-Sintetica,Prueba-Historica-Mirador,Prueba-Historica-Otay}/salida/`:

- `01_elementos_normalizados.csv`, encabezado exacto `Ruta,Elemento de Red,Coordenadas`.
- `summary.csv`, `linaje_y_calidad.jsonl`, `reporte_incidencias.csv`, `asociaciones_elemento_ruta.csv`, `resumen_conteos.csv`.
- `topologia_propuesta.csv`, solo cabecera; `coordenadas_cercanas.csv`, sin aristas implícitas.
- `perfiles_hojas.jsonl`, `filas_no_operativas.jsonl`, para explicar hojas vacías y valores auxiliares omitidos de la geometría.
- `02_elementos_proyectados.csv` **solo en Demo-Sintetica**, 4 filas, controles de fixture verificados. No se produjo para datos reales.

**Manifiestos fuera de entrada/salida:** `auditorias/<nombre>/manifiesto_ejecucion.json` activo y `manifiestos/<ejecucion_id>.json` archivado. Esta ubicación aplica AGENTS sobre la propuesta de contrato P-09; la discrepancia se eleva a revisión sin modificar ADR/TO-BE. Errores fatales dejan un manifiesto de fallo y conservan la salida previa, cuando la auditoría y los destinos son válidos; dry-run no escribe.

| Corrida de PRUEBA | Ocurrencias | Grupos identificados | Duplicados | REVISAR prevalentes/casos | RECHAZADO | FUERA_ALCANCE | Exportables |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mirador, con copia adicional | 732 | 494 | 236 | 494 | 2 | 0 | 0 |
| Otay–Florido | 969 | 749 | 217 | 749 | 2 | 1 | 0 |
| Demo sintética | 8 | 5 | 1 | 1 | 1 | 1 | 4 |

Los cero exportables históricos son el resultado deliberado de **no aprobar un perímetro pendiente P-03**. Los grupos se deduplican y comparan informativamente, pero permanecen en revisión. La demo demuestra el flujo completo hasta proyección, sin convertir un fixture en evidencia CAD.

Ejemplo real del CSV sintético, sin datos de campo:

```csv
Ruta,Elemento de Red,Coordenadas
"Demo ""A"", tramo 1",POSTE,32.500000N 117.000000W
Ruta,CAJA_EMP,32.500000N 117.000000W
Ruta,EXCEDENTE,32.50001N 117W
Ruta,POSTE,32.50002N 117W
```

La escala decimal original del prevalente se preserva. En el fixture, el primer poste se proyecta a `Este=500000.0, Norte=3595859.113489768`, sin compensación heredada; sus controles no acreditan posición alguna del DWG real.

## Límite de entrega

Código probado y productos revisables; ninguna salida se declara FINAL. P-01 por auditoría, P-03, P-04, P-06 y revisión P-09 siguen condicionando producción/validación. No hay cobertura geográfica/topológica acreditada. No se ejecutó AutoCAD ni se crearon SCR, DWG, DWT o PDF; no se modificaron recursos ni originales. El árbol de recursos sin versionar ya existía al iniciar y se dejó intacto.

Siguiente checkpoint: revisar los tres documentos de cierre y las salidas de demostración, aprobar precedencia/perímetro/contrato, proporcionar controles CAD y resolver incidencias de origen. No iniciar el Proceso 2 sin un nuevo encargo.
