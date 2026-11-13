# Checkpoint A4.2 — candidata DATRA/CFE A1

**Técnicamente verificada, pendiente de aprobación.** La propuesta v1.0.0 incorpora cuatro bloques históricos editables. Derivación D03 queda explícitamente pendiente. Se preservó el quinto diagrama de cambio de dirección como referencia independiente, sin atribuirle otra función.

- DWG maestro privado en `AuditoriaCFE/tests/_runtime/a4_2/entrega_v2/Plantilla_DATRA_CFE_A1_v1_0_0.dwg`, SHA-256 `62abf37880f95c0e895cfa0f6e3ef95fb7e620e4560586fc38cc72eda3901728`.
- DWT métrica generada mediante SAVEAS y reabierta en Core Console, junto al DWG. SHA-256 `51eb05563b77925276b94e5a1c8e92701869369452ebc839a5a98b684933748c`.
- Lotes privados en `AuditoriaCFE/auditorias/_a4_2/<auditoria>/salida/`. DWG, PDF, capturas y logs en `resultados_cad/`. Cada lote se reconstruyó con los dos SCR y el default de 300 m.
- Los tres perfiles conservan 438/472/741 elementos representados, 0/21/8 excluidos de la vista y 16/10/12 hojas. El índice, el plan de páginas y los datos canónicos coinciden con los lotes aprobados. El CSV de exclusiones conserva el encabezado previo y las 29 identidades con procedencia, coordenadas y motivos.
- Las 38 comparaciones de las zonas de mapa y cajetín coincidieron píxel a píxel a 50 dpi. La columna lateral cambió en las 38. Se conservan los recortes de cada panel, incluido el aviso de derivación. Esta verificación complementa la inspección de XDATA, coordenadas y el ensayo de reapertura.
- ZIP de revisión externa sanitizado bajo `AuditoriaCFE/tests/_runtime/a4_2/entrega_v2/A4_2_REVISION_EXTERNA.zip`. Las capturas de los detalles y los planos completos quedan locales por custodia.

El responsable debe validar las especificaciones históricas, la propuesta de plantilla y la legibilidad en papel. Las auditorías siguen PRELIMINARES y permanecen pendientes P-03/P-05/P-06. El PR #1 queda abierto.

[Acta](ACTA_A4_2.md) · [Matriz de componentes](MATRIZ_COMPONENTES_CFE.csv) · [Pruebas](RESULTADOS_PRUEBAS_CAD.md) · [Procedimiento](PROCEDIMIENTO_OPERADOR_V1.md) · [Pendientes](PENDIENTES_APROBACION_OWNER.md)
