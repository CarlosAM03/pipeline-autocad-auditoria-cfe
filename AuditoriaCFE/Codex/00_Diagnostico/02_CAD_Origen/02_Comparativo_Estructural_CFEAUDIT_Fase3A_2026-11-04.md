# Auditorías CFE / DATRA — Fase 3A: comparativo estructural de DWG

**Fecha:** 2026-11-04  
**Estado:** Diagnóstico estructural concluido; selección de donador y DWT aún **no aprobadas**.  
**Normativa interna:** ADR-000 (A/B/C/D), especificación TO-BE v0.2.  
**Fuentes:** `146468_PLANOTIJUANA_estructura_CAD.txt`, `Auditoria-STD-MIRADOR_estructura_CAD.txt`, `Auditoria-STD-OTAY-FLORIDO_estructura_CAD.txt`, generados por `CFEAUDIT` sobre copias DWG.  
**Custodia:** no se han alterado los archivos históricos. Este documento interpreta únicamente el inventario retornado por AutoLISP y no certifica la geometría interna de bloques ni la precisión geodésica.

## 1. Hallazgos comprobados

| Indicador | 146468_PLANOTIJUANA | STD-MIRADOR | STD-OTAY-FLORIDO |
|---|---:|---:|---:|
| `INSUNITS` | 4 (mm) | 6 (m) | 6 (m) |
| `ACADVER` | 25.1s | 25.1s | 25.1s |
| Capas | 91 | 110 | 110 |
| Definiciones de bloque, incl. espacios | 113 | 192 | 266 |
| Referencias externas `IsXRef=true` | 0 | 0 | 0 |
| Entidades de nivel superior en Model | 1,194 | 97,942 | 98,820 |
| Entidades de nivel superior en Layout1 | 219 | 217 | 217 |
| `POINT` en Model | 0 | 527 | 965 |
| `TEXT` en Model | 151 | 6,666 | 7,104 |
| `LWPOLYLINE` en Model | 328 | 4,404 | 4,406 |
| `VIEWPORT` en Layout1 | 4 | 4 | 4 |
| Formato `Layout1` | Carta | Carta | Carta |
| Impresora `Layout1` | None | None | None |

El plano `146468` estaba abierto en `Layout1` (`TILEMODE=0`, `CTAB=Layout1`), y su `EXTMIN`/`EXTMAX` registrados (aprox. 0–11 unidades) no prueban la extensión del mapa en Model Space. Mirador estaba abierto en `Layout1` y tiene `EXTMIN=(456142, 3581870)` y `EXTMAX=(544462, 3605160)`; Otay estaba en `Model` y tiene `EXTMAX_Y≈48,032,600`, incompatible con la concentración geográfica de Tijuana. Ninguno de estos datos certifica un CRS.

## 2. Indicadores de herencia de recursos

- Las 91 capas del plano base se encuentran en Mirador. Mirador y Otay tienen **las mismas 110 capas**, sumando 19 a las del base (incluidas `POSTES`, `CAJAS`, `EXCEDENTE`, `TEXTO` y `RUTA`).
- De 111 nombres de definiciones de bloque compartidos entre base y Mirador, 109 tienen exactamente los mismos metadatos de conteo del inventario; las dos diferencias son los conteos de entidades de `*Model_Space` y `*Paper_Space`. Esto sugiere reutilización de componentes CAD, **no demuestra geometría idéntica**.
- Mirador y Otay comparten 192 definiciones de bloque; 191 tienen el mismo conteo. La diferencia es `*Model_Space`. Otay incorpora 74 definiciones adicionales.
- Mirador y Otay tienen el mismo desglose completo de entidades en `Layout1` (217), incluyendo un `OLE2FRAME`, cuatro `VIEWPORT`, seis `INSERT` y 52 `TEXT`. El plano base presenta 219 entidades, siete `INSERT`, 55 `TEXT` y ningún `OLE2FRAME`. Los marcos son muy probablemente derivados de una composición común, pero su texto, logos, objetos OLE y editabilidad requieren inspección visual.
- Los reportes históricos conservan capas `a-logo Bestel` y `a-logo CFE`; no dar por acreditada la marca DATRA sin ver los objetos y contenidos del cajetín.
- No se declararon XREF externas. El mapa puede ser geometría de nivel superior y/o geometría interna de bloques; esto debe comprobarse en AutoCAD y no autoriza aún una extracción automática.

## 3. Diferencias exactas entre dibujos históricos

Otay–Florido tiene 878 entidades más en Model Space que Mirador. El desglose neto es exactamente:

- **+438 `POINT`** (965 vs. 527).
- **+438 `TEXT`** (7,104 vs. 6,666).
- **+2 `LWPOLYLINE`** (4,406 vs. 4,404).

