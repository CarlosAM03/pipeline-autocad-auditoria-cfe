# PROPUESTA documental — checkpoints y corrección de atribución JS

Estado: PROPUESTA para revisión del responsable. No sustituye ni modifica ADR-000 ni TO-BE v0.2. La implementación de CP-01 está expresamente autorizada por el encargo vigente.

| Checkpoint | Resultado | Estado de esta entrega | Precondiciones propias |
|---|---|---|---|
| CP-01 Unificación/deduplicación | 00_elementos_unificados.csv | Implementado y probado | Fuentes/hojas declaradas, interpretación e identidad; no requiere aprobación P-03/P-06. |
| CP-02 Normalización/preparación cartográfica | 01_elementos_normalizados.csv y auxiliar obligatorio02_elementos_proyectados.csv | Conservado y probado; validación real parcial/bloqueada |01 exige admisión vigente P-03;02 exige además evidencia CRS/controles P-06. Auxiliar obligatorio no autoriza generarlo falsamente cuando falta evidencia. |
| CP-03 Configuración AutoCAD | 01_configurar_plano.scr | No implementado, futuro | Plantilla/mapa/marco y perfil CAD verificados. |
| CP-04 Construcción AutoCAD | 02_dibujar_auditoria.scr | No implementado, futuro | Puntos admitidos/proyectados, topología confirmada para líneas, símbolos/etiquetas y presentación aprobados. |

Los checkpoints son controles de productos dentro de los dos procesos arquitectónicos del ADR. No crean cuatro procesos ni eliminan linaje, summary, incidencias, conteos, manifiestos o autoridad humana de conexiones. No se cambia el alcance actual a producción SCR/CAD.

Corrección propuesta para la fila TO-BE v0.2:260: atribuir el retorno al padre a **ordenar.js:184**, que serializa ida/vuelta del árbol en una PLINE, y describir **trayectoria.js:157–176** como preorden sin retorno que puede unir hojas de ramas sin arista. Conservar la prohibición de derivar conexiones físicas del DFS/proximidad. Evidencia ejecutada y hashes en AUDITORIA_JS_HISTORICOS.md; fixture `{0–1,1–2,1–3}` produce respectivamente `[0,1,2,1,3,1,0]` y `[0,1,2,3]`.

Decisión solicitada al responsable: aprobar o ajustar esta redacción y el contrato adicional PROPUESTA-P09-unificados-v1 antes de actualizar documentación normativa en un cambio posterior. No es necesario resolver esa enmienda para utilizar el CSV 00 como preparación no aprobada para CAD.
