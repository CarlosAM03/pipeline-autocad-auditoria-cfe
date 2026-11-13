# Resultados de pruebas CAD

| Auditoría | Base | Representados | Sin representar | Hojas | Mapa idéntico a 50 dpi | Cajetín idéntico a 50 dpi |
|---|---:|---:|---:|---:|---:|---:|
| Natura | 438 | 438 | 0 | 16 | 16/16 | 16/16 |
| Mirador | 493 | 472 | 21 | 10 | 10/10 | 10/10 |
| Otay-Florido | 749 | 741 | 8 | 12 | 12/12 | 12/12 |

- Los tres paquetes se regeneraron mediante el flujo ordinario con radio omitido. El manifiesto registró 300 m. El plan, el índice, los CSV de inventario/diagnóstico, el linaje y las asociaciones coinciden byte a byte con 300 m aprobado. Los IDs y los motivos de las 29 exclusiones coinciden. Se verificaron los dos XLSX por auditoría y su pestaña Decision_Visual.
- Se ejecutaron los dos SCR, se repitió SCR02 y se reabrieron los tres DWG. El propietario XDATA del ensayo ordinario difiere del experimental por diseño. Se verificó el propietario de cada auditoría y se compararon por separado todos los IDs, tipos y coordenadas. El primer comparador rechazó esa diferencia de propietario y se corrigió sin repetir los trazados.
- Se verificaron cuatro bloques históricos por layout y cero entidades con referencias raster o underlay. Las 38 hojas se validaron como A1 horizontal vectorial mediante Poppler y PyMuPDF. Se compararon las tres zonas en todas las hojas y se conservaron capturas nativas antes/después.
- Suite local: 103 aprobadas, cero fallidas, cero omitidas. Compilación y dependencias comprobadas. Se probaron el default, el override, null y la protección de los contratos. Ensayos omitidos: impresión física, GUI y fixture nativo adicional.
- DWT: la primera exportación agotó el tiempo por el orden de argumentos en SAVEAS. Con la secuencia métrica correcta se creó la plantilla real y se reabrió en Core Console.
