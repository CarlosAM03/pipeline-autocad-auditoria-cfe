# Auditorías CFE — Especificación del pipeline TO-BE

**Versión:** 0.1 — propuesta técnica sujeta a validación del responsable  
**Fecha:** 3 de noviembre de 2026  
**Referencia histórica:** `Reconstruccion_Pipeline_CFE_ASIS_2026-11-03.md` y `Hallazgos_Checkpoint_CFE_2026-11-03.csv`  
**Entregables finales buscados:** DWG y presentación A1 reproducibles, acordes con la plantilla visual proporcionada.  
**Regla de alcance:** sin infraestructura cloud, servidores, bases de datos ni interfaz gráfica propia.

## 1. Decisión de diseño propuesta

**Dos procesos ejecutados secuencialmente:**

1. **Preparación fuera de AutoCAD**, con un único ejecutable CLI (`preparar_auditoria.py`):
   - 1A. Lectura de uno o más libros Excel; extracción selectiva, limpieza y normalización.
   - 1B. Reconstrucción/validación de la topología de rutas y preparación de elementos cartográficos.
   - 1C. Generación de dos scripts `01_configurar_plano.scr` y `02_dibujar_auditoria.scr` y un reporte de calidad.
2. **Construcción del plano en AutoCAD convencional**:
   - 2A. Ejecutar `01_configurar_plano.scr` sobre un dibujo nuevo creado con `Plantilla_Auditoria_CFE_Tijuana.dwt` o un DWG vacío conforme al perfil validado.
   - 2B. Ejecutar `02_dibujar_auditoria.scr` para representar elementos, trayectorias, anotaciones y datos de la auditoría.

**Nota:** la numeración es secuencial, no indica ejecución paralela. `01` y `02` son los únicos scripts que el operador deberá ejecutar en AutoCAD. La plantilla DWT y el mapa vectorial DWG son **recursos estáticos**, no pasos adicionales de ejecución.

## 2. Reutilización del conocimiento previo

| Conocimiento | Nuevo tratamiento |
|---|---|
| AutoCAD convencional puede ejecutar `.scr` mediante `SCRIPT` | Mantener `.scr`, no hacer depender el proceso de `MAPIMPORT`/Map 3D |
| Los insumos contienen coordenadas N/W y hay errores de captura | Parser formal con estados válido / revisar / inválido; conservar el texto fuente |
| Proyección histórica afín a WGS84 / UTM 11N | EPSG:32611 como **hipótesis** de referencia; bloquear hasta comparar contra mapa y puntos de control |
| Existen códigos de poste, caja, excedente | Normalizar categorías, pero comprobar símbolos, tipo de poste y atributos disponibles |
| TXT históricos trazaban solo POINT/TEXT | Usar bloques CAD para simbología y numeración; separar geometría de atributos |
| Ordenar por latitud/longitud causa saltos | Exigir conectividad explícita o revisión del trazado inferido; nunca conectar por posición solamente |
| Hay varios nombres de ruta en un CSV | Modelar auditoría > ruta > tramo > nodo/elemento; varios archivos pueden integrar una auditoría |
| Los TXT tenían anomalías no auditables | Producir reporte reproducible de filas y motivos; no borrar ni corregir silenciosamente |

## 3. Entrada, custodia y alcance

Entrada principal: **uno o varios archivos XLSX/XLS**, preservados intactos, incluso si contienen fotografías, hipervínculos, fórmulas y columnas adicionales. La primera transformación **no edita el archivo fuente**: crea datos derivados. Las imágenes no se incorporan automáticamente al dibujo porque actualmente no forman parte del contrato gráfico de la plantilla; se conserva su ubicación y referencia si existiera una relación con la estructura.

Cada archivo y hoja tiene identidad; el importador registra:
- Nombre del archivo y su huella SHA-256.
- Hoja, fila y, si aplica, identificador operativo original.
- Ruta o subruta designada (normalizando nombres solo bajo una tabla de equivalencias validada).
- Tipo de estructura y coordenadas originales.
- Estado de revisión y razón de cada alerta o exclusión.

Nunca concluir que *archivo = ruta*: cada auditoría puede combinar varios archivos y cada archivo puede contener varias rutas.

## 4. Contrato canónico de datos

Una tabla plana de elementos de infraestructura (`elementos_normalizados.csv`) debe contener, como mínimo:

