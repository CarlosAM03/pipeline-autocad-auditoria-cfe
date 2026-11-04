# Fase 3B — Identidad DATRA en marco A1 v0.2

Fecha de consulta: 2026-11-04. **Estado: artefacto CAD preliminar; requiere inspección en AutoCAD 2026.**

## Resultado entregado

- `generar_marco_datra_a1.py`: generador actualizado de presentación editable A1 841 × 594 mm.
- `MARCO_DATRA_A1_EMPRESA_v0_2.dxf`: DXF generado y comprobado con `ezdxf.audit()` sin errores.
- **No contiene la cartografía Tijuana**, no cambia coordenadas WGS84/UTM y no transforma automáticamente tu DWG en DWT.
- Incorpora identidad comercial y contacto de DATRA, pero **no se inventa una razón social** ni se asignan responsables.
- Conserva **13 TAG históricos** del bloque del cajetín y añade **4 TAG corporativos**, todos editables.
- Para evitar conflicto con cajetines previamente importados, el bloque ahora se llama `DATRA_CAJETIN_A1_V02`. Su nombre debe quedar documentado para los scripts CAD futuros.

## Datos que incorpora

| Campo | Texto en marco (sin tildes por compatibilidad CAD) | Fuente |
|---|---|---|
| Nombre comercial | DATRA | https://datra.mx/ |
| Giro breve | Conectividad empresarial / fibra óptica | https://datra.mx/ |
| Teléfono | (664) 941-8515 | https://datra.mx/ |
| Correo | info@datra.mx | https://datra.mx/ |
| Domicilio | Blvd. Cuauhtemoc Sur 9784-C, Col. Revolucion, Tijuana, B.C. | https://datra.mx/cobertura/ |
| Web | datra.mx | https://datra.mx/ |

Otros teléfonos aparecen en artículos y presentaciones comerciales; se conserva el número general mostrado en la página principal. **No se asume que el nombre comercial sea la razón social de una concesión o contrato CFE.**

## Generación en Windows PowerShell

En la carpeta del script:

```powershell
python -m pip install ezdxf
python .\generar_marco_datra_a1.py
```

Se genera `MARCO_DATRA_A1_EMPRESA_v0_2.dxf` al lado del `.py`.

### Logotipo oficial (opcional)

El logotipo no se agregó automáticamente porque **no se pudo recuperar y verificar un archivo gráfico oficial directamente de datra.mx**. No se reutiliza el logotipo de empresas homónimas.

Si cuentas con un PNG o JPG real, autorizado y aprobado de DATRA, copia el archivo junto al generador con el nombre `logo_datra.png`, o pasa su ruta:

```powershell
python -m pip install pillow
python .\generar_marco_datra_a1.py --logo "C:\ruta\al\logo_datra.png"
```

El generador:
1. Copia el activo como `logo_datra_oficial.png` (o `.jpg`) junto al DXF.
2. Lo inserta en el espacio superior derecho del cajetín, conservando relación de aspecto.
3. Usa una **referencia raster relativa**. Para que se vea también en AutoCAD y al guardar la DWT, mantener juntos el logo y el DWG/DWT o actualizar su ruta mediante `EXTERNALREFERENCES` / `XREF` (referencias de imagen).
4. Si no hay un logo local, deja su posición sin imprimir y conserva el nombre DATRA en texto CAD editable.

No agrega fuentes tipográficas ni convierte el logo en vectores; su finalidad es mantener el recurso original verificable.

## Aplicación a la plantilla que ya tienes

**Ejecutar Python no cambia tu `PlantillaMarcoDatraMapaTijuana.dwg`.** La salida es un nuevo DXF. En AutoCAD:

1. Abre **una copia** del DWG ya montado y guarda un respaldo de la DWT v0.1, si existe.
2. Si tienes una pestaña `DATRA_A1` anterior, renómbrala por seguridad a `DATRA_A1_V01_RESPALDO` (o elimínala solamente en la copia). Así se evita una colisión de nombres al importar.
3. Clic derecho en pestaña Layout → **From Template...**, selecciona `MARCO_DATRA_A1_EMPRESA_v0_2.dxf` y la nueva `DATRA_A1`.
4. Conserva el viewport/capa de mapa de la plantilla anterior o crea uno en el panel central; verifica que su escala y CRS sean los esperados. **La importación del layout no importa Model Space del DXF.**
5. En el nuevo layout, usa `EATTEDIT` para modificar el bloque `DATRA_CAJETIN_A1_V02` (responsables, fecha, nombre, recuentos y datos corporativos si hay cambios autorizados).
6. Si agregaste el logo, comprueba su visibilidad y ruta de referencia en una computadora sin acceso al directorio temporal de trabajo.
7. Configura/imprime ISO A1 horizontal (841 × 594 mm) y verifica visualmente. Guarda finalmente como DWT desde AutoCAD, no desde Python.

## Reglas de negocio no alteradas

- El mapa base y las líneas de calles quedan fuera de este generador; la limpieza de capas es otra operación, siempre sobre copia.
- La plantilla sigue siendo una sola lámina A1, sin rutas ni postes preinsertados.
- Los 2 scripts previstos son `01_configurar_plano.scr` y `02_dibujar_auditoria.scr`; no se implementan aquí.
- No se rellenan identificadores de proyecto, responsables o datos de CFE sin fuente y autorización.
