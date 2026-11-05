# Checklist nativo — aceptación pendiente

Se aplica a copias; no guardar sobre recursos ni históricos. El ensayo sintético no acredita CRS ni campo.

1. Ejecutar CLI y `--verificar-paquete`. Anotar ID de manifiesto, hash de base y copia específica. Cerrar cualquier dibujo original que pueda confundirse, sin guardar cambios del usuario por automatismo.
2. Abrir copia en AutoCAD 2026 inglés. Registrar INSUNITS, WORLDUCS, UCSNAME, Model/Layout, unidades reales mediante dos controles identificables. Mantener EPSG:32611 como candidato hasta residual acreditado; no escalar ni sumar ~11.5 m.
3. Ejecutar exactamente SCR01 y SCR02; autorizar solo la carga del LISP cuyo hash coincide. Comprobar que SCR01 no crea INSERTs de auditoría ni otro mapa. Un error debe deshacer su grupo y quedar visible.
4. Repetir SCR02: mismos INSERT físicos y aristas, sin duplicados. Verificar recuento por bloque POSTE/CAJA_EMP/EXCEDENTE, rótulos P/C/E, ID completo XDATA, WGS84, distancias sobre aristas confirmadas. Sin topología, no debe haber líneas DATRA_RUTA.
5. Ejecutar inspección del runtime sobre la copia si hace falta. Inventariar estilos sustituidos, XREF/raster/logo/mapa/proxies; verificar cinco paneles TENSION/SUSPENSION/DERIVACION/EMPALME/OTROS. Prototipos solo esquemáticos, sin afirmar herrajes ni cable.
6. Revisar DATRA_A1: 841×594 mm, horizontal, escala de papel 1:1. No imprimir Layout1/Model adicionales. Revisar viewport del mapa, margen, cajetín editable, logo, norte y paneles. No aceptar únicamente valores DXF sin revisar el papel.
7. Plot PDF en copia: una página, tamaño físico A1, sin recortes y con etiquetas completas. Leer muestras densas y aisladas y todas las clases; General requiere control visual completo. Colisiones o tamaño ilegible => BLOQUEANTE FINAL; owner debe aprobar estrategia o excepción normativa.
8. Guardar DWG de prueba, cerrar y reabrir; confirmar persistencia de INSERT/XDATA/líneas y recursos. Guardar DWT canónica solo si la plantilla ya fue aceptada; reabrir nuevo DWG desde esa DWT y repetir.
9. Adjuntar evidencia nativa y capturas auténticas en salida/resultados_cad, con hashes. No fabricar capturas ni certificar que el PDF fue revisado cuando solo se comprobaron dimensiones.
10. Owner registra ACEPTADO_HUMANO con nombre, fecha, evidencia y alcance. Software/CI verde no produce FINAL automáticamente.

## Limitaciones conocidas de la base

La lectura en Core Console confirmó INSUNITS=4 y WCS activo. DATRA_A1 declara A1 mm; Layout1 tiene extents y escala de pulgadas. La escala geográfica real sigue sin controles. Se detectaron sustituciones de fuentes y objetos personalizados. La geometría de paneles y legibilidad no se acredita por el inventario textual.
