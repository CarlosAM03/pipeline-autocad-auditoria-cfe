# CRS aplicado

El ETL interpreta longitud y latitud en grados WGS84 y aplica pyproj con origen EPSG:4326 y destino candidato EPSG:32611 mediante always_xy. Las columnas este_m y norte_m de 02_DIAGNOSTICO_NO_VERIFICADO.csv se insertan directamente en Model Space, en metros del candidato y sin ajuste local añadido. INSUNITS=4 y UCS mundial describen el archivo y no acreditan la cartografía. La escala papel/modelo sigue el plan aprobado.

P-06 requiere dos controles distintos con latitud/longitud y valores WCS medidos en la base, tolerancia en metros aprobada, CRS propuesto, archivo de evidencia, responsable y fecha. La salida productiva 02 permanece ausente. El encabezado del cajetín de revisión es CRS APLICADO y el valor identifica el candidato y el carácter diagnóstico.
