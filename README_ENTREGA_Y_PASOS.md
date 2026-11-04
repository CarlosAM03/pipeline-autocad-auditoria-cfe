# Entrega: cierre de plantilla DATRA v1 + harness inicial Codex

## Diagnóstico visual

El PDF `PlantillaMarcoDatraMapaTijuana(1).pdf` (aportado por el usuario) ya es A1 horizontal y **sí imprime los cinco símbolos de leyenda de la derecha**. El contenido gráfico ausente es el de los **cinco paneles constructivos de la izquierda**. No confundir ambos problemas: no se arreglan dibujos ausentes variando el grosor de pluma.

## Recuperar detalles CFE de forma segura (AutoCAD)

1. Guardar una copia de trabajo de `PlantillaMarcoDatraMapaTijuana.dwg` y del original `146468_PLANOTIJUANA.dwg`; no sobrescribir el histórico.
2. `APPLOAD` → `CFE_DIAGNOSTICO_DETALLES_LAYOUT.lsp` → comando `CFECHEQUEODETALLES` en cada dibujo. Los TXT se guardan en `AuditoriaCFE/Codex/00_Diagnostico/02_CAD_Origen/`.
3. Revisar si las ilustraciones están en `Model` capa `a-detalles` pero faltan sus viewports en `DATRA_A1`. Si Model ya contiene los detalles, recuperar las ventanas gráficas del layout CFE original y ajustar en copia DATRA. Revisar visibilidad de capa, VP Freeze y Plot.
4. Si no están los dibujos en Model de la copia, copiar desde el DWG CFE **las entidades/bloques correctos** al espacio apropiado de la copia DATRA. Seleccionar únicamente detalles técnicos y no importar el mapa por segunda vez.
5. Comprobar en **Plot Preview** y en el PDF final que las ilustraciones técnicas y leyenda son visibles, sin recorte ni líneas invisibles por estilo de ploteo.
6. Guardar finalmente desde AutoCAD como `AuditoriaCFE/recursos/Plantilla_Auditoria_CFE_Tijuana.dwt`. Crear dibujo nuevo a partir de ella para verificar portabilidad. No usar Python para escribir DWT nativa.

> Este paquete **no modifica DWG** y el AutoLISP adjunto es de diagnóstico/solo lectura. La elección de detalles técnicos aplicables es del owner (ADR C06).

## Harness: ubicación exacta

Descomprime el ZIP en la raíz:

`C:\Users\Carl0\Desktop\Datra\CFE\PipeLineDeAuditoria`

El ZIP ya contiene `AGENTS.md` y `AuditoriaCFE/...` **directamente en su raíz**. Extráelo en `PipeLineDeAuditoria` sin reemplazar ADR-000 ni la especificación v0.2. Los artefactos nuevos son:

```text
PipeLineDeAuditoria/
  AGENTS.md
  AuditoriaCFE/
    Docs/Specs/Contrato_Salidas_Proceso1_PROPUESTA.md
    Codex/01_Implementacion_Proceso1/
      ENCARGO_CODEX_PROCESO1_PREPARACION_v0.1.md
      PRIMER_PROMPT_CODEX.txt
      CHECKLIST_REVISION_PROCESO1.md
      CHECKPOINT_PLANTILLA_BASE_v1.md
    recursos/herramientas/CFE_DIAGNOSTICO_DETALLES_LAYOUT.lsp
```

En PowerShell, después de copiar:

```powershell
git status --short
git add AGENTS.md AuditoriaCFE/Docs/Specs/Contrato_Salidas_Proceso1_PROPUESTA.md AuditoriaCFE/Codex/01_Implementacion_Proceso1/ AuditoriaCFE/recursos/herramientas/CFE_DIAGNOSTICO_DETALLES_LAYOUT.lsp
git diff --cached --stat
```

No necesitas crear un commit antes de ejecutar Codex, aunque es recomendable fijar checkpoint si Git muestra exclusivamente esos documentos y herramienta. No versionar fuentes reales de campo, archivos `.dwl` ni salida de auditorías.

## Iniciar Codex

1. Abrir en VS Code la carpeta **`PipeLineDeAuditoria`**, no solo `AuditoriaCFE`.
2. Copiar y enviar el contenido de `AuditoriaCFE/Codex/01_Implementacion_Proceso1/PRIMER_PROMPT_CODEX.txt`.
3. El agente debe leer el ADR y TO-BE, implementar solo **Proceso 1 preparación**, ejecutar pruebas y parar en checkpoint. No debe generar dos `.scr`, modificar el DWG ni declarar EPSG:32611 validado sin pruebas.

## Qué puede aprobarse por separado

- **Cierre visual de plantilla v1:** al imprimir correctamente los detalles en A1 y guardar una DWT probada.
- **ETL 1A:** CSV geográfico normalizado + resumen, linaje, incidencias y regresión; puede avanzar sin CRS.
- **Proyección 1B:** requiere evidencia del sistema de coordenadas y al menos dos puntos de control; sin ella, mantener estado `CRS_PENDIENTE` y no afirmar CSV proyectado apto.
- **SCR/AutoCAD:** continúa fuera del encargo actual y se abrirá solo tras aprobación.
