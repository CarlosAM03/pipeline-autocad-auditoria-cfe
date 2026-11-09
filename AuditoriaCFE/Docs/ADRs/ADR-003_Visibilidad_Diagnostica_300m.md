# ADR-003 — Visibilidad diagnóstica predeterminada de 300 m

Estado autorizado por el responsable el 9 de noviembre de 2026. Enmienda de alcance a [ADR-002](ADR-002_Presentacion_Multipagina_Y_Rutas_v1.md), conforme al [acta de cierre](../../Codex/04_Diagnostico_Presentacion_CAD/CIERRE_CHECKPOINT_A4_1_1_Y_A4_1_2026-11-09.md).

Para los perfiles multipágina diagnósticos de Natura, Mirador y Otay–Florido se aplica 300 m por defecto a la selección visual antes de compilar CAD. Los componentes de al menos seis posiciones POSTE distintas permanecen visibles. Las cajas y excedentes se evalúan con el apoyo de un poste conservado dentro del radio. Se conserva una decisión por ID en el manifiesto y en las salidas de visibilidad.

La configuración cad.radio_visibilidad_m admite un entero positivo como override. null conserva la presentación anterior. La ausencia de perfil multipágina o el uso de otro modo conserva el comportamiento de sus configuraciones previas. La política es reversible y conserva IDs, coordenadas, CSV, linaje, asociaciones, XLSX y gates. La proximidad carece de autoridad sobre las líneas físicas.
