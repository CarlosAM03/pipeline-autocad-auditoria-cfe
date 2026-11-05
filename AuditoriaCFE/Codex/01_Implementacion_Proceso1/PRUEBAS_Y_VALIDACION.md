# Pruebas y validación — Proceso 1

Fecha: 2026-11-04. **Resultado final: 29 pruebas ejecutadas, 29 aprobadas, 0 fallos y 0 omisiones.** No es aprobación geográfica, de topología ni de CAD.

## Comandos ejecutados y resultado

Desde la raíz del repositorio:

```powershell
& ./AuditoriaCFE/.venv/Scripts/python.exe -m unittest discover -s AuditoriaCFE/tests -v
```

Última ejecución completa: `Ran 29 tests in 43.724s — OK`. Una ejecución anterior completa también pasó las 29 en 32.787s. Las duraciones dependen de carga y almacenamiento; no se promete ese tiempo como SLA.

```powershell
& ./AuditoriaCFE/.venv/Scripts/python.exe -m compileall -q AuditoriaCFE/src AuditoriaCFE/tests AuditoriaCFE/preparar_auditoria.py
& ./AuditoriaCFE/.venv/Scripts/python.exe -m pip check
git diff --check
git rev-parse HEAD
git rev-parse 'checkpoint/pre-codex-proceso1^{commit}'
```

Compilación sin errores; `No broken requirements found`; diff de archivos rastreados sin errores de whitespace; HEAD y commit del tag permanecen `33364c1aa2c94a751857c4d106ee826d8af17ac5`. No se ejecutó un linter ni se afirma cobertura porcentual.

## Matriz de pruebas automatizadas

Los nombres completos están en `tests/test_proceso1.py` (25 métodos) y `tests/test_historico.py` (4 métodos). Los subtests ejercitan variantes adicionales sin inflar el conteo de métodos.

| Control ejecutado | Evidencia / resultado |
|---|---|
| Cuatro familias | F1–F4 detectadas por estructura, nombres de archivo arbitrarios. Foto corrupta ficticia nunca abierta; ZipFile.open monitorizado. |
| Ocultas/auxiliares/vacías | Fila oculta leída, fila solo J explicada, hoja vacía perfilada. Hoja múltiple sin orden falla; con orden explícito prevalece la primera. |
| Canal 12 sin D1 | Falla sin excepción explícita y procesa con F3_D_VACIA. |
| SharedStrings/cachés/fórmulas | Strings e inlineStrings, metadatos de fórmula compartida, caché ausente contado, errores de auxiliares preservados. SharedStrings XML >16 MiB falla explícitamente. |
| Gran formato | Fixture con **1,048,576 filas XML reales** y dimensión A1:XFD1048576: extrae una ocurrencia, sin rectángulo Excel. Último pico `tracemalloc`: **522,967 bytes**. Es memoria Python del lector, no RSS ni memoria total del proceso. |
| Coordenadas | Espacio doble, sin espacio, símbolos °, N/W minúsculas, Decimal con más de 28 decimales; no redondeo por contexto. No detectado, B, W ausente, signo contradictorio, coma decimal, exponentes y mundo imposible se rechazan; S/E se interpretan y quedan a revisión en salida. |
| Auxiliares | Recuperación inequívoca registrada; conflicto entre pares, diferencia con componente primario, enteros sin decimal y cachés no acreditados impiden recuperación. Texto válido prevalece aunque auxiliar sea imposible. |
| Alcance/geografía | Registro FUERA_ALCANCE aun con coordenada mala, tipo desconocido/ruta vacía/remoto REVISAR. Sin perímetro no exporta, pero deduplica grupos y conserva linaje. |
| Identidad exacta | Duplicado entre archivos/rutas, mismo punto con tipo diferente, diferencia de decimales extrema y cercanía sin fusión. Asociaciones mantienen todas las ocurrencias. |
| Precedencia | Lista z.xlsx antes de a.xlsx vence a orden lexicográfico; cambiar mtime no altera bytes; invertir lista cambia prevalente. Config sin lista/completa o con fuente ajena falla. |
| IDs | Dos cajas con ID/evidencia diferente permanecen separadas; repetición de ID se deduplica; ocurrencia sin ID ante varios equipos y mismo ID en otras posiciones quedan REVISAR. Numero no se usa como ID. |
| Comparaciones | Maestro informativo no filtra. Sin baseline NO_DETERMINADO. Baseline completa acredita NUEVO/EXISTENTE; errores en baseline impiden declarar NUEVO por ausencia. |
| Contrato y conteos | Tres columnas exactas, UTF-8 sin BOM, escape de comas/comillas/saltos de línea, reconciliación de estados y clases, un linaje por ocurrencia, duplicados con prevalente real. Hash alterado se detecta. |
| CRS | Sin aprobación/evidencia no existe 02. Fixture con dos controles funciona; residual +11.5 m, control único o unidades ft bloquean únicamente proyección. Rerun bloqueada retira CSV proyectado anterior al reemplazar lote. |
| Referencia independiente geodésica | En meridiano central UTM 11, Este=500000; Norte se compara contra integral del radio de curvatura meridiano WGS84 por Simpson, independiente de pyproj. Tolerancia de aserción: 0.0001 m. |
| Topología | Propuesta vacía, jamás aristas confirmadas. Cercanía es reporte REVISAR_NO_FUSIONAR, sin conexiones. |
| CLI | Selección interactiva simulada, argumento no interactivo y proceso CLI real. Dry-run no escribe. Libro corrupto y configuración inválida dan error no cero explícito. |
| Integridad/interrupción | Fuente cambiada durante lectura impide publicación. Error de esquema conserva salida anterior. KeyboardInterrupt durante rename revierte; estado simulado de caída entre renames se recupera. Bloqueo concurrente rechazado. No se hizo prueba física de apagado ni kill en cada instrucción. |
| Reproducibilidad | Fixtures comparan bytes de todos los productos y contenido de manifiestos entre corridas. Mirador y Otay reales también se ejecutaron dos veces consecutivas con comparación byte a byte y verificación de hashes. |

