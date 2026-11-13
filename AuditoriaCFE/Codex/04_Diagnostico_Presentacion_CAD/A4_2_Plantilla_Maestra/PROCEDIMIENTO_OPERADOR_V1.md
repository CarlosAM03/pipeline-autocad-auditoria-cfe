# Operación con la plantilla propuesta

1. Verificar el SHA de la plantilla propuesta. Copiar el DWG a entrada de una carpeta de auditoría nueva y configurar cad.base_dwg con el nombre de esa copia. Usar cad.copia=true, layout DATRA_A1 y el perfil A4.1 de presentación. Desactivar prototipos con cad.prototipos=false.
2. Ejecutar la preparación diagnóstica habitual. La configuración de los tres perfiles autorizados aplica 300 m cuando cad.radio_visibilidad_m se omite. Un entero positivo lo sobrescribe. null restaura la visibilidad diagnóstica anterior. El modo fuera de diagnóstico y perfiles sin presentación conservan su comportamiento.
3. Revisar el manifiesto, los reportes de visibilidad y el índice. Abrir la copia mutable indicada por el reporte CAD. Cargar 01_configurar_plano.scr y luego 02_dibujar_auditoria.scr con SCRIPT.
4. Revisar los layouts del plan. Guardar y reabrir. Publicar un PDF único A1 horizontal con los layouts de presentacion_paginas.json en su orden. Revisar los cuatro paneles históricos y el aviso de derivación, además de las páginas de detalle.
5. Conservar los dos XLSX, el linaje y las exclusiones. La revisión de campo y la aprobación de la propuesta son controles independientes.
