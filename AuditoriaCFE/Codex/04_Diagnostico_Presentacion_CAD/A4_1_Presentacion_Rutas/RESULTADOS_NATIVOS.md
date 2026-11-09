# Ensayos nativos A4.1

Motor AutoCAD Core Console 2026 inglés (W.122). Las copias usan la plantilla DATRA vigente. Se ejecutan SCR01 y SCR02, se repite SCR02, se guarda, se cierra y se reabre. Se compara la geometría etiquetada y el muestreo de Model heredado, y se comprueban la cámara y el cajetín de cada hoja. Las páginas proceden de DWG To PDF.pc3 y se concatenan sin rasterizar. Poppler y PyMuPDF revisan formato y render.

| Auditoría | POSTE / CAJA_EMP / EXCEDENTE | General, Model/mm | Detalle, Model/mm | Páginas verificadas | Detalle denso |
|---|---:|---:|---:|---:|---:|
| Natura | 438 / 0 / 0 | 38,828 | 6 | 16 | 14, 55 etiquetas |
| Mirador | 414 / 20 / 59 | 182,002 | 6 | 18 | 11, 135 etiquetas |
| Otay–Florido | 586 / 17 / 146 | 7888,899 | 6 | 16 | 4, 109 etiquetas |

Los símbolos en detalle miden 1,1 mm para poste/caja y 1,4 mm de ancho para excedente. El texto WGS84 nominal mide 1,8 mm. En la vista general, los tamaños de símbolos en papel varían con la cámara. Las escalas de la matriz están expresadas en unidades Model por mm de papel, con CRS diagnóstico. La vista general rotula sectores. Las coordenadas completas se conservan en el índice y en sus páginas primarias.

## Inspección de presentación

- Natura, hoja 14. Se distinguen el poste y las coordenadas junto a manzanas y rótulos de calle. Se conservan trazos cartográficos de color.
- Mirador, hoja 11. Los textos de coordenadas y llamadas se distinguen en el recorte de 185 dpi. Desaparece la banda negra de A3 V4, que presentaba 122441 pares de cajas superpuestas. Algunos líderes cruzan rasgos de la cartografía.
- Otay–Florido, hoja 4. Se distinguen las coordenadas y varias clases de símbolo sobre el mapa. Hay 18 coordenadas compartidas por 39 identidades de tipos distintos en todo el lote. El índice conserva el tipo y la identidad por página. Revisar en A1 si las formas y colores coincidentes requieren otro tratamiento gráfico.
- La general de Otay–Florido conserva el extremo que abre el encuadre. Por ello la cartografía urbana es diminuta en esa hoja. Las páginas de detalle conservan el contexto local donde existe mapa heredado. La atribución geográfica del extremo sigue sujeta a P-03/P-06.
- La plantilla heredada conserva norte, marco y cajetín. El cajetín muestra identidad de auditoría, número de hoja y conteo global, y la cabecera muestra conteo primario. Una nota aclara el bloque EXCEDENTE de ensayo en el mapa frente al triángulo heredado en la leyenda. Los paneles de detalle están pendientes.
- Core Console sustituyó varias fuentes de la plantilla por simplex.shx. Se mantiene la geometría embebida y se registra la sustitución para revisión humana. La prueba de legibilidad a escala física y el contraste cartográfico siguen abiertos.

## Verificación de la entrega

Los 50 trazados definitivos pasaron Poppler y PyMuPDF. Se verificaron XDATA, tipos, persistencia al reabrir, idempotencia de SCR02, conteos globales de cajetín, numeración, cobertura de etiquetas y cámaras. El residuo XY máximo de los tres lotes fue menor que 9,4×10⁻¹⁰ unidades de Model. En los tres inventarios hubo cero cajas de coordenadas o marcas de sector superpuestas, y cero cajas fuera del viewport. Las llamadas son segmentos gráficos en papel, con posible interacción visual con rasgos de mapa.

Se inspeccionaron los recortes densos de las tres auditorías y la vista general de Otay–Florido. En el primer trazado de esta última se amontonaban las referencias D de sectores urbanos. La revisión separó las marcas en papel y les añadió líderes; se trazaron de nuevo los tres PDF y se verificó una marca por detalle. La general sigue siendo un índice de cobertura completa. Un encuadre urbano suplementario puede evaluarse con el responsable si desea un resumen cartográfico adicional.

Para contraste se ensayaron dos copias separadas de la hoja 11 de Mirador. La primera aplicó color 8 y grosor 0,05 mm mediante VPLAYER a cinco capas de calles/manzanas. El recorte mostró fondos de manzana más tenues con rótulos y componentes aún visibles. La segunda congeló dos capas de numeración de manzanas en el viewport. El recorte mostró menos números verdes, conservando los trazos de calles. Ambos PDF fueron trazados por AutoCAD, tienen una A1 y conservaron vectores. Las variantes se guardaron en evidencia_contraste de la salida privada de Mirador. La entrega principal conserva el contraste heredado para que el responsable compare las opciones.
