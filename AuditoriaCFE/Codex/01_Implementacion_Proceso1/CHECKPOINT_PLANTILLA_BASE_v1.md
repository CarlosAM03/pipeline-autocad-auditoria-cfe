# Checkpoint — plantilla DATRA A1, primer corte

Fecha: 2026-11-04. **Estado: candidata v1.0, cierre de presentación condicionado a comprobar detalles técnicos en PDF.** La versión operativa no reemplaza por sí sola la verificación geográfica P-06 requerida para proyectar elementos.

## Evidencia comprobada a partir de PDF del usuario

Archivo PDF revisado: `PlantillaMarcoDatraMapaTijuana.pdf` (una página). Tamaño confirmado mediante PyMuPDF: **2384 × 1684 puntos**, equivalente aproximadamente a **841 × 594 mm (ISO A1 horizontal)**.

La composición contiene mapa vectorial denso en el centro, orientación, ubicación de zona, **leyenda derecha visible** (poste, caja, excedente, ruta, ramal), identificación DATRA y logotipo. El cuadro de conteos figura vacío a propósito: se completará por auditoría. Los campos de responsables/fecha/ruta son editables o están pendientes. **El panel izquierdo sí tiene los encabezados `TENSION`, `SUSPENSION`, `DERIVACION`, `EMPALME`, `OTROS`, pero las ilustraciones constructivas no se imprimen en ese PDF.**

## Corrección de los detalles que faltan

La fuente **no debe inventarse**. Abrir `146468_PLANOTIJUANA.dwg` y la copia de `PlantillaMarcoDatraMapaTijuana.dwg` en AutoCAD; ejecutar `CFECHEQUEODETALLES` en ambas. Comprobar:

1. Si las ilustraciones originales residen en Model, especialmente capa `a-detalles`; si también existen en Model del archivo nuevo.
2. Si la presentación original contiene viewport(s) orientadas a los dibujos técnicos y la DATRA solo conserva viewport principal del mapa.
3. Si estas capas están congeladas en la ventana gráfica (VP Freeze), apagadas, o desactivadas para impresión.
4. Si el layout nuevo tiene paneles vacíos **porque el generador DXF solo dibujó encabezados**; en tal caso, cambiar opciones de ploteo no crea geometría ausente.

**Corrección preferida:** recuperar desde el original CFE las vistas/bloques **exactos** de detalles, en una copia del archivo DATRA, ajustarlos a los cinco recuadros izquierdos y verificar ploteo de PDF. No replicar detalles eléctricos/cableado con diagramas aproximados.

## Aceptación manual

- [ ] El PDF A1 muestra los dibujos técnicos apropiados en los recuadros de la izquierda (o el owner aprueba explícitamente su omisión por no aplicar).
- [ ] Se ven los cinco símbolos de la leyenda derecha en pantalla **y** al exportar PDF.
- [ ] No hay referencias a responsables/zonas ajenas a DATRA.
- [ ] El logotipo DATRA se ve en AutoCAD y en PDF sin depender de rutas temporales.
- [ ] El cajetín se puede editar y los conteos siguen siendo campos de auditoría, no valores inventados.
- [ ] La lámina se exporta en A1 horizontal (841 × 594 mm) completa, sin recortes.
- [ ] No hay postes/rutas históricas precargados como datos de esta auditoría.
- [ ] Se crea desde AutoCAD una DWT con nombre canónico `AuditoriaCFE/recursos/Plantilla_Auditoria_CFE_Tijuana.dwt` y se prueba con un DWG **nuevo** nacido de ella.

`P-06` (CRS/unidades/geometría) sigue requiriendo **dos controles geográficos** para habilitar `02_elementos_proyectados.csv`. La aprobación visual del marco no implica la aprobación geodésica.
