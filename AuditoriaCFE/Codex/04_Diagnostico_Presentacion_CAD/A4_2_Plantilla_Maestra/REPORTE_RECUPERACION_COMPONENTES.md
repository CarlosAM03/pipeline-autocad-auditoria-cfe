# Recuperación de componentes

El exportador seleccionó handles de entidades vectoriales por posición y capa dentro de la franja de detalle de Model. Con WBLOCK se crearon cinco dibujos intermedios editables. Se reabrieron, se midieron sus extensiones y se comprobó la ausencia de dependencias externas de geometría. El JSON local enumera cada handle de origen.

Se insertaron cuatro bloques nativos en DATRA_A1, con traslación y escala uniforme para cada panel. Los textos, líderes, líneas y componentes anidados se conservaron editables. El bloque anidado de empalme tenía un nombre presente en la base DATRA. Se renombró en una copia del WBLOCK, previo a la inserción, para que AutoCAD importara su definición histórica sin sustituir ninguna definición DATRA.

El quinto WBLOCK, de cambio de dirección, queda en la biblioteca privada. El rótulo y las referencias PDF identifican un herraje de tensión para cambio de dirección. El panel DATRA de derivación conserva su lugar y muestra un aviso explícito de fuente pendiente. Se conserva íntegra la información histórica del detalle recuperado, con medidas y especificaciones pendientes de validación técnica.

Para reproducir la migración se conservan inventario.py, exportar.py, medir.py, maestra_v2.py, los SCR auxiliares nativos, handles.json y migracion.json bajo el directorio privado A4.2. Estos auxiliares son de construcción de la plantilla. El operador de auditoría sigue usando dos SCR.
