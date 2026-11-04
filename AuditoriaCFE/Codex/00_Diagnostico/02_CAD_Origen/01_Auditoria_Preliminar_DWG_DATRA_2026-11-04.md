# Fase 3A — Auditoría técnica preliminar de DWG para plantilla DATRA

**Fecha:** 2026-11-04  
**Estado:** Parcial — inspección binaria y visual realizada; inspección de entidades CAD nativas pendiente de ejecutar en AutoCAD.  
**Documentos normativos:** `AuditoriaCFE/Docs/ADRs/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md` y `AuditoriaCFE/Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.2.md`.  
**Objetivo:** separar recursos reutilizables de auditoría histórica y determinar, con evidencia, cómo construir `Plantilla_Auditoria_CFE_Tijuana.dwt` y `Mapa_Tijuana_Vectorial.dwg` sin modificar los originales.

## 1. Evidencia inspeccionada y comprobaciones

| Recurso | Tamaño en bytes | SHA-256 | Evidencia |
|---|---:|---|---|
| `Auditoria-STD-MIRADOR.dwg` | 28,590,936 | `b8fb95d1424e1690f0cef486f72a9ee0348c19373637ffdd30455e5468258ecd` | Formato DWG `AC1032` (2018+). |
| `Auditoria-STD-MIRADOR(1).dwg` | 28,590,936 | `b8fb95d1424e1690f0cef486f72a9ee0348c19373637ffdd30455e5468258ecd` | **Binariamente idéntico** a Mirador anterior; no es otra revisión. |
| `Auditoria-STD-OTAY-FLORIDO.dwg` | 33,128,920 | `c8b5c21b6430ad3124fab351a88f5baeb16ae7801cea1a4d327d08ff90c0e978` | Formato DWG `AC1032`. |
| `AuditoriaCFE.dwg` | 23,461,846 | `e0787b6a16c0ce51364cabe0331ac3dfeb566625f51dc3239b5fa104435da198` | Formato DWG `AC1032`. |

### Salidas PDF históricas asociadas

| PDF | Tamaño hoja | Operaciones vectoriales de dibujo detectadas en PDF | Imágenes incrustadas en PDF | Metadatos de creador |
|---|---|---:|---:|---|
| `Auditoria-STD-MIRADOR.pdf` | Carta apaisada, 279.4 × 215.9 mm | 22,888 | 1 | AutoCAD 2026, English |
| `Auditoria-STD-OTAY-FLORIDO.pdf` | Carta apaisada, 279.4 × 215.9 mm | 20,324 | 1 | AutoCAD 2026, English |
| `AuditoriaCFE.pdf` | Carta apaisada, 279.4 × 215.9 mm | 12,990 | 0 | AutoCAD 2026, English |
| `PlantillaAuditoriaCFE.pdf` | **A1 apaisada, 841.0 × 594.1 mm** | 3,229 | 0 | PDFium |

**Interpretación y límite:** Los PDF muestran abundante contenido vectorial y la composición cartográfica visible; **no permiten afirmar** cuántas capas, bloques, XREF, imágenes, fuentes SHX, layouts o entidades existen en cada DWG. Tampoco acreditan que los layouts internos sean Carta: el dato corresponde únicamente a la exportación PDF.

Se intentó abrir el DWG con el lector de inspección disponible (`ezdxf.addons.dwg`), que respondió `DwgVersionError: unsupported DWG version, signature AC1032`. No se alteraron fuentes ni se efectuaron conversiones destructivas. La inspección CAD estructural requiere AutoCAD local o una conversión fiel de copias a DXF.

## 2. Observaciones visuales y destino propuesto de recursos

**Reutilizar previa auditoría:** composición de la lámina (tres franjas), mapa de calles de Tijuana, marco y cajetín de los DWG Mirador/Otay, rosa de los vientos, mapa llave, detalles constructivos aplicables, tablas, estilos y cualquier bloque editable.

**No copiar directamente como contenido de plantilla:** poste/caja/excedente de rutas previas; numeración azul grande que invade el plano; tablas superpuestas al mapa; valores de resumen del levantamiento anterior; anotaciones de nombres/zonas no aplicables; rutas/fibras pintadas por una auditoría concreta; coordenadas con proyección histórica defectuosa.

**Revisar contra requisitos DATRA/CFE:** Los PDFs entregados muestran textos y logotipo de CFE, campos territoriales/administrativos y detalles constructivos heredados de la referencia. No asumir que la división, responsables, teléfono o especificación de material son correctos para DATRA. Los campos no acreditados quedarán editables/vacíos; símbolos y detalles solo se usarán si corresponden a instalación real.

La salida PDF de Mirador y Otay muestra la misma estructura general (detalles a la izquierda, cartografía central, orientación/ubicación/simbología/cajetín a la derecha). **No se eligió todavía un DWG ganador**: esa elección requiere examinar la organización CAD nativa y la completitud real del mapa.

## 3. Auditoría CAD nativa requerida para cerrar P-06 y P-10

Para CADA DWG de Mirador, Otay–Florido y, como contraste, AuditoriaCFE:

