# Fase 6 — Integración operativa y checkpoint revisable

Fecha: 2026-11-05. Software integral v0.3.0. Lotes reales: **PRELIMINAR**, no ACEPTADO_HUMANO.

## Pruebas ejecutadas

- Suite local: **79 ejecutadas, 79 aprobadas, 0 fallidas, 0 omitidas**, 66.953 s; contiene las 43 anteriores, incluido oráculo portable, regresiones XLSX reales y cinco pruebas JS sobre copias aisladas.
- Compilación `compileall`, lint Ruff E9/F821/F822/F823, `pip check` y custodia/oráculo: OK.
- Primera suite de integración: 77 casos, un fallo de recuperación legacy al añadir carpeta de fallos al lote antiguo. Corregido: durante migración fallida se conserva la ubicación de fallos de la autoridad anterior; seis pruebas CP02 repetidas OK y suite final 79/79 OK.
- Ensayo individual Natura y demo sintética ejecutados. Demo conserva cuatro filas admitidas en 01 y cuatro proyectadas v1, controles analíticos de fixture; no acredita cartografía real.
- Batch diagnóstico de cuatro auditorías ejecutado, verificación de integridad completa y repetición con los mismos IDs de ejecución: `BATCH_REPRODUCIBLE True`. Ningún CSV02 productivo real emitido.
- Benchmark final: 1,000,000 filas XML físicas, 10,000 componentes, XLSX 2,758,911 bytes; pipeline + verificación 9.871 s, CPU 9.344 s, RSS pico del proceso 88,862,720 bytes; lectura OS lógica 113,113,011 bytes, escritura 26,479,694. Primera medición 7.387 s/88,285,184 bytes; variación de carga del equipo, sin SLA inventado. Python 3.10.11, Windows 10.0.26300.

Comandos y logs técnicos: `tests/_runtime/fase6_cierre.log`, `benchmark_final.log`, `batch_real_final.log`, `batch_integridad.log`, `repro_batch.log` (locales ignorados). Código de benchmark y verificador se versionan, logs privados no.

## Corridas locales reales

| Auditoría | Ocurrencias | Grupos/00 | Duplicados | Rechazados | Fuera alcance | Filas 01 | Filas 02 productivo | Puntos diagnóstico |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Natura | 507 | 438 | 69 | 0 | 0 | 0 | 0 | 438 |
| Mirador | 732 | 493 | 236 | 3 | 0 | 0 | 0 | 493 |
| Otay-Florido | 969 | 747 | 216 | 5 | 1 | 0 | 0 | 747 |
| Tijuana-General | 4341 | 4131 | 190 | 20 | 0 | 0 | 0 | 4131 |

Tipos 00: Natura 438 POSTE; Mirador 414 POSTE, 20 CAJA_EMP, 59 EXCEDENTE; Otay 584 POSTE, 17 CAJA_EMP, 146 EXCEDENTE; General 4131 POSTE. Todas las cifras concilian por auditoría. 01 contiene solamente encabezado porque no hay perímetro aprobado; 02 validado **no existe**. El diagnóstico tiene archivo diferente y rótulo obligatorio.

Mirador previo 494 corresponde al control STD+Canal (551 ocurrencias). Ahora se añade copia (181 ocurrencias) y tres exclusiones Q24 acreditadas por hash/fila; quedan 493 grupos, 236 duplicados y tres rechazos. Otay previo 749/217 duplicados/dos rechazos pasa a 747/216/cinco con las exclusiones Q24, sin forzar los totales anteriores. No se borran fuentes ni linaje. Natura y General no se comparan con 533/965: esos son conteos TXT históricos de otros conjuntos, no únicos bajo las reglas actuales.

KMZ exacto autorizado leído desde copia: 8087 geometrías, 7839 puntos, 235 líneas, 13 geometrías inválidas conservadas como incidencias; 11 tokens de coordenada imposibles en origen. Propuestas por auditoría: 333/213/533/3353 respectivamente; todas NO_CONFIRMADAS. No se generó topología humana ni se dibujaron los tres anillos por declaración.

## Estado de checkpoints

| CP | Ingeniería | Gate de datos/aceptación |
|---|---|---|
| CP-01 | COMPLETADO_TECNICO, real/sintético probado | Revisión de incidencias por owner; P-09 ratificado |
| CP-02 | COMPLETADO_TECNICO, v1/v2 y geofence probados | PENDIENTE_EVIDENCIA P-03/P-06 reales |
| CP-03 | Compilador y runtime implementados, configuración nativa ensayada | Plantilla/DWT, dependencias y presentación requieren aceptación |
| CP-04 | Compilado/estático probado, sólo puntos diagnósticos reales | Ejecución nativa definitiva y revisión A1 pendientes al registrar esta fase |

Cada salida real contiene acta/checklist, reportes topología/CAD/papel, manifiesto canónico e historial. Los resultados CAD mutables y fallos se preservan fuera de la lista de artefactos inmutables. El verificador de consumo detecta cambios de entradas/configuración, mientras la preparación permite publicar un lote nuevo tras verificar los artefactos anteriores.

## Custodia y Git

Se mantiene la rama autorizada. Commits de fases 0–5: 1706ca0, 176355d, e46a883, b5a6201, f09cb55, bb456b6. No se reescribieron f306074/b3b303a/e4d4e9c ni checkpoints anteriores. README_ENTREGA_Y_PASOS.md ya estaba restaurado exactamente; se preservó. ADR-000 y TO-BE v0.2 intactos.

Se conservaron sin incluir tres archivos previos del paquete del owner: `.gitignore`, `05_PROMPT_MAESTRO_CODEX.txt`, `06_INVENTARIO_PAQUETE.json` dentro de Harness. Transcripción original ignorada. No se versionan entradas, salidas, resoluciones/topología reales, DWG/DWT ni KMZ. El PDF de referencia heredado se permite en el verificador exclusivamente con su hash original; esto no otorga licencia para publicar binarios nuevos.

CI pública propuesta: Windows/Linux × Python 3.10/3.12, checkout superficial, compilación/lint/custodia/suite/benchmark pequeño. Sin fuentes privadas se esperan nueve omisiones históricas explícitas; el estado remoto/PR/protección y último ensayo nativo se anexarán en el cierre sin fingir que ya se ejecutaron.

## Gates residuales

P-03 perímetros y excepciones; P-06 dos controles reales y metros/tolerancia; P-05 aristas confirmadas; P-07 recursos/detalles/plantilla aplicables; P-08 legibilidad A1, especialmente General; P-04 aceptación humana; P-11 conciliado con definiciones históricas. Baseline P-02 opcional ausente => NO_DETERMINADO. P-01 precedencia, P-09 contratos y P-10 perfil AutoCAD quedaron definidos, no se vuelven a consultar.

Se añadió prueba de fallo de validación posterior a publicar: revierte al lote anterior antes de eliminar su copia. Última suite de 79 casos, sin fallos/omisiones. El viewport usa comandos MVIEW/ZOOM, porque Autodesk prohíbe entmake/entmod en VIEWPORT ([referencia oficial](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-AutoLISP-Reference/files/GUID-D47983BA-1E5D-417D-85B8-6F3DE5F506BA.htm)).
