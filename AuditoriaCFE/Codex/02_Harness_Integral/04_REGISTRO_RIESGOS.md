# Registro de riesgos y criterios de escalamiento

| Código | Riesgo o discrepancia | Mitigación para ejecución autónoma | Bloquea |
|---|---|---|---|
| GIT-01 | `README_ENTREGA_Y_PASOS.md` rastreado aparece eliminado localmente; copia en temp ignorado | revisar hash, restaurar o mover con `git mv` preservando historia; no `reset --hard` | commit relacionado hasta resolver |
| GIT-02 | Repo público; `.gitignore` no cubre toda configuración/topología fuera de entrada/salida | preflight de tracked/ignored, escanear stage y PR, no agregar KMZ/XLSX/aristas privadas | push de información sensible |
| GIT-03 | Permisos/licencia de mapa, logo, DWT no acreditados | no publicar nuevos binarios CAD en repositorio público hasta evidencia/permiso | publicación de esos binarios |
| DATA-01 | Q05 desorden de puntos confundido con precedencia de fuentes | precedencia determinista solo identidad; topología siempre separada | ninguna ruta por orden |
| DATA-02 | Q11 pide CSV limpio y revisión sin perder el primer checkpoint | conservar 00 identificables, generar 00 revisión; semántica documentada y contadores | cambio silencioso de contrato |
| DATA-03 | Anomalías 11702014028W, 432N, 2.528N, 177W, 116.48565W | excluir de dibujado, dejar todas incidencias; resolver solo con evidencia | incluir esos puntos |
| DATA-04 | Dos cajas mismo punto sin ID de fuente acreditado | `elemento_id` calculado no prueba dos equipos; evidencia externa | excepción multi-equipo |
| DATA-05 | Geofences/KMZ reales aún no declarados en `entrada/` | pruebas sintéticas y `PENDIENTE_EVIDENCIA`; no inventar zonas | P03 productivo |
| GEO-01 | Base `146468` INSUNITS mm vs Mirador m; DATRA WCS no acreditado | dos controles WCS/WGS84 reales y medición residual; sin escalado ciego | CSV02 productivo y FINAL |
| GEO-02 | Fórmula UTM JS tiene ~+11.5m en Norte a ~32.5N | pyproj y controles; nunca +/−11.5 m | coincidencia real de CAD |
| GEO-03 | Usuario quiere dibujo por defecto aun sin WCS confirmado | solo diagnóstico en copia rotulado no verificado; no confundir con FINAL | aceptación cartográfica |
| TOPO-01 | KMZ descrito pero sin archivo/ruta accesible en inventario | emitir reporte de ausencia; desarrollar importador con fixture; puntos preliminares | rutas confirmadas reales |
| TOPO-02 | Puntos no demuestran aristas; 3 anillos referidos sin mapa de enlaces | fuente/evidencia + confirmación manual; soportar ciclos estructuralmente | rutas finales sin confirmación |
| TOPO-03 | Inicio/final y troncal no acreditados | identificar candidatos, dejar NA; B06 diagnóstico | etiqueta de troncal confirmada |
| CAD-01 | DWT 90% visual no acredita geometría WCS, detalles ni A1 | ensayo AutoCAD sobre copia, reportes y gate | DWT aprobada |
| CAD-02 | Algunos paneles técnicos ausentes en PDF | recuperar originales o producir esquemas provisionales no homologados | FINAL con esos detalles |
| CAD-03 | Puntos/etiquetas General no caben en A1 | múltiples estrategias de viewport/tabla en hoja única; bloqueo y excepción formal | FINAL General |
| CAD-04 | Codex sin control GUI AutoCAD local | tests offline/estáticos + lista manual; no fingir ejecución GUI | certificación CAD, no compilador |
| OPS-01 | Manifiestos actuales fuera de salida y publicación atómica | migración versionada con rollback y test de crash; no autorreferencia de hash | nuevo contrato de ubicación |
| OPS-02 | Test `--batch` se mezcla con fuentes | directorio por auditoría/locks/manifests independientes | CLI batch |
| CI-01 | GitHub Actions no accede a fuentes ignoradas ni AutoCAD | separar CI portable vs integración local/humana, omisiones visibles | afirmar E2E real |
| CI-02 | Protección de ramas requiere permisos admin | intentar API autorizada, si no entregar guía UI concreta | configuración automática de protección |
| PERF-01 | Carga útil crece, RSS sin presupuesto fijo | benchmark baseline con máquina/versión; optimizar sin inventar SLA | no bloquea salvo OOM |

**Política de escalamiento:** los bloqueos de hechos de campo/AutoCAD detienen solo la parte que necesita esa evidencia. Codex debe terminar en la misma ejecución todo lo independiente, generar reportes precisos y no esperar respuestas para refactors/tests/compiladores que no alteren reglas de negocio.
