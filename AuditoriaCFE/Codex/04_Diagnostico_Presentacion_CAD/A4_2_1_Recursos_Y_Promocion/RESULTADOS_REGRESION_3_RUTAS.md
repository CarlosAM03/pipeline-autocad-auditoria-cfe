# Regresión de rutas

| Ruta | Inventario | Dibujados | Exclusiones visuales | Hojas | Residual XY máximo (unidades Model) |
|---|---:|---:|---:|---:|---:|
| Natura | 438 | 438 | 0 | 16 | 9.39 × 10⁻¹⁰ |
| Mirador | 493 | 472 | 21 | 10 | 9.34 × 10⁻¹⁰ |
| Otay–Florido, incluido Bomberos | 749 | 741 | 8 | 12 | 9.39 × 10⁻¹⁰ |
| Total | 1,680 | 1,651 | 29 | 38 | |

Los CSV 00, 01, diagnóstico 02, linaje, asociaciones, índice y paginación coincidieron por SHA-256 con la línea base a 300 m. Los CSV y summaries de exclusiones coincidieron con A4.2. Los seis XLSX pasaron CRC y conservan Decision_Visual. Cada DWG pasó los dos SCR, repetición de SCR02, persistencia, identidad/XDATA y posiciones en Model, verificación de atributos y viewports. En cada layout se encontraron los cuatro INSERT constructivos D01/D02/D04/D05. Se conservaron las geometrías heredadas inventariadas.

Compilación Python y suite local de 104 casos aprobados, cero fallidos y cero omitidos. El primer recorrido de PDF produjo las hojas pero falló en la escritura del registrador AutoLISP auxiliar. Se conservó el log y se repitió la inspección de los DWG trasladados con el registrador corregido antes de validar los PDF. El fixture también se reubicó después de que el gate de custodia rechazara su carpeta inicial fuera de auditorias.

El dry-run de los perfiles principales reveló que la configuración local de Otay–Florido omitía Bomberos. Se verificó el hash del XLSX, se incorporó en cuarta posición y se ejecutó el perfil corregido sobre una copia aislada. Reprodujo por hash el inventario, la proyección diagnóstica, el linaje, las exclusiones, el índice y las 12 hojas del lote nativo.
