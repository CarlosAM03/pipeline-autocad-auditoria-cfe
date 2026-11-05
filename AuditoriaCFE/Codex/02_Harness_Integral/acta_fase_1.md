# Fase 1 — CP-01 extendido

Implementados bandeja 00 revisión (14 campos), resoluciones acreditadas por hash/archivo/hoja/fila/valor original, tipologías inequívocas y ámbitos GeoJSON/KML/corredores. Se conservan 00 de 12 columnas y 01 de tres. No se infiere conectividad ni se corrigen dígitos. Una resolución no aprobada permanece sin aplicar; referencias inexistentes o conflictos fallan explícitamente.

Intake crea exclusivamente copias de las fuentes declaradas para Natura, Mirador, Otay-Florido y Tijuana-General, con manifiesto de hashes. Configuraciones y resoluciones reales ignoradas. Se materializa Q24 como exclusiones por ocurrencia, sin borrar XLSX/linaje. Maestro sigue separado e informativo; no se inventa baseline de novedades. Bomberos no se incorpora.

Ámbito aprobado requiere archivo, versión, responsable, evidencia y CRS WGS84; geometría inválida o antimeridiano sin división se rechaza. Bordes exteriores admitidos, huecos respetados; corredor usa buffer métrico local con pyproj y Shapely. No existe todavía ámbito real aprobado: CP-01 COMPLETADO_TECNICO, admisión productiva PENDIENTE_EVIDENCIA.

Pruebas nuevas sintéticas de corrección/exclusión, hash incorrecto, no aprobadas, tipos, polígonos con huecos/bordes, corredor, excepción individual y ámbito inválido. Las 43 anteriores se mantienen. Resultados agregados y SHA de commits se registran en el cierre incremental. Dependencia Shapely 2.1.2 fijada, sin reparación automática mediante buffer(0).