Las capas que cambian netamente son: `POSTES` +290, `EXCEDENTE` +145, `CAJAS` +3, `TEXTO` +438, `RUTA` +2. El resto de las cantidades por capa de Model Space es igual. Esto confirma una base cartográfica **muy parecida por conteo** y variaciones concentradas en anotaciones/componentes de auditoría; no prueba que cada geometría cartográfica sea espacialmente idéntica.

**Diferencia pendiente de reconciliación:** el TXT/SCR histórico de Mirador contenía 533 comandos `POINT`, mientras el DWG inspeccionado contiene 527 entidades `POINT` de nivel superior (452 en `POSTES`, 55 en `EXCEDENTE`, 20 en `CAJAS`). Diferencia neta: **6**. No atribuirla a un borrado específico sin comparar handles/posiciones y el estado del archivo. En Otay, 965 `POINT` coinciden con el total del TXT histórico.

## 4. Riesgos que bloquean aprobar la plantilla canónica

1. **Unidades distintas:** `INSUNITS=4` (base) frente a `INSUNITS=6` (históricos). `INSUNITS` define escala de inserción, pero **no prueba** la unidad física real de toda la geometría; no convertir ni reescalar en bloque sin controles.
2. **CRS sin verificar:** EPSG:32611 sigue siendo una hipótesis; hacen falta al menos dos puntos de control no coincidentes, identificables y con coordenadas WGS84 acreditadas.
3. **Extensión aberrante en Otay:** `EXTMAX_Y≈4.80326e7`. Es compatible con la anomalía histórica de latitud imposible, pero debe identificarse exactamente qué entidades la causan; no asumir que el origen es únicamente un punto.
4. **Impresión no canónica:** los tres `Layout1` siguen configurados en Carta con `PlotDevice=None`; construir y probar A1 horizontal 841×594 mm.
5. **Identidad empresarial:** no sabemos todavía cuáles son los campos y recursos gráficos DATRA reales. Verificar OLE, logo, texto, bloques y posibles restos de CFE/Bestel.
6. **Separación de recursos:** en los históricos hay infraestructura del levantamiento mezclada con la cartografía y notas. Al crear base, retirar exclusivamente en COPIAS los elementos de auditoría y conservar la cartografía validada.
7. **Anidamiento:** el reporte de `ssget "_X"` no cuenta entidades internas de bloques; la cantidad 1,194 de `146468` **no significa** que tenga menos cobertura territorial.

## 5. Recomendación de recuperación — aún no aprobada

- Usar `146468_PLANOTIJUANA.dwg` como **referencia del formato CFE y candidato a mapa**, sin considerarlo donador único por defecto.
- Usar **Mirador** como primer candidato para estudiar la combinación de cartografía en metros y marco modificado; Otay–Florido como contraste visual y funcional, pero no como fuente directa de geometría limpia debido al extremo anómalo.
- El donador definitivo del **mapa** y el del **cajetín** pueden ser distintos. La decisión se tomará después de verificar coordenadas y el contenido real del Paper Space.
- En una copia de trabajo nueva, crear `Mapa_Tijuana_Vectorial.dwg` aislado de infraestructura histórica y `Plantilla_Auditoria_CFE_Tijuana.dwt` con una sola referencia cartográfica (embebida o XREF declarada), layout A1 y campos DATRA editables.

## 6. Próximas comprobaciones prácticas, sin alterar originales

1. Abrir COPIAS de los tres DWG y comparar visualmente `Layout1` de los tres; identificar el marco, campos DATRA, logos y el objeto `OLE2FRAME` (sin editar valores). Identificar qué parte del cajetín es bloque con atributos y qué parte es `TEXT`/`MTEXT` suelto.
2. En `146468`, cambiar a **Model** (solo visualización) y consultar los límites reales del dibujo y una muestra de coordenadas mediante `ID`/`LIST` en entidades cartográficas reconocibles. Evitar inferencias por `EXTMIN/EXTMAX` del layout.
3. En los tres, identificar físicamente dos puntos de control no coincidentes del mapa con coordenadas de origen confiables. Ejecutar `CFECTRL` solo si los puntos están acreditados. Comparar WCS contra una proyección geodésica estándar; contrastar orientación, posible desplazamiento, escala y CRS antes de trasladar recursos.
4. Localizar la capa y el contenido de la cartografía principal (p. ej. `FTRAZA`, `NLUZ`, bloques `COLONIAS`/`DELEG_NUEVAS`) y verificar si su posición espacial corresponde a los datos de auditoría.
5. Revisar `LAYOUT1` para A1: impresora PDF, `CanonicalMediaName`, escala, márgenes, cuatro ventanas gráficas, estilos, OLE y texto empresarial; conservar una única lámina según C01.
6. Documentar la elección fundamentada de donador mapa/marco y solicitar aprobación antes de extraer o reconstruir la DWT.

**Estado de aprobación:** Fase 3A estructural informativa completada, pero `P-06`, `P-07`, `P-08` y `P-10` del ADR-000 siguen pendientes. No existe todavía DWT canónica aprobada ni se ha autorizado la implementación de scripts productivos.
