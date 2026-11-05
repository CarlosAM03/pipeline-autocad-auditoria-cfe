# Preparación del Proceso 1 CFE / DATRA

Implementación local Python >=3.10. No genera ni ejecuta CAD. ADR-000 gobierna las reglas; esquemas auxiliares implementados como **PROPUESTA P-09**. Todas las corridas quedan PRELIMINAR hasta definición de liberación P-04.

Extensión **0.2.0 / CP-01**: se genera `00_elementos_unificados.csv` con los prevalentes identificados, incluso con geografía y CRS pendientes. Cada fila distingue `estado_preparacion=IDENTIFICADO`, admisión geográfica y `apto_csv_01`; deduplicar no aprueba dibujo. Se conservan los contratos de 01/02 y reportes. Contrato propuesto, flujo y conteos: [EXTENSION_ETL_UNIFICADO.md](Codex/01_Implementacion_Proceso1/EXTENSION_ETL_UNIFICADO.md). Auditoría de funciones JS y contraste 533/965: [AUDITORIA_JS_HISTORICOS.md](Codex/01_Implementacion_Proceso1/AUDITORIA_JS_HISTORICOS.md).

| Checkpoint funcional | Resultado / estado |
|---|---|
| CP-01 | CSV 00 implementado, visible sin P-03/P-06; sin inferir topología. |
| CP-02 | CSV 01 conserva admisión P-03; CSV 02 conserva gate P-06. Probado sintéticamente, bloqueado para validación real pendiente. |
| CP-03 | Futuro 01_configurar_plano.scr; no implementado. |
| CP-04 | Futuro 02_dibujar_auditoria.scr; no implementado. |

Desde la raíz del repositorio, PowerShell:

```powershell
python -m venv AuditoriaCFE/.venv
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip install -r AuditoriaCFE/requirements.txt
& ./AuditoriaCFE/.venv/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --help
```

En esta extensión el entorno `.venv` preexistente apunta a un Python 3.11 de WindowsApps inaccesible. Se conservó intacto y se verificó en un entorno aislado adicional, ignorado por Git:

```powershell
& 'C:/Users/Carl0/AppData/Local/Programs/Thonny/python.exe' -m venv AuditoriaCFE/.venv-cp01
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe -m pip install -r AuditoriaCFE/requirements.txt
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe -m compileall -q AuditoriaCFE/src AuditoriaCFE/tests AuditoriaCFE/preparar_auditoria.py
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe -m pip check
```

La suite ampliada tiene 43 pruebas (29 originales intactas + 9 de unificación + 5 de JS). Solo las cinco de auditoría JS necesitan Node.js en PATH y los históricos exactos; no es dependencia del ETL. La auditoría ejecuta funciones sobre copias temporales sin MAIN ni escrituras JS, nunca genera SCR ni ejecuta AutoCAD. Si falta Node o histórico se marca omisión, no aprobación simulada. La prueba de compatibilidad de reportes lee `reporting.py` del commit `7baa82c` mediante `git show`; necesita ese historial local.

Si `python` es un alias de Windows inaccesible, usar la ruta explícita al intérprete instalado. En esta máquina se utilizó `C:/Users/Carl0/AppData/Local/Programs/Thonny/python.exe` para crear el entorno. La extracción y pruebas sin proyección usan biblioteca estándar. `pyproj` es necesario para las pruebas geodésicas obligatorias, proyección acreditada y cercanía optativa. No requiere Excel, openpyxl, pandas, Pillow ni AutoCAD.

## Operación

1. Crear `AuditoriaCFE/auditorias/<nombre>/entrada/`. El operador coloca allí los XLSX originales de esa auditoría; nunca usar el histórico como destino de escrituras.
2. Copiar `configuracion.ejemplo.json` a `auditorias/<nombre>/configuracion.json`. Ajustar `auditoria` y **todos** los nombres relativos en `fuentes_en_orden`, con separador `/`. El orden es autoridad explícita, sin fechas de modificación. Si hay varias hojas, `hojas_por_fuente` enumera todas, incluidas vacías, una vez y en orden. Hoja única usa su orden natural. Archivo extra o faltante bloquea la corrida, no se omite silenciosamente.
3. Revisar inventario y pendientes, después ejecutar:

```powershell
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria MiAuditoria --dry-run
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria MiAuditoria
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria MiAuditoria --verificar-salida
# Selección interactiva de carpetas con entrada/:
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py
```

`--dry-run` muestra cantidad/lista, precedencia, configuración y pendientes sin abrir celdas ni escribir. No sustituye la validación de las hojas al ejecutar. Código de salida: 0 ejecución técnica completada (puede ser PRELIMINAR), 2 error de configuración/lectura, 130 interrupción. Un XLS/XLSM/XLSB o archivo temporal de Excel bloquea con diagnóstico explícito.

## Configuración y decisiones