| Campo | Significado |
|---|---|
| `elemento_id` | Identificador estable de la entidad para el lote, que no dependa solo de latitud/longitud |
| `auditoria_id` | Identificador del plano/entrega |
| `ruta_id` | Ruta lógica a la que se atribuye el registro |
| `archivo_origen`, `hoja_origen`, `fila_origen` | Linaje de datos |
| `tipo_original`, `tipo_normalizado` | Valor fuente y dominio controlado `POSTE`, `CAJA_EMP`, `EXCEDENTE`, `OTRO` |
| `coordenada_original` | Texto íntegro sin alteraciones |
| `latitud`, `longitud` | Coordenadas geográficas decimales tras interpretación validada |
| `este_m`, `norte_m` | Coordenadas proyectadas WCS, en metros, **solo si el CRS se verifica** |
| `estado`, `incidencias` | `VALIDO`, `REVISAR`, `RECHAZADO`, y los motivos concretos |
| `atributos_fuente` | Referencia o campos auxiliares que el modelo final necesita (material, propiedad, transformador, si están disponibles) |

La **topología de red** es una relación distinta de la lista de elementos. Se propone una tabla simple `tramos_confirmados.csv`:

`auditoria_id,ruta_id,tramo_id,desde_elemento_id,hasta_elemento_id,orden,estado`

Puede derivarse de un orden de levantamiento verificable si realmente existe en Excel; de lo contrario debe confirmarse el recorrido. Si el usuario declara los tramos, el archivo expresa esa declaración. El motor puede proponer conexiones, pero **no aceptarlas automáticamente** cuando exista ambigüedad. Mantener nodos compartidos para bifurcaciones; no unir rutas distintas a partir de cercanía física.

La identificación de la troncal y sus ramales se basa en el grafo confirmado: nodos iniciales/finales, grados de conectividad, segmentos y ramificaciones. El conteo de nodos y de distancias sirve como control, **no como prueba independiente de conectividad física**. La regla histórica de que la troncal sea más larga que los ramales queda por validar antes de convertirla en restricción bloqueante.

## 5. Proceso 1A — Extracción, limpieza, validación, transformación

1. Inventariar archivos y hojas; detectar filas/columnas de encabezado y estructura real del Excel.
2. Aplicar mapeo de columnas configurable desde el primer Excel de referencia. Evitar reconocer encabezados arbitrarios sin evidencia.
3. Conservar columnas imprescindibles y la referencia al origen; no eliminar información del libro fuente.
4. Normalizar tipos (`poste`, `cajadedmpalme`, `excedente`, variantes autorizadas). Los desconocidos van a `REVISAR`.
5. Interpretar coordenadas N/W, decimal, signos y separadores; admitir solo conversiones inequívocas.
6. Validar latitud [-90,90], longitud [-180,180], ámbito geográfico esperado, duplicados, valores vacíos y anomalías por ruta.
7. No imputar coordenadas inexistentes mediante promedio/moda ni corregir dígitos especulativamente; enviar a revisión.
8. Transformar WGS84 geográfico a UTM zona 11N **solo después de validar** el sistema de la base CAD.
9. Verificar consistencia por comparación con puntos de control del mapa; no reproducir de forma automática el desplazamiento Norte ~11.5 m de las salidas históricas.
10. Escribir tablas canónicas, incidencias y resumen de conteos por fuente, ruta, tipo y estado.

**Punto de control de calidad:** si hay coordenadas inválidas sin decisión, el lote es `NO APTO PARA GENERACIÓN FINAL`. Se puede producir un dibujo preliminar de elementos válidos claramente marcado, pero no un plano final supuestamente completo.

## 6. Proceso 1B — Topología y dibujo lógico

1. Leer orden, conectividad o definición confirmada de tramos.
2. Generar grafo por `auditoria_id/ruta_id`; detectar componentes desconectados, ciclos, nodos aislados, bifurcaciones y extremos.
3. Verificar aristas inconsistentes o inverosímiles por distancia, sin usar una distancia límite como prueba de que dos postes deban unirse.
4. Excluir `CAJA_EMP` y `EXCEDENTE` de la topología de postes salvo que la relación física esté expresamente modelada; se dibujan como elementos asociados.
5. Identificar trayectorias/tramos y generar segmentos de polilínea independientes; nunca regresar al punto de bifurcación dibujando una falsa conexión entre ramales.
6. Calcular distancias planas entre puntos de **aristas confirmadas**; distinguir estas distancias de la longitud real de fibra/cable y reservas.
7. Numerar estructuras con secuencia de dibujo de la ruta; preservar y mostrar el ID operativo original cuando exista y se requiera.
8. Producir tabla de aristas, extremos y alertas topológicas.

**Punto de control:** para trazar una línea final, cada tramo debe tener nodos identificables y una secuencia o conectividad confirmada. Si falta, se conserva la capa de puntos sin inventar el recorrido.

## 7. Proceso 1C — Compilación de scripts para AutoCAD

La CLI produce exactamente dos scripts operativos:

### `01_configurar_plano.scr`

