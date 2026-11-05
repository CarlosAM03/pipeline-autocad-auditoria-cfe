# Extensión CP-01 — contrato técnico PROPUESTA P-09

Estado: **IMPLEMENTADO Y VERIFICADO**, versión Python 0.2.0. Autorizado el artefacto adicional `00_elementos_unificados.csv`, sin modificar ADR ni TO-BE. El esquema sigue siendo PROPUESTA P-09.

Usa los mismos grupos ya identificados por `dedup.consolidate`, antes del filtro de admisión de 01. No ejecuta un segundo ETL. Una fila por prevalente con `elemento_id`; inválidos, exclusiones y casos sin identidad permanecen en los reportes existentes. La unificación no implica aprobación geográfica ni CAD.

Compatibilidad **verificada**: mismos bytes de 01, 02 cuando existe, summary, linaje, incidencias, asociaciones, perfiles, diagnósticos y topología para iguales entradas/configuración. Conteos y manifiestos se amplían de forma aditiva. P-03 y P-06 no bloquean CP-01.

## Contrato adicional `PROPUESTA-P09-unificados-v1`

Ruta: `AuditoriaCFE/auditorias/<auditoria>/salida/00_elementos_unificados.csv`. UTF-8 sin BOM, coma, CRLF y escape CSV estándar. Encabezado propuesto implementado:

```csv
elemento_id,ruta_prevalente,tipo,coordenada_original,coordenada_interpretada,estado_preparacion,admision_geografica,apto_csv_01,archivo_prevalente,hoja_prevalente,fila_prevalente,ocurrencias
```

| Campo | Definición |
|---|---|
| elemento_id | Mismo ID determinista `identidad-v1` del grupo en linaje/summary; no cambia por incorporar esta vista ni por habilitar P-03. Incluye auditoría, tipo, valores decimales exactos y distinción de equipos acreditados cuando procede. |
| ruta_prevalente | Subruta literal de la primera fuente/hoja/fila declarada; rutas adicionales permanecen en asociaciones, sin repetir fila física. |
| tipo | POSTE, CAJA_EMP o EXCEDENTE. |
| coordenada_original | Texto literal de la ocurrencia prevalente, incluso No detectado si fue recuperada inequívocamente. |
| coordenada_interpretada | Interpretación ya obtenida por el ETL; escala del prevalente, sin redondeo de identidad. Recuperaciones se explican en linaje/incidencias. |
| estado_preparacion | **IDENTIFICADO**, no VALIDO ni aprobación CAD. |
| admision_geografica | PENDIENTE_P03 cuando no existe área acreditada; REVISAR_FUERA_AMBITO para remoto bajo área configurada; ADMITIDO_P03 si superó las condiciones actuales; REVISAR como resguardo para otros estados. Describe el control existente, no acredita el mapa CAD. |
| apto_csv_01 | SI solo si pertenece al conjunto de únicos que el ETL actual admite en 01; NO en otro caso. Nunca habilita 02/CRS ni confirma topología. |
| archivo_prevalente, hoja_prevalente, fila_prevalente | Origen exacto de la ocurrencia prevalente, fila Excel desde1; archivo relativo a la entrada declarada. |
| ocurrencias | Total de ocurrencias del grupo: prevalente+duplicados, independientemente de cuántas rutas lo comparten. |

No se replican fórmulas, celdas completas, todas las rutas ni comparaciones en 00. Permanecen en los reportes existentes. **00 contiene solo grupos identificados**, no una fila artificial por rechazo: casos imposibles, tipo desconocido, ruta vacía, caché primario no acreditado, hemisferio fuera del contrato actual, conflicto de IDs y ocurrencia sin ID ante varios equipos siguen trazados sin inventarles clave física. Un estado REVISAR puede pertenecer a un grupo identificable por falta de P-03, o carecer de identidad por ambigüedad: se distinguen en conteos.

## Flujo y compatibilidad

```text
XLSX declarados → schemas/extract → quality/interpretación existente
    → dedup.consolidate (sin cambio de sus reglas)
        → identified_groups: prevalentes identificados → CSV 00 (CP-01)
        → únicos actualmente admitidos por P-03       → CSV 01 (CP-02)
            → controles CRS P-06                    → CSV 02 (CP-02, condicionado)
```

La evaluación geográfica existente sigue marcando la ocurrencia antes de reportar. La nueva vista se selecciona por identidad, **sin exigir que esa evaluación esté aprobada**. No se construye un segundo ETL ni se cambia el orden de autoridad de fuentes. `identified_groups()` es una vista sin mutaciones con comprobación de prevalente único, referencias y coordenadas coherentes. `consolidate()` mantiene íntegro su comportamiento de 7baa82c.

Identidad: tipo y lat/lon decimales exactamente iguales; ceros redundantes de escala son equivalentes numéricamente y el texto original prevalente se conserva. Valores próximos distintos permanecen separados, incluso más allá de 28 decimales. Cajas con IDs confiables distintos permanecen separadas con el mismo punto. Registro nunca entra a 00. El maestro se consulta informativamente después de consolidar y no cambia los grupos. No hay filtros de aislados120/500/1000 ni aristas propuestas automáticamente.

