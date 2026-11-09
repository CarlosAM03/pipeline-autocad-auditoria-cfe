# Pruebas y regresiones A4.1

La ejecución de entrega usó Python 3.10.11 y `python -m unittest discover -s AuditoriaCFE/tests -v`. Resultado local **96 aprobadas, 0 fallidas, 0 omitidas**, 50,532 s en la última ejecución. Se reactivaron las cuatro pruebas históricas usando las rutas explícitas actuales y los SHA originales del oráculo. Tres pruebas nuevas cubren partición determinista con extremos, parámetros visuales independientes e inclusión de Bomberos con linaje, subruta, índice y dos SCR.

Aprobados `compileall` sobre src/tests/herramientas, `pip check`, `git diff --cached --check` y `verificar_publicacion.py --staged`. El código y documentación sanitizada se publicaron en edbc7131d9f9297c202a504a2f38a5742ef770ef. En el PR #1 completaron con éxito los cuatro jobs Windows/Ubuntu × Python 3.10/3.12 del run 42592235038. Las fuentes privadas y AutoCAD se verificaron localmente.

## Ensayos intermedios

- El primer intento nativo copió títulos de la general a los detalles. Se corrigió preparando los layouts antes de agregar anotaciones.
- El segundo intento duplicó anotaciones en layouts inactivos al repetir SCR02. Se corrigió activando el layout correspondiente antes de borrar sus entidades propias. Los tres lotes finales superaron la comparación.
- El trazado intermedio terminó los PDF por hoja pero quedó detenido en QUIT con cambios de vista en las copias. Se conservaron los archivos y se cerraron los procesos intermedios de forma específica después del último PDF. La ejecución final guardó y cerró las copias.
- El primer validador de trazado final usaba el número de viewport de la sesión activa. Los viewports de layouts inactivos informan número cero tras reabrir. Se corrigió la comprobación para identificar por capa, layout y dimensiones. Se conservaron los PDF y se repitió la verificación sobre los mismos archivos nativos.

Omitidos el ensayo GUI y la impresión física. La simulación de dos perfiles alternativos midió encuadre y cajas en papel. El perfil seleccionado se trazó de forma nativa.
