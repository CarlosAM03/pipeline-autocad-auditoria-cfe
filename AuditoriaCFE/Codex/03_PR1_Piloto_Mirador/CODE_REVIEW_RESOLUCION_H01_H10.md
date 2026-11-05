# Resolución técnica del review independiente PR #1

Referencia auditada: 97731f5. Los datos y evidencias nativas permanecen locales;
el ZIP privado contiene sus hashes y resultados. No se fusiona PR #1.

| Hallazgo | Cambio y verificación | Pendiente |
|---|---|---|
| H01 | Pertenencias elemento→rutas desde todas las ocurrencias de identidades admitidas; ambos extremos POSTE deben pertenecer. Regresión negativa reproducida antes; positivos compartidos y negativos por extremo en test_network_integral | Transferencias distintas de estas pertenencias requieren decisión/evidencia explícita |
| H02 | Selección antes de preparación; bootstrap y maestro reciben lista seleccionada; batch explícito. Regresión antes/después, snapshot sintético y control real sin escrituras en otras auditorías | No hay selector Windows; configuración estructural previa documentada |
| H03 | Fixture ficticio de seis postes, cinco aristas AB/BC/BD/DA/EF, ciclo, rama y dos componentes. Driver nativo comprueba XDATA, longitudes, idempotencia, reapertura y rollback | No acredita conexiones de Mirador ni CRS físico |
| H04 | Inspección nativa de DATRA_CAJETIN_A1: atributos TOTAL_POSTES/TOTAL_CAJAS/TOTAL_EXCEDENTES. Actualización por tag y layout, bloque único, sin segunda tabla de tipos. Falta de correspondencia deja PENDIENTE_AJUSTE_PLANTILLA | Aceptación visual de paneles y cajetín |
| H05 | pipeline_integral booleano independiente de schema_02; compatibilidad explícita de perfiles previos. Tests v1 integral y v2 legado | Migración de cada configuración operativa por responsable |
| H06 | CLI distingue paquete reproducible de acta/resultados CAD mutables. Verificación independiente de hashes nativos ligada a ejecución; prueba de alteración de DWG | Integridad no verifica por sí sola autenticidad de firma ni calidad humana |
| H07 | Original PDF no modificado. Comparación Poppler/PyMuPDF y PDFSHX=0 de nuevas impresiones nativas, sin rasterizar los PDF | Compatibilidad del PDF histórico se conserva como limitación |
| H08 | Valida ambas carpetas sin exigir entradas actuales, restaura anterior íntegra y pone activa inválida en cuarentena. Pruebas de fallo y preservación de trabajo mutable | Corte físico no ensayado; recuperación de trabajo del operador requiere revisión |
| H09 | CI agrega pip check; pruebas negativas de ZIP/KMZ y manifiestos, guardia/staging revisados | Ruff sigue selectivo; guardia por paths no acredita licencias ni hace DLP semántico |
| H10 | README enlaza cierre integral y acta nueva; cortes 79/81 conservados cronológicamente | Ninguna reescritura de historia |

El ensayo nativo detectó además un defecto antes oculto: UNDO informaba un
grupo activo y no retiraba la geometría de una falla simulada. El runtime ahora
comprueba también el indicador explícito de fallo y restaura las entidades
propias mediante diario, incluyendo atributos y viewport anterior. Se ensaya
una falla después de redibujar, no solo una excepción Python. No se afirma una
transacción universal para recursos externos ni configuraciones globales.

La recomendación de agrupar UNDO está en la [documentación Autodesk](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-AutoLISP/files/GUID-4481039B-77DA-4500-AE8B-3D2AD6951115.htm);
el comportamiento efectivo de SCRIPT/Core se comprobó localmente y no se dio
por correcto a partir de esa recomendación.

Normas CSV, ADR y TO-BE intactos. P03, P05, P06, P07, P08 y P04 siguen abiertos.