- Garantizar WCS / UCS World, orientación y unidades de dibujo en metros.
- Preparar capas separadas para mapa, puntos por clase, tramo principal/ramas, numeración, anotaciones, distancias, tablas y elementos de presentación.
- Insertar o referenciar el mapa vectorial Tijuana desde un DWG georreferenciado: preferentemente como **XREF** con ruta relativa y propiedades que impidan modificarlo accidentalmente.
- Verificar punto de control, escala 1:1 en modelo, extents de trabajo y referencia del sistema de coordenadas; atención: asignar `INSUNITS=6` no convierte de latitud/longitud ni prueba la georreferenciación.
- Activar/verificar recursos estáticos de plantilla: bloques de símbolos, estilos, presentación A1, marco, vistas, tablas y cajetín.
- El PDF entregado es **referencia visual**; no representa por sí mismo una plantilla editable DWG/DWT.

### `02_dibujar_auditoria.scr`

- Insertar un bloque distinto para cada tipo de estructura representable (en lugar de confiar solo en `POINT`/`PDMODE`), con sus atributos disponibles.
- Dibujar la geometría validada, troncales y ramales por capas/tramos, sin saltos.
- Incorporar numeración legible de postes, distancias interpostales, identificaciones pertinentes, inicio/fin y notas de ruta.
- Completar **en la medida que existan datos acreditados** la tabla de coordenadas, resumen de postes, cotas, nombre de la ruta, ficha técnica y datos del cajetín.
- Actualizar o ajustar presentaciones/ventanas gráficas para que el área útil se centre en la geometría pertinente sin invadir la simbología.
- Dejar el DWG listo para una revisión visual final y eventual impresión/exportación; no declarar aprobado automáticamente.

**Convención:** modelo (Model Space) contiene geometría en coordenadas reales y metros; presentación (Paper Space) contiene lámina A1, márgenes, cajetín y ventanas a escala. No estirar ni trasladar los elementos geográficos para encajarlos en la hoja; ajustar la escala/viewport.

## 8. DWT y mapa base reutilizables

- Construir **una sola vez** `Plantilla_Auditoria_CFE_Tijuana.dwt`, tomando el PDF A1 como referencia de composición. Incluir marco A1, detalles constructivos a la izquierda, símbolos y tabla/leyendas/cajetín a la derecha, con zonas configurables. Evitar copiar datos ilustrativos de Nezahualcóyotl.
- Mantener `Mapa_Tijuana_Vectorial.dwg` como fondo geográfico autoritativo, con unidades y proyección documentadas. Puede adjuntarse como XREF en la configuración (o incluirse como referencia en DWT si se confirma la estrategia). Verificar extensión y permisos de uso.
- Alternativa **no preferida:** mapa en línea vía AutoCAD GEOMAP, que requiere localización geográfica y sesión; para imprimir o trabajar offline es necesario capturar el mapa como imagen de mapa. No asumir que el mapa online se imprime automáticamente.
- La escala de cada viewport debe elegirse y controlarse por la extensión de la auditoría; no utilizar el zoom indiscriminado a todos los objetos, que puede ser destruido por coordenadas anómalas.

## 9. Formato y fidelidad a la plantilla

Inspección del PDF: 1 página, **A1 horizontal**, 2384 × 1684 puntos. Su composición observada tiene una banda de **detalles técnicos** a la izquierda, un área principal de **mapa y trayectoria** al centro y un costado derecho con **orientación, ubicación, simbología, resumen, datos, tabla y cajetín**. Incluye postes numerados, conectados por ruta y distancias interpostales.

**No copiar** del ejemplo: coordenadas, nombres de calles o colonias, división de otra región, responsables, cantidades, direcciones, logotipos no proporcionados o información de una ruta distinta. Dejar marcados como requeridos los datos empresariales faltantes en vez de inventarlos.

Los datos mínimos que no necesariamente están en el Excel de postes y requieren fuente adicional son: material/tipo de poste, si tiene transformador y propiedad, especificaciones del cable, herrajes, cantidad de fibra, distancias de cable con reservas, datos de responsable/concesionario, logos aprobados, punto de inicio y fin y criterio de escala. No atribuir propiedades a postes por aproximación geográfica.

## 10. Estructura mínima de carpetas

```text
Auditoria_CFE/
  preparar_auditoria.py               # Una CLI local, sin interfaz propia
  recursos/
    Plantilla_Auditoria_CFE_Tijuana.dwt  # Recurso estático creado una vez
    Mapa_Tijuana_Vectorial.dwg          # Recurso estático georreferenciado
  auditorias/
    AMPLIACION_001/
      fuente_original/                 # Excel(s) inmutables
      definicion_ruta/                # Tramos o secuencia confirmada
      salida/
        elementos_normalizados.csv
        tramos_confirmados.csv
        reporte_calidad.csv
        resumen_auditoria.json
        01_configurar_plano.scr
        02_dibujar_auditoria.scr
        auditoria_final.dwg            # Guardado tras ejecución y revisión CAD
```

