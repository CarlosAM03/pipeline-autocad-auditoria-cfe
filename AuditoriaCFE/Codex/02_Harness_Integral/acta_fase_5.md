# Fase 5 — CP-04 y evidencia nativa

Compilación: COMPLETADO_TECNICO. Entrega DWG/PDF/DWT: PENDIENTE_EVIDENCIA.

El SCR02 consume 02 v1/v2 a través del lector común. Se habilita con controles CRS y unidades declaradas; la alternativa diagnóstica usa un archivo distinto, copia explícita y rótulo NO_VERIFICADO. Sin esos datos el SCR02 informa el gate y no dibuja. Un bloque por ID, etiquetas P/C/E con número estable y XDATA con ID completo; WGS84 textual y distancias planas en las aristas humanas confirmadas. No se utiliza DFS ni orden de filas para construir líneas.

La repetición retira exclusivamente entidades etiquetadas del mismo propietario de auditoría. El runtime cuenta INSERT reales por tipo y aristas reales antes de emitir resumen. Un fallo deshace el grupo de operaciones. Se reutiliza el viewport principal de la copia; no se inserta otro mapa. La única lámina imprimible de entrega es DATRA_A1, A1 horizontal. Layouts heredados se conservan como contenido del original, no se publican como hojas adicionales.

Verificación offline: suite completa de fase 4 **70/70 OK**, 0 fallidas/omitidas, 72.737 s. Ocho pruebas CAD repetidas tras endurecimiento: **8/8 OK**, 0 fallidas/omitidas. No representan una ejecución visual AutoCAD.

Ensayo nativo en copia sintética `Ensayo-CAD-Nativo`: AutoCAD Core Console 2026 W.122 arrancó; primer intento no cargó LISP por ruta de confianza; segundo detectó que Core Console no expone documento ActiveX. Se sustituyó el uso de COM por AutoLISP/DXF/command nativos. Tercer intento configuró CP03 y reveló un fallo del manejador de errores: `error` no es una función AutoLISP. Se corrigió por un fallo explícito atrapado y rollback. El último reensayo queda para el cierre, por petición del usuario. No declarar CP04 nativo aprobado mientras no exista reporte real de inserción.

La lectura nativa de la copia acreditó INSUNITS=4, WORLDUCS=1 y UCSNAME vacío. DATRA_A1 declara 841×594 mm, rotación 0, escala 1:1; Layout1 también referencia papel A1, pero tiene escala 25.4 y extents de pulgadas. **Esto confirma la necesidad de conservar P-06**: no se escaló cartografía ni se convirtió la mera etiqueta de unidades en metros acreditados.

Se observaron sustituciones de seis estilos/fuentes durante apertura (incluye ARCHITXT, OUTLINE y OpenSansCondensed-Light). Los detalles de los cinco paneles, raster/logo, proxies, encuadre y legibilidad requieren cotejo del owner. No hay DWT canónica ni PDF FINAL.

Siguiente fase: CLI batch, CI portable, benchmarks, cuatro auditorías con gates, documentación de aceptación y último ensayo nativo.
