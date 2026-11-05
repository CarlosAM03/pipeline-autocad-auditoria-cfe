# Fase 2 — CP-02 y manifiestos

CSV02 v2 separa ruta_id real (hash ruta-v1 de auditoría+literal) y ruta_nombre. Reader acepta v1 sin cambiar su semántica anterior. Configuración schema_02=1 conserva compatibilidad de los 43 tests; schema_02=2 es la configuración de las nuevas cuatro auditorías y habilita manifiesto canónico dentro de salida. Schema y algoritmos se declaran en manifiesto; 00/01 permanecen intactos.

Migración por lote: verifica el lote anterior, copia historial, prepara activo sin autorreferencia, intercambia directorios con rollback y verifica antes de retirar únicamente JSON antiguos copiados idénticos. Reader reconoce legacy mientras migra. Entradas operativas se hashean y su alteración posterior invalida el paquete. Se prueba interrupción y rechazo de entrada alterada. El fallo Windows de fase1 (49/50 aprobadas, un PermissionError de publicación) motivó reintentos acotados exclusivamente para PermissionError; no se cambió una regla de calidad ni se etiquetó ese ensayo fallido como OK.

El diagnóstico exige opt-in y copia DWG dentro de entrada; produce archivo distinto 02_DIAGNOSTICO_NO_VERIFICADO.csv y no el CSV02 productivo. No habilita un CRS por declarar EPSG o INSUNITS. Para base real faltan dos controles WCS↔WGS84 independientes y tolerancia acreditada: PENDIENTE_EVIDENCIA. Compilación y pruebas avanzan independientemente.
