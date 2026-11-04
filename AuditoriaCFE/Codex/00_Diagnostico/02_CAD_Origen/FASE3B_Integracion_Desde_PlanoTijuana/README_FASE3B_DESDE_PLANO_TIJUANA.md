# Fase 3B — Marco DATRA A1 desde `146468_PLANOTIJUANA.dwg`

**Estado:** paquete de integración para prueba en AutoCAD 2026, no DWT homologada ni CRS validado.  
**Reglas:** ADR-000 + TO-BE v0.2. Una lámina A1 horizontal, mapa en Model Space, marco editable en Paper Space, dos SCR de auditoría en fases posteriores.

## Cambio de estrategia

`146468_PLANOTIJUANA.dwg` **es el origen de la plantilla**: ya contiene el mapa base y no contiene rutas de las auditorías nuevas. No limpiar Mirador/Otay ni copiarlos como cartografía; utilizarlos solo como comparativos del cajetín DATRA y de los detalles aplicables. Preservar la composición CFE de tres zonas (detalles | mapa | leyenda/cajetín). La cartografía de base puede estar encapsulada en bloques; **no ejecutar EXPLODE masivo**.

No cambiamos `INSUNITS=4` automáticamente: el plano base reporta ese valor, pero eso **no acredita** si sus bloques están en coordenadas cartográficas georreferenciadas. Los DWG históricos reportan `INSUNITS=6`, geolocalización `UTM84-11N`, y deben usarse para contrastar al menos dos puntos de control. No escalar, mover ni compensar 11.5 m sin esa comparación.

## Artefactos del paquete

- `MARCO_DATRA_A1_EDITABLE.dxf`: hoja **DATRA_A1** en Paper Space (841 x 594 mm); marco, columna técnica con **espacios reservados** para detalles CFE aplicables, columna central libre para viewport, orientación, leyenda y bloque de cajetín `DATRA_CAJETIN_A1` con atributos editables. **No incluye mapa ni rutas**, porque se importa al DWG existente.
- `generar_marco_datra_a1.py`: código reproducible para rehacer el DXF (`ezdxf`), no necesario para usar el marco.
- `CFE_FASE3B_BASE_SIN_BORRADO.lsp`: inspección y activación/desactivación de capas toponímicas solo en copia de trabajo; **nunca borra geometría**.
- `previsualizacion_marco_A1.png`: vista de diseño a escala aproximada; no sustituye prueba de ploteo.

## Integración rápida en AutoCAD 2026

1. Cierra el original y trabaja con la siguiente **copia** del archivo `146468_PLANOTIJUANA.dwg`, en `AuditoriaCFE/recursos/146468_PLANOTIJUANA_TRABAJO.dwg`. Conserva intacta la carpeta histórica y este original.
2. Abre la copia en AutoCAD. Si quieres reducir rótulos, `APPLOAD` del archivo `.lsp` y ejecuta primero `CFE3B_BASE_INFO` y después `CFE3B_TOPONIMIA_OFF`. Es opcional, no elimina textos ni bloques. Revisa visualmente si persiste toponimia interna de bloques.
3. **Importa el marco**: haz clic derecho en una pestaña de presentación, selecciona **From Template... / Desde plantilla...**. Elige `MARCO_DATRA_A1_EDITABLE.dxf` y selecciona el layout `DATRA_A1`. Alternativamente, en línea de comando utiliza `_LAYOUT`, opción `_Template`, selecciona el DXF y el layout indicado. Autodesk documenta esta importación desde DXF; se importa **la presentación y sus objetos de Paper Space**, no el Model Space del archivo DXF.
4. Abre la pestaña `DATRA_A1`. En **Page Setup Manager** configura `DWG To PDF.pc3` (o PDF nativo disponible) y papel **ISO A1 horizontal, 841 x 594 mm**; tamaño 1:1, área **Layout**, impresora y márgenes según driver. Comprueba que el marco no se recorta. Los nombres exactos del papel pueden variar en tu instalación.
5. El DXF **NO contiene un viewport activado**: crea uno mediante `_MVIEW` / `MVIEW`, ajustándolo solamente dentro de la zona central (papel aprox. x=145..693, y=16..578), configura vista/escala con pruebas de coordenadas y bloquéalo. No intentes que la ciudad completa quepa a una escala ilegible.
6. Revisa `Layout1`: es la hoja Carta heredada de CFE. Si deseas una sola presentación activa A1 en el DWT, **elimínala únicamente en la copia** tras comprobar que no pierdes el contenido del cajetín antiguo que quieras conservar. No elimines Model Space.
7. Tras confirmar el marco editable, los detalles técnicos aplicables, una vista correcta y **dos puntos de control geográficos**, guarda la copia mediante **Save As → AutoCAD Drawing Template (*.dwt)**, como `AuditoriaCFE/recursos/Plantilla_Auditoria_CFE_Tijuana.dwt`. No guardes sobre los archivos históricos.
8. Verifica con un **dibujo nuevo basado en la DWT**: sin rutas antiguas, con cartografía, layout DATRA_A1, cajetín y atributos editables, presentación A1 que exporte correctamente. Después se definen los scripts 01/02 del pipeline; no ejecutarlos todavía.

### ¿Qué conservar de CFE?

El DXF generado preserva **la estructura visual, no reproduce automáticamente los cinco dibujos constructivos del PDF** ni copia logotipos de terceros. Las cinco zonas técnicas tienen guías no imprimibles para recibir los detalles CFE verificados. Para recuperar detalles del original, preferir copiar entidades o bloques seleccionados del `Layout1` CFE en la **copia**, con sus escalas revisadas; no insertar tablas con material, longitud o nombres inventados.

### Por qué no entregamos directamente `.dwt`

Una DWT nativa requiere guardar/validar las estructuras DWG y sus dependencias en AutoCAD. Este entorno sí puede crear un DXF editable y verificable, pero no puede producir con garantías una DWT 2026 que contenga intacto el mapa binario DWG del usuario. El paso final de guardado nativo se ejecuta en su AutoCAD.

### Chequeos antes de dar la plantilla por terminada

- [ ] Copia del DWG base; no se modificaron históricos.
- [ ] `DATRA_A1` existe, sin superposición del marco Carta.
- [ ] Papel ISO A1 841 x 594 mm, layout en mm y PDF sin recortes.
- [ ] Cartografía original en Model Space, sin rutas históricas.
- [ ] Toponimia desactivada por defecto y con posibilidad de reactivarla.
- [ ] Marco DATRA y campos editables, logotipo oficial validado, detalles CFE aprobados.
- [ ] CRS confirmado con dos puntos de control; unidades coherentes entre geometría y importación del pipeline.
- [ ] Viewport del mapa orientado, a escala y bloqueado.
- [ ] Ninguna dependencia ausente (SHX, CTB/STB, XREF, imágenes imprescindibles).
- [ ] DWT abre un dibujo nuevo correctamente sin pasos auxiliares.

**La plantilla aún no puede declararse canónica hasta superar estos controles.**
