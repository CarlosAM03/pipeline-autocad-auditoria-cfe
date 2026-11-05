# Operación reproducible del piloto

1. Instalar Python >=3.10 y requirements.txt en un entorno local. El ejemplo
   usa `python`; seleccionar el ejecutable de ese entorno.
2. Disponer históricos locales autorizados y recursos DATRA, ignorados por Git.
   Cada auditoría tiene `entrada/`, `configuracion.json` y `salida/`. No se
   ofrece un selector Windows genérico: el menú enumera carpetas existentes.
3. Declarar precedencia de los tres XLSX de Mirador y excepciones de hojas,
   `pipeline_integral: true`, `schema_02: 2`, ámbito null y CRS no validado si
   falta evidencia. Base DWG copiada en entrada y `cad.copia: true`. Para este
   piloto se usa `cad.copia_nombre: piloto_PR1_Mirador_v1.dwg`, distinta de la
   copia anterior del operador. Nunca reutilizar ese nombre para otro ensayo
   si el responsable ya editó ese DWG; elegir un nombre nuevo.
4. Ejecutar desde la raíz:

   ```powershell
   python AuditoriaCFE/preparar_auditoria.py --auditoria Mirador --preparar-entradas --diagnostico
   python AuditoriaCFE/preparar_auditoria.py --auditoria Mirador --verificar-paquete
   ```

   Para selección por menú, omitir `--auditoria Mirador`; elegir el número de
   Mirador antes de la preparación. No usar batch para este piloto.
5. Abrir exclusivamente la copia indicada por reporte_validacion_cad.json en
   AutoCAD 2026 inglés. Mantener juntos los dos SCR y los dos LISP emitidos en
   salida. Ejecutar `SCRIPT` con `01_configurar_plano.scr`, luego con
   `02_dibujar_auditoria.scr`. El compilador carga los LISP; no APPLOAD manual.
   Las rutas del paquete están vinculadas al entorno de compilación: al cambiar
   carpeta, volver a compilar; no editar artefactos sin actualizar manifiesto.
6. Repetir SCR02 para verificar idempotencia; comprobar 493 INSERTs propios,
   cero aristas y atributos 414/20/59 en la tabla derecha. Guardar la copia,
   cerrar y reabrir. Inspeccionar Model/WCS, A1 y referencias/fuentes.
7. Imprimir únicamente DATRA_A1 con DWG To PDF.pc3 y PDFSHX=0. La configuración
   evita comentarios SHX, conserva los glifos visibles y mantiene PDF vectorial.
   La configuración de PDFSHX persiste en AutoCAD; revisarla al terminar.
8. El driver opt-in `herramientas/ensayo_nativo.py` automatiza esas pruebas
   sobre la copia declarada en Core Console y genera un acta de hashes.
   `--verificar-evidencia-cad` comprueba esa acta independientemente del lote.
   Si el operador edita después el DWG, la evidencia queda obsoleta hasta
   repetir el ensayo; el paquete reproducible puede seguir íntegro.
9. Revisar XLSX y PDF, solapamientos, todos los paneles y licencias de recursos.
   No enviar originales ni el KMZ a revisores. El ZIP privado contiene solo
   evidencia derivada seleccionada; el owner decide con quién compartirlo.

P03/P05/P06/P07/P08/P04 continúan pendientes. El modo diagnóstico no acredita
CRS ni conexiones y nunca constituye plano FINAL. Los controles analíticos y
las cinco aristas del fixture son ficticios; no transferirlos a Mirador.
