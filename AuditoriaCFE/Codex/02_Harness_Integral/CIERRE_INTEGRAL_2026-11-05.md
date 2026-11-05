# Cierre integral — software verificable con gates pendientes

Fecha de decisiones: 2026-11-05. Rama: `codex/etl-unificado-auditoria-js`. PR: [#1](https://github.com/CarlosAM03/pipeline-autocad-auditoria-cfe/pull/1), listo para revisión, **sin merge**.

## Implementación y pruebas

CP-01/02 y compiladores CP-03/04 integrados. Código v0.3.0, dos SCR y dos auxiliares LISP cargados automáticamente, sin tercer paso de SCRIPT/APPLOAD. Se conservan encabezados 00/01 y lector 02 v1; v2 es explícito. El programa grande vive en `cad_datos.lsp`, evitando líneas SCRIPT de megabytes; prueba sintética de 4200 filas incluida.

**Última suite local: 80 casos, 80 aprobados, 0 fallidos, 0 omitidos, 61.554 s.** Las 43 pruebas iniciales están intactas. `compileall`, Ruff E9/F821/F822/F823, `pip check`, custodia/oráculo y `git diff --check` ejecutados correctamente. Comando: `python -m unittest discover -s AuditoriaCFE/tests -v`; log local `tests/_runtime/FINAL_PRUEBAS.log`.

Clon superficial de f22d886 sin fuentes privadas: 79 descubiertas, 70 aprobadas, nueve omitidas, ninguna fallida, 49.046 s. Las nueve corresponden a originales XLSX/JS ausentes. Ese corte completó CI de push en Windows/Linux y Python 3.10/3.12. El commit posterior de cierre incorpora el caso 80 y vuelve a ejecutar CI; el estado de su SHA se consulta en el PR, sin atribuirle anticipadamente el resultado del corte anterior.

Individual Natura, demo (cuatro filas admitidas en 01/02 con controles sintéticos), cuatro auditorías batch, integridad y reproducibilidad ejecutados. Conteos 00 y conciliación: 438 Natura, 493 Mirador, 747 Otay y 4131 General. Ver [acta fase 6](acta_fase_6.md). Las cuatro fuentes reales siguen sin 01 admitido ni 02 productivo por P-03/P-06; los diagnósticos usan otro archivo y no promueven registros.

## Último ensayo nativo, realmente ejecutado

El servicio GUI mantuvo la parada de Escape aun después de las nuevas autorizaciones y de reinicializar el cliente. No se realizaron más acciones GUI ni se guardó el documento del usuario. **Sí** se ejecutó AutoCAD **Core Console 2026 W.122** con los SCR generados sobre copias separadas.

En cada copia: SCR01, SCR02 y repetición SCR02, inspección, QSAVE y ploteo. La nueva apertura de la copia conservó las entidades. El runtime verificó INSERTs reales por tipo y aristas; las cinco corridas terminaron sin errores ni duplicados. Se generaron cinco PDF de diagnóstico y `pdfinfo` confirmó **una página A1 horizontal** en cada uno.

| Copia | Bloques reales | POSTE / CAJA_EMP / EXCEDENTE | Aristas nuevas | Tiempo nativo final |
|---|---:|---|---:|---:|
| Fixture | 4 | 2 / 1 / 1 | 0 | 14.97 s |
| Natura | 438 | 438 / 0 / 0 | 0 | 17.43 s |
| Mirador | 493 | 414 / 20 / 59 | 0 | 16.40 s |
| Otay-Florido | 747 | 584 / 17 / 146 | 0 | 17.40 s |
| Tijuana-General | 4131 | 4131 / 0 / 0 | 0 | 30.30 s |

Pruebas nativas de datos reales = **diagnóstico de puntos**, no autorización geográfica. Las ramas/ciclos/aristas confirmadas y distancias se probaron en fixtures Python; no se afirma ejecución de líneas físicas reales sin entrada humana. Cada `salida/resultados_cad/resultado_ensayo.json` registra ID del lote, hashes de compiladores/DWG/PDF/log, conteos y aceptación humana pendiente. Los binarios y logs privados permanecen fuera de Git.

Errores reparados durante el ensayo: confianza de carga (carpeta concreta verificada y restaurada en el driver), ausencia de COM/ActiveX en Core Console, manejador de errores AutoLISP, viewport mediante MVIEW/ZOOM, referencia a objetos confundida con Center, encuadre y margen de etiquetas, borde no imprimible y encabezado dentro del papel. Se conserva rollback del grupo si falla una operación.

El primer PDF de Natura produjo más de 21,000 anotaciones SHX y Poppler no pudo abrir la página. SCR01 establece PDFSHX=0: conserva glifos visibles y elimina comentarios SHX, conforme a [Autodesk](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-Core/files/GUID-56EA988C-A1DA-4E85-8765-B3F31A01AB02.htm). Los cinco PDF posteriores se abren y tienen tamaño correcto. Esa preferencia queda en el perfil, no altera coordenadas ni seguridad de carga.

## Revisión visual y límites reales

Se renderizaron e inspeccionaron fixture, Mirador y General con Poppler. Se corrigieron recortes del encabezado/encuadre. En Mirador y General hay puntos remotos y agrupaciones de etiquetas superpuestas: **NO pasan legibilidad para FINAL**. No se omitieron etiquetas ni se crearon páginas adicionales.

La base DATRA declara INSUNITS=4 y WCS activo. DATRA_A1 es A1 mm; Layout1 conserva escala/extents de pulgadas. No se escaló el mapa ni se aplicó offset geográfico. La coincidencia real continúa sin acreditación. El marco se reutiliza, sin redibujar Tijuana ni insertar otro mapa. Los cinco paneles y el cuadro de ubicación/logo no están acreditados como entrega completa; el runtime preserva geometría heredada y solo admite prototipos no homologados en espacios vacíos, sin afirmar materiales. Se detectaron fuentes sustituidas. Los campos de cajetín permanecen editables/pendientes donde falta información.

El título de GUI observado indicaba STUDENT/NON COMMERCIAL. La prueba de ingeniería no acredita licencia de uso productivo ni permiso de difusión; el responsable debe verificar ese alcance antes de producción.

**No se generó ni certificó DWT canónica, plano FINAL ni PDF productivo.** Los DWG/PDF de ensayo existen localmente, etiquetados DIAGNOSTICO_NO_VERIFICADO, y no sustituyen la aceptación GUI/humana.

## Gates y siguiente acción exacta

| Clase | Gate | Acción del responsable |
|---|---|---|
| BLOQUEANTE productivo | P-03 | Aprobar perímetros/corredores y resolver puntos remotos con evidencia por fila. Repetir preparación. |
| BLOQUEANTE productivo | P-06 | Acreditar dos controles reales distintos WCS/WGS84, metros y tolerancia medida de la base DATRA. |
| BLOQUEANTE para rutas finales | P-05 | Firmar aristas físicas y mapa de IDs. Sin esa entrada, mantener solo puntos. |
| BLOQUEANTE FINAL | P-07/P-08/P-04 | Completar/aceptar recursos, paneles, fuentes, cajetín y DWT; revisar DWG/PDF en GUI. Tras P-03/P-06, volver a evaluar A1. Si General sigue ilegible, aprobar excepción normativa; no esconder datos ni añadir hojas por algoritmo. |
| NO BLOQUEANTE | P-02 | Aportar inventario histórico si necesita novedad; sin él NO_DETERMINADO. |
| NO BLOQUEANTE para software | Licencia | Autorizar difusión antes de publicar nuevos recursos/binaries CAD; ahora permanecen locales con hash. |
| MEJORA | SLA y fixture nativo de líneas | Fijar presupuesto medido y ampliar ensayo nativo con grafo totalmente ficticio si se desea; no es evidencia de enlaces reales. |

P-01 precedencia, P-09 contratos, P-10 perfil 2026 inglés y Q01–Q75 no se reabren. P-11 se concilia por definiciones, sin forzar cifras históricas.

## Publicación y protección

Fases confirmadas: 1706ca0, 176355d, e46a883, b5a6201, f09cb55, bb456b6, f22d886; correcciones nativas en commit posterior independiente. No se reescribieron commits/tags ni main. Push de fases 0–6 comprobado. El conector negó crear PR por 403 de integración; la credencial Git local autorizada permitió crearlo mediante API, sin exponer secretos.

Protección de main aplicada y leída de vuelta (HTTP 200): una aprobación, revisión de cambios desactualizada al nuevo push, conversaciones resueltas y los cuatro checks `tests (ubuntu-latest/windows-latest, py3.10/py3.12)`, ramas al día, administradores incluidos, force-push y borrado deshabilitados. La variante inicial con bypass de administradores fue rechazada por auto-review; se aplicó la alternativa segura enforce_admins=true. No hay merge automático y el autor no puede aprobar su propio PR.

Antes/después del push, solo quedaron tres archivos previos sin seguimiento del paquete del owner: `.gitignore`, `05_PROMPT_MAESTRO_CODEX.txt`, `06_INVENTARIO_PAQUETE.json` en Harness. Se conservaron fuera de los commits. Transcripción, entradas/salidas, resoluciones/topología reales, temporales y nuevos CAD propietarios ignorados. Hashes de los nueve recursos/fuentes de referencia se cotejaron sin cambios; ADR-000, TO-BE v0.2 y README_ENTREGA_Y_PASOS.md permanecen intactos.

La validación técnica concluye con gates explícitos. El último SHA, resultado remoto de sus checks y estado Git se informan en la entrega; este documento no se autoatribuye el hash de su propio commit.