- Rutas/subrutas se preservan literalmente, incluso espacios finales, tilde, coma o salto de línea. No existe tabla de equivalencias de nombres aprobada. Tipos conocidos se normalizan a POSTE, CAJA_EMP, EXCEDENTE; Registro es FUERA_ALCANCE antes de revisar coordenadas.
- Coordenadas: decimal exacto con hemisferios, sin redondeo ni inserción de dígitos. Parser interpreta N/S/E/W; S/E se reportan REVISAR porque el contrato exportable actual corresponde a N/W. Admite espacios variables, ausencia de espacio entre N y W y símbolo °. Conserva escala del prevalente; clave de identidad elimina solo ceros decimales redundantes. La identidad física se separa de la conectividad.
- Primaria válida prevalece sobre auxiliares y registra discrepancia sin inventar tolerancia. Recuperación exige pares auxiliares interpretables, concordantes exactamente, sin cachés de fórmulas no acreditados ni magnitudes imposibles. Tokens primarios interpretables deben concordar. Coordenada mundialmente imposible nunca se repara automáticamente. Los valores originales y fórmulas permanecen en linaje.
- `geografia_permitida=null`: P-03 pendiente; componentes mundialmente interpretables se deduplican y quedan REVISAR; **no entran** al CSV dibujable. Para habilitar admisión local se exige objeto con `lat_min,lat_max,lon_min,lon_max,aprobada:true,evidencia`. Los límites son aportados por el responsable, no calculados por el programa. El rectángulo es una capacidad técnica; no acredita cobertura completa ni reemplaza un perímetro administrativo. Fuera del rectángulo: REVISAR sin corrección ni exclusión por distancia. No se aprueba automáticamente la ventana exploratoria del diagnóstico.
- `ids_confiables`: lista de `{archivo,hoja,fila,id,evidencia}`. No se presume que Numero sea un ID. Solo cajas con distintos IDs acreditados se separan dentro de una coordenada idéntica; ocurrencia sin ID ante varios equipos queda REVISAR. ID en varias posiciones/tipos queda en conflicto. No se acepta referencia inexistente.
- Excepción de Canal 12: `excepciones_cabecera: {"nombre.xlsx":{"Hoja1":"F3_D_VACIA"}}`. Requiere estructura F3 comprobada por encabezados; no adivina columnas de hojas desconocidas.
- `maestro_informativo`: `{archivo,fecha,hojas?,excepciones_cabecera?}`. CSV estricto de tres columnas o XLSX de familias reconocidas; ruta relativa a la auditoría o absoluta **explícita**, lectura separada después de unificación. Comparación exacta tipo/coordenada; no excluye componentes del plano individual. Errores de referencia quedan detallados en manifiesto y hacen indeterminada una ausencia.
- `baseline_historica`: igual referencia, añadiendo `auditoria` igual a la carpeta seleccionada. CSV sin cabecera solo con `sin_cabecera:true`. Ausencia de baseline = NO_DETERMINADO. Baseline con errores permite acreditar coincidencias, pero no declarar NUEVO por ausencia. La fecha declarada conserva la responsabilidad y evidencia del operador.
- `cercanos_m`: umbral diagnóstico explícito opcional. Reporta pares de igual tipo por distancia geodésica WGS84 sin fusionar ni conectar. Sin umbral, el manifiesto informa CERCANIA_NO_EVALUADA. El cero exacto corresponde a identidad/ID, no a cercanía.
- `crs_validado:false`: no produce 02. Para habilitar: `crs_candidato` aceptado y `evidencia_crs` con `archivo` de evidencia existente, `aprobado_por,fecha,crs,unidades:"m",tolerancia_m,controles`. Controles: al menos dos posiciones y destinos diferentes, cada uno con `id,latitud,longitud,este_m,norte_m`. Se verifican residuales con la tolerancia suministrada; no se calcula una compensación. Fallo de controles/dependencia/transformación bloquea solo el proyectado y conserva ETL. Una declaración JSON no sustituye la inspección y aprobación humana del CAD.

