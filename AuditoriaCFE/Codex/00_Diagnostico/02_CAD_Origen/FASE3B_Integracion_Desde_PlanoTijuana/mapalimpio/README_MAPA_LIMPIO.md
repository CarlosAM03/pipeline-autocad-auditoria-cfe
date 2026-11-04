# Fase 3B — Mapa vectorial Tijuana limpio (DATRA)

**Propósito:** resolver el insumo cartográfico pendiente, independiente del marco A1 empresarial. Esta herramienta limpia visualmente **una copia** de `146468_PLANOTIJUANA.dwg` o de `PlantillaMarcoDatraMapaTijuana.dwg`, conservando líneas viales y geometría útil. No reemplaza ni modifica el generador Python del marco.

## Qué genera y qué no

El archivo `CFE_MAPA_LIMPIO_FASE3B.lsp` **no contiene un mapa nuevo**: aplica una vista cartográfica depurada al DWG existente. Los vectores reales están en tu DWG nativo. El código no borra geometría, no descompone bloques, no modifica coordenadas ni unidades y no guarda automáticamente. Deja los otros textos cartográficos en una capa oculta y separa los nombres de calles como capa opcional.

**Debe ejecutarse en AutoCAD para obtener el DWG resultante**; sin ejecutar ese paso no existe todavía un DWG del mapa limpio ni una DWT limpia aprobada. Esta primera versión prepara una vista depurada del mapa **incorporado a la plantilla**; la extracción del mapa como XREF independiente requiere una verificación adicional del Model Space.

## Ejecución segura

1. Guarda una **copia** de tu actual plantilla: `AuditoriaCFE/recursos/PlantillaMarcoDatraMapaTijuana_TRABAJO.dwg`. Mantén el original como respaldo. Si quieres separar cartografía de marco, también puedes hacer copia de `146468_PLANOTIJUANA.dwg`.
2. En la copia, abre `APPLOAD` y carga `CFE_MAPA_LIMPIO_FASE3B.lsp`.
3. Escribe `CFEMAPA_LIMPIAR`.
4. Elige **`V`** (solo vías, carreteras, banquetas y geometría vial) o **`U`** (vías + manzanas/predios). Para menos saturación, prueba primero `V`.
5. Elige **`N`** para mantener ocultos los nombres de calles (se pueden activar luego). Confirma escribiendo **`SI`** cuando el programa lo solicite.
6. Comprueba `Layout1` y `Model`. Activa nombres con `CFEMAPA_NOMBRES` si deseas conservarlos.
7. Consulta el archivo `*_CFEMAPA_LIMPIEZA.txt`, generado junto al DWG de trabajo. Allí se indican textos tratados y geometría de bloque aún en `layer 0`.
8. Si el resultado es incorrecto, ejecuta `CFEMAPA_RESTAURAR` **en la misma sesión** o cierra sin guardar. Este comando devuelve los textos a sus capas y los estados originales de encendido de capa.
9. Una vez validado el resultado, usa **Save As** para guardar el DWG limpio. Para el primer resultado, **preferimos el mapa incorporado en la plantilla de trabajo**: guarda la copia de `PlantillaMarcoDatraMapaTijuana.dwg` y, después de validar, **Save As → AutoCAD Drawing Template (.dwt)**. Si además necesitas un `Mapa_Tijuana_Vectorial.dwg` aislado para utilizarlo como XREF, **no basta con renombrar el archivo**: hay que comprobar que el Model Space no contenga detalles de marco, cajetín u otras geometrías auxiliares y separarlos selectivamente, sin borrar la cartografía.

## Comandos

| Comando | Acción |
|---|---|
| `CFEMAPA_LIMPIAR` | Limpieza reversible mediante apagado de capas cartográficas secundarias y clasificación de textos en Model y bloques que NO estén usados en Paper Space |
| `CFEMAPA_NOMBRES` | Alterna nombres de calles |
| `CFEMAPA_RESTAURAR` | Restaura la sesión anterior a la limpieza |
| `CFEMAPA_RESUMEN` | Reescribe informe con métricas y capas desactivadas |

## Precauciones

- **No ejecutar directamente sobre archivos de la carpeta histórica** `Auditorias-20261104T035633Z-1-001`; la herramienta intenta impedirlo. El resultado validado debe guardarse en `AuditoriaCFE/recursos`.
- El mapa base conserva `INSUNITS=4` mientras no se verifiquen CRS y dos puntos de control. No convertirlo mecánicamente a metros ni escalar por 1,000. Los dos scripts productivos requieren un CRS CAD probado.
- Algunos bloques del mapa están anidados y sus entidades podrían estar en la **capa 0**, mezcladas con otros elementos. No se puede garantizar la separación semántica de calles y ruidos por capa si comparten `0`. La herramienta avisa cuántas primitivas quedaron bajo esa condición; no las suprime para no borrar calles legítimas. Si el resultado no es suficientemente limpio, **no congelar todavía la DWT**: enviaremos un inventario selectivo de los bloques afectados y diseñaremos una excepción segura.
- Las etiquetas detectadas como calles se clasifican por nombre de capa. Una calle etiquetada por error en `0` quedará oculta; se revisará visualmente.
- Los bloques utilizados por Paper Space (marco/cajetín) se protegen. Los recursos en Model Space que por error se usen como detalles del cajetín pueden requerir revisión visual.
- `CFEMAPA_RESTAURAR` es una reversión **en memoria, en la sesión actual**. Para reversión permanente conserva el DWG original sin modificar. No uses `PURGE`, `OVERKILL` ni `EXPLODE` masivos en esta fase.
- El proceso de visibilidad no reduce necesariamente el tamaño físico del DWG. Es intencional: prioridad a integridad y trazabilidad.

## Qué se considera terminado

- No hay infraestructura, anotaciones arbitrarias ni detalles cartográficos que tapen la red; opcionalmente nombres de calles legibles.
- Marco DATRA, cajetín y disposición A1 se conservan en Paper Space.
- La cartografía conserva las coordenadas originales. Se documenta qué CRS y unidades **resultaron verificados** (todavía pendiente).
- Se guarda, abre de nuevo y plotea correctamente una copia `.dwg`; después se obtiene `Plantilla_Auditoria_CFE_Tijuana.dwt` al validarla en AutoCAD.
