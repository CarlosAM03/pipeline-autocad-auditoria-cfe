# Oráculo de compatibilidad de reportes

`reporting_7baa82c.py` es una copia congelada, sin modificaciones, de
`AuditoriaCFE/src/auditoriacfe/reporting.py` del commit
`7baa82c231166681d0928013551cf29c2e2de298`.

SHA-256 del texto UTF-8 con finales LF:
`443e5eab1cd9f86651f381721f8f38cc7eac2512d5a52230c429765428d2c4e8`.

La prueba comprueba este hash y compara los bytes de los productos comunes
del reportador anterior con el actual, conservando la excepción de conteos
aditivos. La copia pertenece exclusivamente a las pruebas: no se importa desde
producción, no se llama a su publicación ni se usa para procesar datos operativos.

No regenerar esta referencia desde el código actual para hacer pasar una
regresión. Un cambio del oráculo requiere revisión explícita de procedencia,
hash y expectativas. La ejecución normal no necesita Git, acceso a la red ni
el objeto del commit original; funciona en clones superficiales o exportaciones
sin `.git`. `read_text` normaliza CRLF a LF para conservar el hash en Windows.
