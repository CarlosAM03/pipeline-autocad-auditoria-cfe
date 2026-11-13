# Estado y alcance ratificados

| Eje | Estado | Fuente |
|---|---|---|
| PR #1 | Abierto, no fusionado | GitHub PR #1, observado en este turno |
| HEAD | `0267abf312d8cbc6da9b927211f7ae4ca96f7524` | GitHub, observado en este turno |
| CI | Ocho jobs verdes, suite local 93/93: **evidencia histórica reportada por usuario/Codex**, no re-ejecutada por este paquete | Acta del piloto y resumen compartido |
| Mirador | 493 bloques, cero aristas, diagnóstico, NO FINAL | Acta versionada `ACTA_TRABAJO.md`; evidencia CAD privada fuera de Git |
| Fixture | Seis bloques, cinco aristas ficticias; validación de motor, NO red de campo | Acta versionada y resumen usuario |
| CP-01 | Completado técnico; identidad, trazabilidad, CSV/XLSX | Acta versión `0267abf` |
| CP-02 | P-03/P-06 pendiente: CSV01 sin admitidos; CSV02 productivo ausente | Acta versión `0267abf` |
| CP-03 | Compilador y ensayo Core Console declarados; validación de layout/plantilla aún humana | Acta versión `0267abf` |
| CP-04 | SCR genera puntos diagnósticos; topología real no confirmada, presentación no aceptada | Código y acta |
| FINAL | BLOQUEADO | P03, P05, P06, P07, P08 y P04 |

## Alcance de esta etapa

La intervención siguiente es **presentación CAD**, no rediseño del ETL ni aprobación automática de trazados de CFE:

- Diagnosticar por separado coordenadas WCS en Model Space, viewport en Paper Space, tamaño de símbolos, tamaño/posición de textos, estilo de plantilla y plot PDF.
- Confirmar el layout `DATRA_A1` y distinguirlo de `Layout1` antes de comparar capturas.
- Analizar todos los puntos, incluidos extremos geográficos, sin eliminarlos ni moverlos para acomodar el plano.
- Mantener dos SCR operativos, el contrato de CSV y XLSX, IDs y reglas aprobadas.
- Exigir evidencia antes/después: inspección estructural DWG, hashes, PDF auténticos, capas y entidades nativas.

## Lo que no permite concluir esta revisión

- No prueba que las coordenadas geográficas coincidan con el fondo del mapa: faltan controles reales P-06.
- No homologa legibilidad de todos los elementos en A1 ni los paneles técnicos P-07/P-08.
- No permite atribuir los siete PDF adicionales a Natura/Otay sin manifest de procedencia.
- No verifica los ZIP privados del piloto dentro de este paquete; no están aquí.
