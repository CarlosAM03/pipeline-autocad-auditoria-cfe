"""Acta operativa reproducible; aprobar evidencias sigue siendo humano."""
from .util import json_text


def write_acta(stage, manifest):
    lines=['# Acta de checkpoints — '+manifest['auditoria'],'',
           'Estado del lote: PRELIMINAR. Aceptación humana: PENDIENTE.',
           'Código SHA-256: '+manifest['codigo_hash'],
           'Configuración SHA-256: '+manifest['config_hash'],'',
           'Manifiesto activo: manifiesto_ejecucion.json; verificar antes de consumir.','']
    for name,state in manifest['checkpoints'].items():
        lines += ['## '+name,'','```json',json_text(state).rstrip(),'```','']
    lines += ['## Entradas declaradas y hashes','']
    for source in manifest['entradas']:
        lines += [f"- `{source['archivo']}`: `{source['sha256']}`"]
    lines += ['','## Conteos reconciliados','','```json',json_text(manifest['conteos']).rstrip(),'```','',
              'Las pruebas automatizadas se registran en Codex/02_Harness_Integral; esta corrida no ejecuta la suite ni AutoCAD.',
              'Las propuestas KMZ no confirman aristas. Sin baseline, novedad NO_DETERMINADO.','']
    (stage/'acta_checkpoint.md').write_text('\n'.join(lines),encoding='utf-8')
    checklist=['# Checklist de entrega — '+manifest['auditoria'],'',
      '- [ ] Responsable acepta ámbito P-03 y revisa bandeja 00/rechazos.',
      '- [ ] Responsable acredita dos controles distintos WCS/WGS84, tolerancia y metros P-06.',
      '- [ ] Verificar lote con --verificar-paquete antes de abrir la copia indicada.',
      '- [ ] Declarar aristas humanas en entrada/topologia_confirmada.csv; sin ellas SOLO PUNTOS PRELIMINAR.',
      '- [ ] Abrir copia DWG; SCRIPT 01_configurar_plano.scr y SCRIPT 02_dibujar_auditoria.scr.',
      '- [ ] Aprobar carga del LISP empaquetado solo tras verificar hashes; no desactivar SECURELOAD global.',
      '- [ ] Revisar reporte nativo: INSERTs y conteos por tipo coinciden, repetir SCR02 sin duplicados.',
      '- [ ] Verificar mapa/base, WCS/UCS, unidades reales, proxies, imágenes/logo, fuentes y cinco detalles.',
      '- [ ] Imprimir SOLO DATRA_A1, 841x594 mm horizontal: etiquetas, IDs y WGS84 completos y legibles.',
      '- [ ] General: comprobar legibilidad de miles de etiquetas; si falla, BLOQUEANTE FINAL, proponer excepción.',
      '- [ ] Guardar DWG/PDF de copia. DWT canónica solo tras guardar/abrir nativamente y aceptar plantilla.',
      '- [ ] Owner firma aceptación humana. Ningún check automático otorga FINAL.','']
    (stage/'checklist_entrega.md').write_text('\n'.join(checklist),encoding='utf-8')
