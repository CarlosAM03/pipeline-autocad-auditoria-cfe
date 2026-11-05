# AGENTS.md — Pipeline de Auditorías CFE/DATRA — Arnés integral

## Ámbito, corte y autoridad

Raíz del repositorio = carpeta que contiene este `AGENTS.md`; no depender de ruta absoluta excepto para mostrar contexto. La rama autorizada es `codex/etl-unificado-auditoria-js`, HEAD de referencia `f3060742e9a2ce90d186802ab3de5a4ccd968633`. Respuestas Q01–Q75 del 2026-11-05 autorizan completar el pipeline por fases y hacer push en esa rama sin merge a `main`.

**Jerarquía:** `AuditoriaCFE/Docs/ADRs/ADR-000_...md` conserva las decisiones históricas; `ADR-001_Enmienda_Cierre_2026-11-05.md` prevalece **solo en los apartados expresamente enmendados**; después `Docs/Specs/Especificacion_Pipeline_Auditorias_CFE_TOBE_v0.3.md`, `Contrato_Salidas_Pipeline_P09_v1.md`, y `AuditoriaCFE/Codex/02_Harness_Integral/01_ACTA_CIERRE.md` + respuestas originales para resolver ambigüedades; v0.2, diagnósticos y JS como evidencia no autoritativa.

## Autorización nueva

Se autoriza el desarrollo end-to-end de CP-01, CP-02, CP-03 y CP-04: módulos ETL, geofences, resoluciones, KMZ/topología, generadores **exactamente dos SCR**, AutoLISP auxiliar empaquetado, recursos CAD/plantilla desde copias, CLI individual/batch, tests y CI. Se permite probar en AutoCAD 2026 **en copias** si existe acceso. La compilación de SCR ocurre fuera de AutoCAD; el operador luego abre una copia del DWG/DWT DATRA, ejecuta SCR01 y SCR02, revisa DWG/PDF A1.

**Autonomía:** implementar y probar etapas independientes sin detenerse por datos externos faltantes. Codex puede escoger librerías, estrategias internas y fixtures sin alterar contratos aprobados. No puede inferir como verdad un inicio/final de ruta, conexión física, CRS validado, corrección de coordenada, detalle de instalación o permiso de publicar un recurso sin respaldo. Documentar gate y continuar el resto.

## Custodia estricta

- `Auditorias-20261104T035633Z-1-001/`: histórico **solo lectura**; jamás modificar, renombrar, ejecutar en sitio, reextraer ZIP o escribir dentro. Codex puede leer archivos exactos y crear **copias** bajo `AuditoriaCFE/auditorias/<nombre>/entrada/` con registro SHA-256.
- `AuditoriaCFE/recursos/`: autorizado generar nuevos recursos canónicos en copias con respaldo. Base: `PlantillaMarcoDatraMapaTijuana.dwg`; CFE `146468_PLANOTIJUANA.dwg` es referencia; Mirador para contraste del histórico UTM84-11N/metros. No sobrescribir un original sin copia y plan de reversión.
- Todos los datos operativos persistentes de una auditoría van bajo `entrada/` o `salida/`: XLSX/KMZ/topología/resoluciones y salidas CSV/SCR/reportes/manifiestos. Mantener `configuracion.json` estructural, fuentes Python, documentación oficial, plugins y herramientas en sus ubicaciones explícitas. `temporales/` solo efímero para publicación atómica.
- Documentos generados por Codex, actas y evidencias de trabajo van bajo `AuditoriaCFE/Codex/`, no en raíz salvo README oficiales.
- **Seguridad Git:** nunca `git add .` indiscriminadamente, nunca registrar la transcripción íntegra `00_RESPUESTAS_ORIGINALES.md`, XLSX, KMZ, planos de campo, entradas/salidas, claves o aristas privadas en un repo público. Antes de push consultar `git status`, `git ls-files`, `git check-ignore` y stage diff. El repo actual es público; no asumir que todos los archivos delicados ya están ignorados. Verificar permisos antes de publicar nuevos CAD binarios canónicos.
- Nunca `git reset --hard`, `git clean`, borrar fuentes o mover sin preservar histórico.

## Reglas de negocio no negociables

- Misma auditoría lógica puede reunir varias rutas, tres tipos `POSTE/CAJA_EMP/EXCEDENTE`, `Registro` FUERA_ALCANCE.
- Deduplicar tipo + coordenadas decimales exactas y preservar cada ocurrencia/prevalencia según orden técnico determinista; nunca ordenar coordenadas para suponer camino físico.
- 00 es un inventario identificado y deduplicado; 00 revisión auxiliar separa problemas; 01 mínimo tiene exclusivamente `Ruta,Elemento de Red,Coordenadas`; 02 requiere control WCS real y versión de contrato.
- Sin baseline de inventario acreditada, novedad NO_DETERMINADO. El DWG base no es baseline histórica de novedades.
- Sin perímetro autorizado, no declarar los puntos de 01 productivos; rectángulo diagnóstico no es evidencia. Rechazos se excluyen de CAD pero quedan en linaje.
- EPSG:32611 candidato, NO confirmado hasta dos controles WCS↔WGS84 distintos con residual dentro de tolerancia real. Cualquier modo de prueba sin validación produce SOLO archivos rotulados DIAGNÓSTICO, nunca salida 02 validada ni DWG FINAL.
- Los tres anillos redundantes son contexto; aristas derivadas de proximidad o KMZ son propuestas hasta confirmación humana. Sin `topologia_confirmada.csv` aprobada dibujar solo PUNTOS PRELIMINARES.
- AutoCAD convencional 2026 inglés, dos SCR operativos en orden, sin Map 3D, sin mapa duplicado, geometría en Model Space real y presentación A1 horizontal única. Si no se lee, no omitir etiquetas ni crear hojas extra sin enmienda.
- Cajetín DATRA con datos acreditados y detalles constructivos solo confirmados. El owner revisa/acepta FINAL.

## Trabajo y checkpoints

Seguir `AuditoriaCFE/Codex/02_Harness_Integral/02_PLAN_IMPLEMENTACION.md` por fases 0–6 y `03_MATRIZ_PRUEBAS.md`. Mantener suite original de 43 tests y ampliar. Tests CI sintéticos no deben fingir inspección CAD/histórico. Reportar estado por CP con `COMPLETADO_TECNICO`, `PENDIENTE_EVIDENCIA`, `PRELIMINAR`, `FALLIDO`, `ACEPTADO_HUMANO` (este último solo tras autorización humana).

La rama tiene un archivo rastreado reportado como **eliminado**: `README_ENTREGA_Y_PASOS.md`, actualmente copiado en `temp/`. No ocultar ni perderlo: restaurar o mover a diagnóstico con conservación de historial y registrar la decisión conservadora en el primer checkpoint.

Crear commits locales por fase, pruebas, staging explícito, **push permitido** a `codex/etl-unificado-auditoria-js` y PR listo si existe acceso. **Nunca hacer merge a main por cuenta propia**. No esperar respuesta ante fallos de ingeniería solucionables; si no hay GUI/KMZ/controles, continuar módulos restantes y entregar reporte verificable de gates pendientes.

---

- ! nota: el kmz se encuentra en Auditorias-20261104T035633Z-1-001\Rutas Con nombre Ultima Version.kmz es una copia segura para lectura y manupulacion. !
