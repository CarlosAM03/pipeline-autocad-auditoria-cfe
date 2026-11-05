# Fase 3 — fuentes espaciales y topología

Importador KML/KMZ sin extracción ni red, con límites de tamaño/ratio/entradas, rechazo de traversal, enlaces, cifrado y DTD/entidades. Point/LineString/MultiGeometry/ExtendedData se trazan; geometrías con coordenadas imposibles se conservan como INVALIDA, nunca se corrigen ni detienen las demás geometrías válidas. El KMZ real autorizado existe y fue copiado con hash idéntico a las cuatro entradas. Su lectura inicial detectó 11 tokens mundialmente imposibles de 19642; se adaptó la bandeja espacial para informar sin convertirlos en postes válidos. Datos/IDs/geometría real permanecen ignorados por Git.

Correspondencia por mapa de ID acreditado o coincidencia/vecindad como propuesta, con tolerancia explícita; se sugieren 20 m solo para diagnóstico, pendiente de validar por owner. Polígonos visuales, proximidad y los tres anillos declarados no autorizan conexiones. Propuestas siempre NO_CONFIRMADA.

Entrada topologia_confirmada.csv exige IDs POSTE admitidos, ruta, tramo, clase, evidencia, responsable, fecha y CONFIRMADA. Consolida arista física no dirigida una vez, preservando sus asociaciones. Grafo permite ciclos/bifurcaciones/desconexiones, extrema candidatos y B06 solo alerta. Sin entrada humana: SOLO_PUNTOS_PRELIMINAR. No se confirman aristas reales con esta entrega.

Estado software COMPLETADO_TECNICO; evidencia de conexiones PENDIENTE_EVIDENCIA. Pruebas sintéticas de ZIP/XML hostil, geometría, bifurcación/ciclo, duplicado físico, desconexiones, cajas no conectoras y ausencia de autoridad; más regresión original intacta. Controles físicos CAD siguen separados.
