# Checklist manual de presentación (owner, AutoCAD 2026)

Usar **copia DWG** indicada por el manifiesto, no la plantilla original ni dibujos históricos.

- [ ] En **Model**, ejecutar `UCS` → World y comprobar `INSUNITS`, `UCSNAME`, orientación de ejes y rangos de las entidades DATRA.
- [ ] Seleccionar dos postes reconocibles y registrar ID, coordenada WCS exacta, GPS acreditada y fuente de esta última. **No aprobar CRS** hasta residuales calculados y tolerancia acordada.
- [ ] En **Paper**, comparar `Layout1` con `DATRA_A1`. Registrar cuál estaba activo en cada captura; trazar solo `DATRA_A1`.
- [ ] En `DATRA_A1`, verificar que haya un único viewport principal, que esté bloqueado y no recorte etiquetas ni fondo.
- [ ] Verificar cifras de postes/cajas/excedentes en los atributos del cajetín, y cotejarlas con reporte/manifiesto del lote.
- [ ] Examinar tres zonas: de mayor densidad, de menor densidad y un punto extremo. Comprobar ID y coordenada íntegra en A1.
- [ ] Comprobar símbolos por tipo, orientación del mapa, leyenda, logo, fuentes sustituidas y dependencias raster/XREF.
- [ ] Comprobar cinco paneles TENSION/SUSPENSION/DERIVACION/EMPALME/OTROS. Si son prototipos, el plano no es FINAL.
- [ ] Repetir SCR02 en una COPIA: conteo idéntico, no se crean duplicados, no borra otras capas ni las referencias.
- [ ] Guardar, cerrar y reabrir el DWG de prueba; exportar PDF A1 y abrirlo en dos lectores.
- [ ] Registrar dictamen y excepciones pendientes de P03/P05/P06/P07/P08/P04.

**Advertencia:** no editar `ctab`, escala, coordenadas o capas del DWG principal para forzar una aprobación visual. Las pruebas proponen ajustes solo en copias y con comparación reproducible antes/después.
