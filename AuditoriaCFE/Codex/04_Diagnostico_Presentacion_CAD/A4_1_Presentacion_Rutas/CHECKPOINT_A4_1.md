# Checkpoint A4.1 — revisión de los tres planos prioritarios

**TECNICAMENTE_COMPLETA_PENDIENTE_APROBACION.** Los tres DWG de trabajo y los tres PDF A1 están disponibles localmente. La geometría usa el CRS candidato, con rótulo DIAGNOSTICO_NO_VERIFICADO. Los tres planos permanecen PRELIMINARES. La validación de aceptación y el inicio de A4.2 requieren autorización expresa del responsable.

| Auditoría | Identidades en Model | Hojas A1 | Etiquetas primarias | Colisiones AABB entre textos | Recortes de etiqueta |
|---|---:|---:|---:|---:|---:|
| Natura | 438 | 16 | 438 | 0 | 0 |
| Mirador | 493 | 18 | 493 | 0 | 0 |
| Otay–Florido | 749 | 16 | 749 | 0 | 0 |

La entrega usa los lotes privados de cada auditoría bajo `salida/resultados_cad/A4_1_r5/<auditoria>/`. Dentro del lote se encuentran entrada, configuración y salida con los dos SCR, dos XLSX, contratos CSV/JSONL, índice, plan de hojas y manifiesto. El DWG y PDF consolidados están en `salida/resultados_cad/` del lote, y sus hashes, trazados originales por hoja, extracción nativa y recortes en `evidencia/`. El acta nativa JSON enlaza los hashes del DWG y PDF a la ejecución ETL y pasó la verificación independiente del paquete. Las rondas anteriores conservan sus propios lotes para contraste.

La transferencia privada es `AuditoriaCFE/tests/_runtime/a4_1/A4_1_REVISION_PRIVADA_R5.zip`, 8 370 977 bytes, SHA-256 f17ea0162cfab9ab44dbac4d203c8e9fdad4b11ed9f2e24a3d0a11183b1dd226. Se verificaron CRC y SHA-256 de todas sus entradas enumeradas. Contiene vistas generales y detalles representativos auténticos, recortes y métricas. Los tres PDF completos permanecen en sus lotes.

Puntos de revisión humana. Contraste, tamaño físico A1 y lectura de líderes en las zonas densas. En Otay–Florido el extremo amplía la general y reduce el mapa urbano, conservado a escala útil en los detalles. Revisar las 18 posiciones con tipos coincidentes mediante simbología e índice. Revisar el EXCEDENTE esquemático frente a la leyenda heredada. P-03, P-06 y topología siguen siendo gates independientes. Las tres fuentes históricas para A4.2 están comprobadas por SHA, y el marco constructivo queda pendiente.

Continuidad. Partida ebe2d861464d91ea8d04c8363eaac8b71bfe81e5 en codex/etl-unificado-auditoria-js. Código base A4.1 publicado en edbc7131d9f9297c202a504a2f38a5742ef770ef. El commit que contiene este checkpoint incorpora la última corrección de referencias en la general y los resultados sanitizados. Solo se versionaron código, pruebas y documentos permitidos. El PR #1 conserva su estado abierto.

- [Acta y custodia](ACTA_A4_1.md)
- [Resultados nativos y contraste](RESULTADOS_NATIVOS.md)
- [Pruebas y regresiones](PRUEBAS_Y_REGRESIONES.md)
- [Operación y regeneración](INSTRUCCIONES_OPERADOR.md)
- [Pendientes de aprobación](PENDIENTES_APROBACION_OWNER.md)
