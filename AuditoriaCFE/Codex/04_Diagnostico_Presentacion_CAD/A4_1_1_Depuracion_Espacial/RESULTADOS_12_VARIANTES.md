# Resultados de las doce variantes

Las doce variantes se validaron en AutoCAD Core Console 2026 como diagnóstico. Se reabrieron los DWG y se comprobó la idempotencia de SCR02. Los PDF consolidados contienen 126 páginas vectoriales A1 horizontales, verificadas con Poppler y PyMuPDF.

| Auditoría | Radio m | Conservado | Excluido | % | Componentes conservados | Microcomponentes | A1 | Δ A4.1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Natura | 50 | 41 | 397 | 90.64 | 6 | 232 | 4 | -12 |
| Natura | 100 | 360 | 78 | 17.81 | 27 | 35 | 11 | -5 |
| Natura | 200 | 432 | 6 | 1.37 | 5 | 4 | 14 | -2 |
| Natura | 300 | 438 | 0 | 0.00 | 2 | 0 | 16 | +0 |
| Mirador | 50 | 269 | 224 | 45.44 | 24 | 91 | 7 | -11 |
| Mirador | 100 | 465 | 28 | 5.68 | 5 | 17 | 10 | -8 |
| Mirador | 200 | 472 | 21 | 4.26 | 2 | 15 | 10 | -8 |
| Mirador | 300 | 472 | 21 | 4.26 | 2 | 15 | 10 | -8 |
| Otay-Florido | 50 | 317 | 432 | 57.68 | 27 | 179 | 8 | -8 |
| Otay-Florido | 100 | 729 | 20 | 2.67 | 16 | 9 | 12 | -4 |
| Otay-Florido | 200 | 741 | 8 | 1.07 | 3 | 7 | 12 | -4 |
| Otay-Florido | 300 | 741 | 8 | 1.07 | 2 | 7 | 12 | -4 |

- Natura es muy sensible a 50 m. Se deben revisar las subrutas y extremos que quedan fuera antes de elegir.
- Mirador y Otay–Florido tienen el mismo conjunto representado a 200 y 300 m. Los componentes y alertas pueden variar con las aristas auxiliares.
- La media al vecino más cercano de Otay–Florido supera 5 km por la cola extrema, mientras la clase modal es 30–40 m. La media global no interviene en las decisiones.
- Contraste territorial exploratorio. 0 Natura, 14 Mirador y 3 Otay–Florido fuera del AGEM candidato. La cobertura DATRA está pendiente de acreditación.
- Candidatos próximos, por pares de identidades. Natura 23, Mirador 137, Otay–Florido 348. En este último hay 24 pares exactamente coincidentes en 18 posiciones y con distintos tipos.
- Cero cruces AABB de texto y cero cajas recortadas. Las páginas de detalle tienen más de cinco etiquetas primarias. La columna de utilidad solo detecta detalles sin primarias y no sustituye la revisión cartográfica. Las vistas generales siguen el encuadre de la selección.
- En cada variante con exclusiones, el recorte huérfano muestra un punto excluido en el PDF A4.1 original. Se adjunta el contexto de la variante si el punto entra en un viewport; si queda fuera, se documenta esa condición. Natura 300 m carece de exclusiones.
- El cociente de la escala de detalle, el estilo, los símbolos y el texto coinciden con el perfil A4.1. Permanecen pendientes impresión física, revisión de contraste y evidencia de campo.