1. Inventariar layouts y configuración de papel `CanonicalMediaName`, unidades de papel, orientación y dispositivo de trazado; comprobar si A1 ya existe en alguna presentación.
2. Contabilizar por espacio, capa y tipo de entidad; distinguir mapa, redes antiguas, anotaciones, bloques de simbología y cajetín. Describir elementos que sean `INSERT` y geometría anidada no contabilizada directamente.
3. Enumerar bloques y XREF, sus rutas, dependencias y faltantes; buscar mapas raster enlazados, fuentes, tipos de línea y CTB/STB necesarios.
4. Confirmar `INSUNITS`, `INSBASE`, UCS/WCS y extents del modelo. `INSUNITS=6` **solo expresa metros**, no valida un CRS.
5. Obtener **dos puntos de control independientes y espacialmente separados** sobre elementos conocidos, en coordenadas WCS y con sus latitudes/longitudes originales verificadas. Comparar contra una transformación geodésica estándar; no corregir visualmente por desplazamientos arbitrarios.
6. Verificar la editabilidad del marco, simbología, tabla y cajetín; identificar si la geometría de Paper Space está encapsulada en bloque editable o está hecha con primitivas separadas.
7. Elegir justificadamente el donador del **mapa** y el del **marco** (pueden ser distintos). Evaluar cobertura, CRS, limpieza, separación de capas, independencia de XREF/fuentes y tamaño.

### Herramienta de inspección adjunta

`CFE_AUDITORIA_DWG_SOLO_LECTURA.lsp` ofrece dos comandos para ejecutar **en copias** abiertas en AutoCAD 2026 para Windows:

- `CFEAUDIT`: exporta variables de dibujo, layouts, capas, definiciones de bloques/XREF y conteos de entidades de primer nivel por espacio/tipo/capa, en TXT. **No guarda ni modifica el DWG**.
- `CFECTRL`: permite elegir manualmente dos puntos de control y registrar sus coordenadas WCS junto a su identificación/lat-lon confirmada. Requiere que el usuario utilice OSNAP y elija puntos físicos conocidos; **no demuestra por sí solo el CRS**.

Los TXT se escriben en `AuditoriaCFE/Codex/00_Diagnostico/02_CAD_Origen/`, sin sobrescribir reportes existentes. **La herramienta LISP fue revisada estáticamente, pero no ejecutada en AutoCAD aquí**; cualquier incompatibilidad deberá registrarse, no repararse modificando fuentes históricas.

## 4. Reglas de aceptación para la futura DWT (ADR-000 / v0.2)

- Un DWT reutilizable que, al crear un DWG nuevo, contenga **un solo mapa de Tijuana** correctamente situado, marco DATRA/CFE y una sola presentación **A1 horizontal**.
- Mapas/rutas en **Model Space a coordenadas planas reales**; marco/cajetín/tablas fijas en **Paper Space**; viewport muestra región pertinente sin desplazar geometría.
- Capas y símbolos permanentes separados de rutas y elementos de una auditoría; bloques editables para `POSTE` genérico, `CAJA_EMP`, `EXCEDENTE` y etiquetas tipo/número/coordenadas.
- Tabla impresa con recuento de entidades **únicas dibujadas** por tipo; otras métricas y exclusiones solo en resumen interno.
- Cajetín basado en recursos existentes Mirador/Otay, editable y sin datos inventados; detalles constructivos solo cuando aplican.
- Una sola lámina A1: evaluar legibilidad del plano general y reportar incumplimiento sin ocultar etiquetas ni crear láminas extras.
- En primer script `.scr` verificar/ajustar dibujo existente **sin volver a insertar el mapa**; en segundo script insertar las entidades/tramos confirmados/tabla. Ambos se ejecutarán luego sobre DWT abierta.
- Si el mapa va como XREF, verificar **portabilidad del path** cuando un dibujo se crea desde DWT y luego se guarda en una carpeta de auditoría diferente.
- No generar ni aprobar CSV geográfico proyectado `02_elementos_proyectados.csv` hasta que el CRS CAD esté respaldado por controles.

## 5. Bloqueos y estado

| Control | Estado | Acción necesaria |
|---|---|---|
| Compatibilidad de formato DWG 2018+ | Confirmada por firma binaria | Verificar apertura en AutoCAD instalado |
| Copia de Mirador recién compartida | Idéntica por SHA-256 | Solo analizar una copia |
| Formato PDF histórico Carta / referencia A1 | Confirmado | Revisar media configurada en layouts CAD |
| Existencia visual de marco y composición reutilizables | Confirmada en PDF | Localizar objetos editables dentro del DWG |
| Capas, bloques, XREF, estilos y fonts | **No verificado** | `CFEAUDIT` en AutoCAD y/o DXF desde copia |
| Donador de mapa y donador de marco | **No elegido** | Inventario y comparación por evidencia |
| CRS del mapa y dos puntos de control | **No verificado** | `CFECTRL`, coordenadas conocidas y prueba pyproj |
| Plantilla DATRA canónica `.dwt` | **No creada** | Fase 3B tras resolver bloqueos |
| Scripts operativos 01 y 02 | **No creados** | Codex posterior, tras aprobar DWT |

**Checkpoint:** La Fase 3A se encuentra iniciada y documentada, pero **no está técnicamente cerrada** hasta incorporar los reportes CAD nativos y controles geográficos. No declarar plantilla lista ni cambiar el ADR de manera implícita.
