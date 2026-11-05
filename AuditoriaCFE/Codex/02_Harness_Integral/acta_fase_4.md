# Fase 4 — Compilador de configuración DATRA

Estado de ingeniería: COMPLETADO_TECNICO. Aceptación de plantilla: PENDIENTE_EVIDENCIA.

Se implementó `cad.py` y `cad_runtime.lsp`, empaquetados y cubiertos por hashes del lote. SCR01 crea capas y tres bloques esquemáticos, estilo, layout A1 y dispositivo PDF. Conserva mapa y contenido heredado. No inserta componentes ni cartografía adicional; solo cambia INSUNITS a metros si la configuración declara la unidad verificada. Esto no acredita la escala real del mapa.

Antes de modificar un dibujo, el runtime compara su ruta completa con la copia específica preparada. Los resultados nativos quedan en `salida/resultados_cad/`, carpeta mutable preservada al regenerar el lote, separada de los artefactos reproducibles del compilador. El original en entrada y recursos no se sobreescribe. El segundo SCR queda bloqueado explícitamente cuando falta proyección habilitada.

Los dos SCR cargan automáticamente el mismo LISP. `DATRACONTROLES` permite al operador capturar dos puntos en WCS, sin aprobarlos automáticamente. `datra:inspect` inventaría espacios, layouts, unidades, UCS, bloques, capas y referencias en un archivo de evidencia.

AutoCAD 2026 estaba disponible. La observación mostró la base DATRA abierta y paneles con esquema, logo, mapa, Model/Layout1/DATRA_A1. No se guardó ni se ejecutó código en ese documento: era un dibujo del usuario con modificaciones. Los intentos de abrir una copia detectaron entrada manual y finalmente Computer Use fue detenido por Escape. No se reanudó el control de GUI. Por tanto, no se acredita ejecución de SCR, inspección interna completa, DWT nativa ni PDF A1.

La DWT propuesta conserva el nombre `Plantilla_Auditoria_CFE_Tijuana.dwt`; debe obtenerse con SAVEAS nativo tras la revisión descrita en el checklist. No se generó una falsa DWT por renombrado.

Pruebas: ocho casos nuevos de compilación, límites, custodia de copia, idempotencia, dos SCR, aristas y A1. Primer ensayo: cuatro errores en serialización del resumen por saltos de línea; corregido a texto plano. Resultado definitivo de suite completa se registra en fase 6.

Referencia técnica: [Autodesk StandardScale](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-ActiveX-Reference/files/GUID-E8D9D4F5-24C1-4C89-924E-DF57C7F0CF5F.htm). El chequeo de paréntesis es estático; no sustituye la prueba AutoCAD.