La proyección usa `Transformer.from_crs(..., always_xy=True)` y `errcheck=True`, conforme a la [documentación oficial de pyproj](https://pyproj4.github.io/pyproj/stable/api/transformer.html). No se reutiliza el algoritmo JS ni su desplazamiento.

## Productos y consumo

En `auditorias/<nombre>/salida/`: `01_elementos_normalizados.csv` (tres columnas exactas UTF-8 sin BOM, coma/CRLF), `summary.csv`, `linaje_y_calidad.jsonl`, `reporte_incidencias.csv`, `asociaciones_elemento_ruta.csv`, `resumen_conteos.csv`, `topologia_propuesta.csv` (solo cabecera), `perfiles_hojas.jsonl`, `filas_no_operativas.jsonl`, `coordenadas_cercanas.csv` y, únicamente con CRS acreditado y controles correctos, `02_elementos_proyectados.csv`.

Además se genera `00_elementos_unificados.csv`, con una fila por prevalente identificable en el mismo ETL. No incluye rechazos, exclusiones ni ambigüedades sin identidad, que permanecen en los reportes. Sin perímetro los grupos identificados aparecen en 00 como pendientes, aunque 01 contenga solo cabecera. No usa el maestro ni cercanía como filtros. `filas_csv_00`, `filas_csv_01`, `filas_csv_02` y `csv_02_generado` se reconcilian con los productos y hashes. Las métricas anteriores se conservan con sus valores; las nuevas separan grupos pendientes de revisiones sin identidad.

El manifiesto activo está en `auditorias/<nombre>/manifiesto_ejecucion.json` y su archivo por hash en `manifiestos/<ejecucion_id>.json`, **fuera de entrada/salida por AGENTS.md**. Contiene hashes de cada fuente/artefacto/configuración/código, versiones Python/pyproj/PROJ, conteos, decisiones, controles y referencias. No contiene reloj variable: repetir entradas, configuración y versión produce iguales bytes, incluido manifiesto. Cambiar de intérprete/dependencia cambia la identidad de ejecución; no cambia deliberadamente el dato geográfico.

Cada ocurrencia operativa tiene un estado terminal y linaje exacto. Un duplicado puede apuntar a un prevalente REVISAR: se identifica el grupo pero no se habilita dibujo. `unicos_identificados` cuenta esos grupos; `unicos_exportables=VALIDO=POSTE+CAJA_EMP+EXCEDENTE`. Los rechazados/fuera de alcance permanecen individualmente trazables. `summary` contiene un caso por prevalente o incidente no agrupable; las asociaciones conservan cada ocurrencia y ruta, incluidas las pendientes.

La publicación usa staging y cambio de directorio bajo bloqueo del SO. Las ejecuciones concurrentes de una auditoría se rechazan. Ante una interrupción entre renombrados, la siguiente ejecución restaura la carpeta anterior si falta salida. Un error antes de publicación no modifica la salida previa. El manifiesto activo se actualiza al final: si el proceso muere en esa ventana, los hashes del activo no coinciden y **no se debe consumir el lote**; reejecutar restablece publicación. Ejecutar siempre `--verificar-salida` antes de integrar con otro proceso. Un conjunto íntegro sigue siendo PRELIMINAR, no aprobación de calidad/CAD. Los errores producen manifiesto `fallo_*.json` cuando existe auditoría válida; un dry-run nunca escribe.

Los temporales se limitan a `auditorias/<nombre>/temporales/`; la lectura OOXML mantiene una fila y sharedStrings con límite de 16 MiB XML. El conjunto de ocurrencias reales, reportes y referencias ocupa memoria proporcional a registros útiles, no a fotografías ni al área formateada. SharedStrings superior al límite falla explícitamente; soporte indexado de tamaños mayores es una mejora futura.

## Regresión histórica solo lectura

Las pruebas integradas leen las nueve rutas exactas documentadas bajo `Auditorias-20261104T035633Z-1-001/postes`, comprueban sus hashes diagnósticos y los dos CSV históricos. Si esos originales faltan, la clase se marca OMITIDA y se informa como no ejecutada. No se buscan fuentes alternativas ni se extraen respaldos.

Para generar reportes revisables de los históricos, se incluyen configuraciones **de prueba**. Su precedencia y referencias no son decisiones operativas aprobadas:

```powershell
$historicoMirador = 'Auditorias-20261104T035633Z-1-001/postes/CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador'
$historicoOtay = 'Auditorias-20261104T035633Z-1-001/postes/CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido'
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Prueba-Historica-Mirador --entrada-prueba $historicoMirador
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Prueba-Historica-Otay --entrada-prueba $historicoOtay
```

El modo PRUEBA registra la raíz externa explícita y no escribe allí. Cada inventario debe coincidir íntegramente con la lista declarada. Mirador incluye los 551 de la reconstrucción más la copia de 181 para probar versiones; Otay incluye 969. Sin geografía acreditada los dos CSV mínimos contienen solo encabezado, mientras linaje, identidad, comparaciones y conteos siguen disponibles. No se trata de resultados cartográficos validados.

CP-01 hace visible esa identidad en 00: Mirador tiene 494 filas y Otay 749; no cambia su estado geográfico. La demo tiene 5 grupos en 00, de los que 4 son admitidos en 01 y 02. Para repetir la integración y verificar dos corridas con los mismos bytes:

```powershell
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe AuditoriaCFE/tests/validar_extension_local.py
& ./AuditoriaCFE/.venv-cp01/Scripts/python.exe AuditoriaCFE/tests/audit_js_support.py
```

`validar_extension_local.py` actualiza exclusivamente las tres auditorías de prueba conocidas, verifica integridad antes de reemplazar el lote y no regenera entradas ni configuraciones. `--comparar-anterior` añade comparación contra el snapshot local previo a esta extensión, no versionado. No utilizar ese modo si falta el snapshot.

Para revisar salidas completas sin usar datos de campo:

```powershell
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/tests/crear_demo.py
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Demo-Sintetica --verificar-salida
```

Crea 8 ocurrencias sintéticas, 4 exportables y sus 4 proyecciones; conserva 1 duplicado, 1 fuera de alcance, 1 rechazado y 1 revisión. La evidencia `CONTROLES_SINTETICOS.txt` y su perímetro pertenecen únicamente al fixture, no al mapa CAD real.