P-03 pendiente: el prevalente mantiene REVISAR en linaje, duplicados apuntan a él como antes; en 00 se ve IDENTIFICADO/PENDIENTE_P03/NO. P-03 aprobado en configuración y controles de calidad satisfechos: la misma identidad puede figurar IDENTIFICADO/ADMITIDO_P03/SI. P-06 se evalúa separadamente. Ningún cambio de esos estados valida por sí solo una georreferenciación o recorrido.

## Conteos y manifiesto

Se conserva `resumen_conteos.csv` con encabezado `metrica,valor` y todas sus métricas previas, nombres y valores. Se añaden:

- `grupos_pendientes_revision`: prevalentes identificados con estado REVISAR; cada grupo se cuenta una vez.
- `ocurrencias_revision_sin_identidad`: REVISAR no pertenecientes a ningún grupo; no se confunden con los anteriores.
- `ocurrencias_con_identidad`: prevalentes identificados+sus duplicados.
- `filas_csv_00`, `filas_csv_01`, `filas_csv_02`: filas de datos, sin encabezado.
- `csv_02_generado`:1 si existe02,0 si no. Así0 filas no se confunde con archivo no generado.

Invariantes comprobadas en cada lote:

```text
grupos = únicos admitidos + grupos pendientes de revisión
ocurrencias con identidad = grupos + duplicados
ocurrencias originales = grupos + duplicados + revisión sin identidad + rechazados + fuera de alcance
filas00 = grupos; filas01 = únicos admitidos; si existe02: filas02 = filas01
SUM(ocurrencias de 00) = ocurrencias con identidad
```

00 entra automáticamente al inventario de artefactos, hash/tamaño, publicación por lote y `--verificar-salida`. Manifiesto mantiene campos previos y añade `contrato_unificado` y el estado de CP-01..CP-04. Cambian versión del programa, hashes de código/configuración de ejecución y hash de conteos; no se espera el mismo ID de ejecución que 0.1.0. Los IDs físicos se conservan. No se cambiaron encabezados de01/02/summary/linaje/incidencias/asociaciones/topología ni rutas de manifiestos.

## Resultados de integración ejecutada

| Corrida | Ocurrencias | Grupos/filas00 | Duplicados | Pendientes identificados | Revisión sin identidad | Rechazos | Fuera alcance | Filas01 | Filas02 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Prueba-Historica-Mirador (incluye copia) | 732 | **494** | 236 | 494 | 0 | 2 | 0 | 0 | no generado |
| Prueba-Historica-Otay | 969 | **749** | 217 | 749 | 0 | 2 | 1 | 0 | no generado |
| Demo-Sintetica existente | 8 | **5** | 1 | 1 | 0 | 1 | 1 | **4** | **4** |

Los grupos coinciden exactamente con los reportados anteriormente; cambia su visibilidad mediante00. El Mirador de regresión sin copia tiene 551 registros y494 grupos; agregar la copia añade 180 duplicados interpretables y 1 rechazo, no agrega grupos. Los533/965 POINT históricos incluyen duplicados y filtros incompatibles con las reglas actuales; su diferencia se explica en AUDITORIA_JS_HISTORICOS.md.

Se verificaron dos corridas consecutivas por auditoría, todos los bytes y hashes, y se compararon los artefactos previos contra snapshot tomado antes de modificar código. Todos los artefactos antiguos salvo conteos mantienen hash/tamaño exacto; todas las métricas antiguas conservan sus valores. La demo existente se reusó sin regenerar su XLSX ni evidencia. No se modificaron configuraciones ni recursos de las tres auditorías.

## Pruebas de aceptación ejecutadas

43 pruebas OK: se conservan intactos los 29 métodos previos; se agregan9 de unificación y5 de auditoría JS. Los tests nuevos cubren 00 sin P-03/P-06, cuatro familias con precedencia, subrutas compartidas, precisión exacta, cajas con IDs diferentes, casos sin identidad, remotos, aislados, estados sin promoción, conteos, hashes y reproducibilidad. Un oráculo carga el reporting.py real de 7baa82c en memoria y compara bytes de sus productos con el actual, con/sin 02; permite solo métricas nuevas de conteos y el artefacto adicional00.

Comandos reproducibles (Node requerido solo para auditoría JS):

```powershell
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe AuditoriaCFE/tests/validar_extension_local.py
# --comparar-anterior exige el snapshot local extension_antes.json, no versionado.
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe AuditoriaCFE/tests/validar_extension_local.py --comparar-anterior
```

La reproducción de integración actualiza exclusivamente tres lotes de prueba declarados, verifica su integridad previa y nunca busca raíces alternativas. Si faltan fuentes/salidas, falla explícitamente. Pendientes P-01..P-11 no se cierran por estos tests; el nuevo CP-01 es útil aun cuando CP-02 real siga bloqueado.