La estructura es una convención documental propuesta; no se está creando la CLI ni las plantillas hasta validar el Excel real, mapa y versión de AutoCAD.

## 11. Operación prevista por auditoría

1. Copiar los Excel de la ampliación a `fuente_original/` sin editarlos.
2. Declarar la agrupación de ruta/tramos en el mínimo archivo de configuración necesario.
3. Ejecutar `preparar_auditoria.py` y leer su reporte de calidad.
4. Resolver excepciones, confirmar la topología y ejecutar nuevamente hasta obtener lote apto.
5. En AutoCAD convencional, crear dibujo desde el DWT aprobado.
6. Ejecutar `01_configurar_plano.scr`.
7. Ejecutar `02_dibujar_auditoria.scr`.
8. Revisar visualmente la integridad geométrica, conteos, tabla, simbología, títulos, escalas, legibilidad y consistencia de material de red.
9. Guardar DWG y exportar formato de entrega solicitado. Conservar evidencia de revisión.

## 12. Pruebas de aceptación (antes de las tres nuevas ampliaciones)

| Prueba | Criterio |
|---|---|
| Fuentes múltiples | Ningún archivo, hoja o fila operativa desaparece sin estado y motivo |
| Integridad | Conteos de filas leídas = válidas + revisar + rechazadas (según dominio declarado) |
| Coordenadas | Valores N/W se interpretan sin inversión de ejes, rango válido y comparación con punto de control |
| Históricos defectuosos | `432.464440N` es rechazado; longitudes sin decimal se revisan; coordenadas remotas quedan alertadas |
| Duplicados | Se reportan y se decide con criterio de activo/ruta; no se borran automáticamente |
| Topología | Ninguna unión inferida sin soporte; ramales no producen líneas falsas de retorno |
| Reejecución | Mismos insumos y configuración → mismas salidas canónicas y geometría |
| Formato CFE | A1 apaisado con símbolos, numeración, cotas y cajetín según plantilla aceptada |
| Cadena CAD | Ambos `.scr` se ejecutan íntegros sin diálogos no contemplados ni comandos desconocidos en versión de AutoCAD validada |
| Entrega | DWG abre correctamente, imprime en área A1 y coincide con el reporte de elementos |

## 13. Decisiones de diseño y negocio que requieren confirmación

1. **Esquema real del Excel:** hojas, encabezados, imágenes, identificadores, campos de activo/material/propiedad, orden de captura y pertenencia a rutas.
2. **Autoridad de topología:** ¿orden de recorrido registrado, lista `desde/hasta`, trazo manual existente, o ruta a declarar de forma separada?
3. **Modelo geográfico:** proyección del mapa vectorial, punto(s) de control y tratamiento de discrepancia Norte de ~11.5 m observada en TXT históricos.
4. **Símbolos y campos CFE:** cuáles de la plantilla son obligatorios, cuál es el símbolo de `POSTE` cuando no hay material ni transformador, cómo tratar `Registro`, y qué cantidad se contabiliza cuando varias rutas pasan por el mismo poste.
5. **Presentación:** escala o criterio de selección automática por ruta, cantidad de láminas cuando una ruta no cabe legible en A1, y si la auditoría debe incluir referencia de ciudad completa o solo su perímetro.
6. **Compatibilidad:** versión y producto exactos de AutoCAD, idioma, si existe una DWT/DWG ya editable y el mapa vectorial original.

## 14. Orden de construcción recomendado

1. **Contrato de datos:** validar un Excel real (sin asumir sus columnas); obtener `elementos_normalizados.csv` y `reporte_calidad.csv`.
2. **Sistema geográfico:** resolver CRS y controles sobre mapa DWG antes de escribir geometría.
3. **Topología:** cargar una ruta confirmada, validar conectividad y distancias con referencia cartográfica.
4. **Plantilla CAD:** construir DWT A1 + bloques y símbolos, derivados del PDF.
5. **Script 01:** validar inicialización y referencia vectorial en un nuevo DWG.
6. **Script 02:** probar con tramo pequeño, luego ramificación, luego ruta completa y varias fuentes.
7. **Regresión histórica:** comparar resultados de Mirador/Otay–Florido solo como evidencia de datos, no copiar sus errores.
8. **Producción:** repetir para las tres ampliaciones, una auditoría por ejecución, con sus archivos fuente asociados.

**Conclusión:** se crea la implementación de nuevo, pero no se pierde el conocimiento técnico ni se conserva implícitamente ningún error del pipeline histórico. El diseño coloca la calidad y la topología antes del trazado, y la geometría real antes del formato de la hoja.