## Regresión readonly real

Se leyeron exclusivamente las nueve rutas exactas del diagnóstico y los dos CSV. **9/9 hashes XLSX coinciden con inventario diagnóstico**, se verificaron antes y después; ambos CSV coinciden con sus hashes diagnósticos. No se escribieron, repararon ni ejecutaron originales. No se extrajeron respaldos.

| Fuente | Candidatos extraídos |
|---|---:|
| FLO-OTAY-BOMBEROS | 494 |
| Natura | 507 (14 rutas) |
| Copy STD | 181 (44 filas ocultas y segunda hoja vacía) |
| Canal 12 | 347 |
| STD | 204 |
| FLO-OTAY final | 622 |
| Protección Civil | 303 |
| Vía Rápida | 44 |
| Postes_CFE | 4,341 |
| **Total** | **7,043** |

También coinciden **1,058,886 filas XML**, **6,175 fórmulas**, cuatro familias y una hoja vacía. La clasificación cruda de coordenadas da 7,020 interpretables mundialmente, 10 imposibles y 13 no interpretables; rango mundial no prueba ubicación local.

- Mirador: concatenación STD+Canal = **551/551 triples literales y en secuencia** tras omitir únicamente las tres filas CSV completamente vacías. El CSV carece de cabecera y contiene BOM. Repeticiones literales adicionales: **56**. P-11 frente a la cifra AS-IS 58 no se declara cerrado.
- Otay: Vía Rápida+FLO+Protección Civil = **969 posiciones**; **968 literales** y una diferencia de espacio doble en posición 731. Colapsando solo espacios de coordenadas: **969/969**. Repeticiones literales históricas: **218**.
- Diagnóstico nuevo de identidad exacta, sin aprobar ámbito: Mirador tiene 494 grupos interpretables y 56 repeticiones, con 1 coordenada imposible; Otay tiene 749 grupos, 217 repeticiones, 2 imposibles y 1 Registro fuera de alcance. El duplicado de coordenada imposible de Otay explica la diferencia 218→217 al separar rechazos. No son conteos de dibujables validados.

## Corridas CLI de reportes realmente ejecutadas

```powershell
$historicoMirador = 'Auditorias-20261104T035633Z-1-001/postes/CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Mirador'
$historicoOtay = 'Auditorias-20261104T035633Z-1-001/postes/CFE POSTES OTAY-FLORIDO_STD PLAYAS MIRADOR/Otay - Florido'
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Prueba-Historica-Mirador --entrada-prueba $historicoMirador
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Prueba-Historica-Otay --entrada-prueba $historicoOtay
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/tests/crear_demo.py
& ./AuditoriaCFE/.venv/Scripts/python.exe AuditoriaCFE/preparar_auditoria.py --auditoria Demo-Sintetica --verificar-salida
```

Después de los últimos ajustes de código, se ejecutó dos veces `run()` sobre cada raíz histórica con las mismas configuraciones, comparando `read_bytes()` de todos los artefactos y el manifiesto completo. Se llamó `verify()` sobre ambos activos: **idénticos y íntegros**. Identidades finales archivadas:

- Mirador: `10352c47fdee56faf1bd638a0c970339f45c802e6dd9864f1262e7142f0fda02`.
- Otay: `98e9cbc28db194fa9dcb0e6c5b14850f82f0425d07d501647052a317780e4717`.

La configuración Mirador de prueba incluye **la copia de 181**, de modo que sus reportes tienen 732 ocurrencias (494 REVISAR +236 DUPLICADO +2 RECHAZADO). La regresión de 551 se prueba separadamente sin la copia. Otay: 969=749 REVISAR+217 DUPLICADO+2 RECHAZADO+1 FUERA_ALCANCE. Ambos tienen CSV mínimo solo con cabecera y no producen 02: P-03/P-06 siguen abiertos.

Demo: 8=4 VALIDO+1 DUPLICADO+1 REVISAR+1 RECHAZADO+1 FUERA_ALCANCE; 4 proyectados con controles sintéticos; cardinalidad 1:1. Verificación activa ejecutada con resultado Integridad OK. Una generación nueva de fixture puede cambiar los bytes ZIP de entrada (timestamps ZIP); repetir corrida sobre las mismas entradas conserva los productos. No se confunde regenerar un XLSX con repetir una misma entrada.

## Fallos encontrados y resueltos durante la verificación

1. Alias Windows python inaccesible: uso explícito de intérprete existente y entorno virtual local.
2. Red sandbox bloqueó primera descarga pyproj: instalación completada tras revisión automática autorizada; geodesia sí se ejecutó.
3. Primera expectativa de Norte del test era incorrecta (67.154 m distinta). Se sustituyó por referencia independiente de integral meridiana; no se alteró proyección para forzar la cifra.
4. Primer lector de referencia histórica del test omitía líneas sin campos, pero retenía tres triples vacíos `,,` de Mirador. Corregido el filtro de referencia; extracción histórica intacta.
5. Se reforzaron manifiestos de fallo, bloqueo por SO, trazabilidad de duplicados con prevalente REVISAR, archivo activo y rechazo de alias de escritura. Se repitió suite completa tras ajustes: 29 OK.

**Fallos automatizados sin resolver: ninguno observado.** Limitaciones de aceptación productiva y mejoras están clasificadas en PENDIENTES_PARA_REVISION.md. No se ejecutó prueba CAD ni validación de perímetro/control real, y no se declaran exitosas.
