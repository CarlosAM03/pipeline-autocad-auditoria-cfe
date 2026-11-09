# Promoción y custodia de la plantilla

La candidata A4.2 original, con SHA-256 62abf37880f95c0e895cfa0f6e3ef95fb7e620e4560586fc38cc72eda3901728, se enriqueció sobre copia. La ruta contractual es AuditoriaCFE/recursos/PlantillaMarcoDatraMapaTijuana.dwg. El respaldo privado conserva los 22,950,864 bytes originales y el SHA-256 8386c4c6d6bd05cb95a4d226fefc28e3c85276f149afde8abcfaa92c877f7a8a. El DWG enriquecido tiene 23,113,177 bytes. La DWT se creó mediante SAVEAS nativo y se reabrió desde una segunda carpeta con ambos PNG.

El control de promoción comprueba las regresiones, el fixture, el hash anterior y los hashes de las configuraciones antes de reemplazar. El intercambio usa un archivo temporal en el mismo directorio. Se vuelve a abrir una copia obtenida de la ruta activa y se ejecuta allí un fixture de punta a punta. Las tres configuraciones autorizadas usan nuevas bases bajo entrada/cad_A4_2_1 y mantienen los demás campos previos.

Para revertir, verificar primero que la plantilla activa y las configuraciones correspondan a los hashes posteriores del registro. Recuperar la base y los tres JSON desde sus respaldos mediante sustitución atómica, conservando cualquier edición posterior para revisión. Las copias nuevas de entrada pueden quedar archivadas.
