# AGENTS.md — PipeLineDeAuditoria (DATRA / CFE)

## Alcance y autoridad
- Raíz de ejecución: `C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria` (en otros equipos, resolver la raíz a partir del repositorio; **nunca** buscar carpetas alternativas automáticamente).
- Código y salidas nuevas: **solo** en `AuditoriaCFE/`. Tratar `Auditorias-20261104T035633Z-1-001/` como **histórico inmutable y de solo lectura**. No modificarlo, renombrarlo, descomprimir respaldos ni ejecutar archivos históricos.
- Precedencia para reglas aprobadas: `AuditoriaCFE/Docs/ADRs/ADR-000_Decisiones_Base_Pipeline_Auditorias_CFE.md`, después `AuditoriaCFE/Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.2.md`, luego diagnósticos en `AuditoriaCFE/Codex/00_Diagnostico/`. Si hay contradicción, detener el cambio correspondiente, registrar la discrepancia y consultar al owner.
- No convertir decisiones técnicas propuestas en reglas de negocio aprobadas; explicitar supuestos y controles pendientes P-01 a P-11.

## Fase actualmente autorizada
- Implementar **Proceso 1, preparación de información**, por etapas verificables: 1A XLSX→CSV normalizado y reportes; 1B proyección espacial a CSV **solamente si CRS verificado**, con topología propuesta NO confirmada.
- No crear todavía `.scr`, `.dwg`, `.dwt`, PDF productivo ni ejecutar AutoCAD; son una fase distinta. No escribir ni modificar `recursos/` salvo instrucciones específicas del owner.
- No inferir trayectorias por orden de Excel, proximidad, DFS o filtrado de aislados. Las conexiones solo pueden aparecer en el dibujo si están confirmadas.

## Datos y reproducibilidad
- Procesar únicamente los XLSX contenidos en la `entrada/` de una auditoría seleccionada; la comparación con `Postes_CFE.xlsx` es separada e informativa, solo si su fuente de referencia se declara explícitamente.
- La selección de auditoría debe funcionar por consola y con argumento no interactivo para pruebas. Mostrar previamente la cantidad y lista de XLSX.
- Precedencia de fuentes obligatoria y explícita en configuración para corridas productivas; no usar `mtime`, orden del sistema de archivos ni orden geográfico como autoridad. Orden de hojas/filas determinista.
- Los XLSX pueden contener imágenes masivas y dimensiones XML de un millón de filas: usar extracción secuencial OOXML y lectura de celdas con valor real, sin extraer fotografías, activar macros o cargar imágenes a memoria.
- Normalizar `poste`→`POSTE`, `excedente`→`EXCEDENTE`, `cajadedmpalme`→`CAJA_EMP`. `Registro` es subterráneo: `FUERA_ALCANCE`, no dibujar ni contar como CFE.
- Duplicado dentro de auditoría: mismo tipo canónico y coordenadas normalizadas exactamente iguales, sin redondeo; respetar excepción documentada de identificadores confiables de equipos distintos. Retener cada ocurrencia en linaje; solo un componente prevalente por grupo.
- No corregir dígitos especulativamente; auxiliares N/W solo cuando sean inequívocos y registrar sustitución. Valores mundiales imposibles no entran al CSV dibujable; continuar preliminar con incidencia.
- No confundir coincidencia con maestro con novedad respecto a auditoría previa. Si no hay baseline histórica declarada: `NO_DETERMINADO`.
- CRS objetivo `EPSG:32611` es candidato, no autorización. Sin evidencia CAD de control, no producir `02_elementos_proyectados.csv` como validado; registrar bloqueo. Prohibido compensar manualmente ~11.5 m del algoritmo JS anterior.

## Contratos, pruebas y cambios
- El CSV mínimo debe tener exactamente `Ruta,Elemento de Red,Coordenadas` en ese orden, UTF-8, escapado CSV correcto. Los metadatos extensos van a reportes auxiliares.
- Salidas en `AuditoriaCFE/auditorias/<auditoria>/salida/`; configuraciones, manifiestos y topología confirmada **fuera** de `entrada/` y `salida/`.
- Cada corrida debe producir un manifiesto reproducible de hashes/configuración, conteos reconciliables, summary, linaje e incidencias, aunque una corrida sea PRELIMINAR.
- Pruebas unitarias con fixtures ligeros, pruebas sintéticas de gran dimensión y regresión sobre Mirador/Otay usando histórico solo de lectura. No añadir XLSX pesados ni salidas generadas a Git.
- Antes de terminar: ejecutar pruebas disponibles y presentar archivos cambiados, comandos ejecutados, resultados, limitaciones, decisiones P-xx bloqueantes y propuesta de siguiente checkpoint. No declarar cobertura geográfica ni topológica validada sin evidencia.
- No modificar ADR-000 ni TO-BE v0.2 sin autorización. Una corrección o propuesta puede registrarse en documento separado identificado como **propuesta**.
