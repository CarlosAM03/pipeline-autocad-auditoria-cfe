# Auditoría CFE/DATRA — cierre técnico A4.2.1 y decisiones de entrada A4.2.2

**Fecha documental:** 2026-11-09  
**Repositorio:** `CarlosAM03/pipeline-autocad-auditoria-cfe`  
**Rama:** `codex/etl-unificado-auditoria-js`  
**SHA informado y contrastado en PR:** `955b0a87febfb24ef7873cf0ebab33d7ae887074`  
**Estado del PR:** abierto, sin merge  
**Tipo de cierre:** técnico; no constituye entrega CFE ni aceptación física.

## 1. Evidencia A4.2.1

El reporte de Codex documenta la promoción de la base operativa `AuditoriaCFE/recursos/PlantillaMarcoDatraMapaTijuana.dwg`, SHA-256 `3e30879ad6894a04c87f9fc3a63b41f13487a39f296a9547d361c00b716bf7be`, tras crear respaldo recuperable, así como la generación y reapertura de DWT nativa. El checkpoint público indica que ambos PNG se empacan como referencias relativas y se verificaron en los planos trasladados. La suite local reporta 104 pruebas aprobadas; los cuatro jobs de GitHub Actions reportados quedaron en verde.

| Auditoría | Representadas | Exclusiones visuales | PDF A1 |
|---|---:|---:|---:|
| Natura | 438 | 0 | 16 páginas |
| Mirador | 472 | 21 | 10 páginas |
| Otay–Florido, incluye Bomberos | 741 | 8 | 12 páginas |
| **Total** | **1651** | **29** | **38 páginas** |

La revisión de los PDF adjuntos confirma 16/10/12 páginas A1 horizontal. Su primera página contiene dos imágenes por página PDF (logo y mapa de ubicación), además de cartografía vectorial. Los paneles históricos recuperados aparecen en el lateral izquierdo; el D03 — derivación continúa indicado como pendiente. Hay zonas con acumulaciones de etiquetas, cuya aceptación física A1 aún requiere comprobación humana.

**Límites:** no se ha verificado aquí la ejecución en un segundo equipo ni la inspección manual de DWG realizada por el owner. Los valores y hashes corresponden a lo reportado y a la revisión documental; cada corrida posterior debe generar los suyos.

## 2. Decisiones nuevas del owner para A4.2.2

1. **Ubicación de zona:** el recuadro de localización deberá enfocarse en la cobertura de la ruta de la auditoría, no mostrar únicamente el mismo mapa general indiferenciado en las tres.
2. **Tablas de referencia CFE:** Codex inspeccionará `Auditorias-20261104T035633Z-1-001/Plantilla (3)-ejemplo.pdf`, `Auditorias-20261104T035633Z-1-001/AuditoriaCFE2.dwg` y los reportes del pipeline. Solo incluirá columnas/campos con respaldo. No inventará cantidades ni especificaciones. La hoja tabular será la **primera página del PDF** de cada auditoría.
3. **Fecha de auditoría:** `09/11/2026`, conforme a la indicación administrativa del owner; debe distinguirse de fecha de levantamiento físico de campo si no está acreditada.
4. **Elaboró:** `Carlos Armenta`.
5. **Revisó:** `Ing. Adolfo de La Torre`. El nombre consignado no acredita firma ni aprobación formal.
6. **CRS:** se solicita identificar el realmente empleado, incluyendo WGS84 `EPSG:4326` para coordenadas de origen y `EPSG:32611` como **candidato** del pipeline; actualmente `crs_validado=False` y P-06 exige dos controles WCS comprobados y evidencia. No se permite escribir VALIDADO sin superar P-06.
7. **Estado de revisión:** el owner solicita cambiar PRELIMINAR a FINAL. La implementación debe generar el cambio **solo mediante gate de publicación**: mientras P-03/P-05/P-06 y aceptación humana continúen pendientes, indicar `LISTO PARA REVISIÓN FINAL / NO PUBLICABLE` o `PRELIMINAR` según el contrato, sin falsear `FINAL`.
8. **Simbología:** cada icono del panel derecho debe coincidir en geometría/tipo/convención con los bloques realmente usados, sin anunciar líneas de ruta confirmadas cuando no hay aristas verificadas.

## 3. Inventario de tablas de la referencia CFE

En la hoja de referencia A1 se observan tres tablas/zonas distintas: (a) `RESUMEN ESTRUCTURAS CFE EMPLEADAS...`, con descripción/cantidad/unidad y conceptos de materiales/instalación; (b) `LISTA DE ESTRUCTURAS CON COORDENADAS EN GRADOS DECIMALES`, con poste, material y X/Y; (c) `FICHA TÉCNICA DEL CABLE`, con campos de tipo/modelo/marca/peso/número de kilómetros, entre otros. Los datos disponibles sustentan inventario, tipos canónicos, procedencia, IDs, latitud/longitud, exclusiones y algunas métricas de presentación. **No sustentan, por sí solos, materiales físicos, metros de cable tendido, calibres, herrajes, fabricante, altura de postes, modelo ni costos.**

Recomendar una primera página `RESUMEN TÉCNICO DE AUDITORÍA` con tablas parciales fieles al propósito de CFE y anexo de coordenadas paginado si no cabe. Priorizar un índice de identificadores y ubicación con fuentes de datos; la página 1 siempre conserva sus tablas aun cuando haya hojas de apoyo posteriores. Ningún registro válido deberá omitirse del expediente tabular por falta de espacio.

## 4. Invariantes

- Tres auditorías, radio de visibilidad 300 m, 1651 identidades dibujadas, 29 exclusiones preservadas, inventario de origen 1680 sin cambios.
- 38 hojas cartográficas actuales como línea base; añadir páginas tabulares no significa borrar páginas ni volver a numerar silenciosamente.
- Dos scripts manuales (`01_configurar_plano.scr`, `02_dibujar_auditoria.scr`), plantilla operativa DATRA con logo y mapa, referencias relativas portables, DWG independiente por ruta, un único PDF final por ruta.
- D03 permanece pendiente; P-03, P-05 y P-06 son controles independientes.
- No publicar material privado en GitHub; mantener PR #1 abierto.

## 5. Condición para concluir A4.2.2

Generar, en copias, tres DWG y tres PDF consolidados donde la primera hoja tenga las tablas documentables, la ubicación se centre en la cobertura correspondiente y el cajetín consigne los datos administrativos autorizados; verificar simbología, conteos, integridad vectorial, referencias raster, 300 m, CSV/XLSX, linaje, exclusiones, dos SCR, idempotencia, reapertura, CI y portabilidad. Entregar matriz `tabla → campo → fuente → fórmula → estado`, alertas por dato no acreditado, paquete privado y checklist de revisión manual. La **liberación FINAL CFE** seguirá condicionada a los gates y firma/aceptación pertinentes.
