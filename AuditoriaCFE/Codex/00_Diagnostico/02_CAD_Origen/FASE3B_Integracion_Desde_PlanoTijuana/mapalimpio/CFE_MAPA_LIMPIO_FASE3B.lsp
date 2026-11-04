;;; CFE / DATRA - FASE 3B - Mapa Tijuana limpio (AutoCAD Windows)
;;; Version 0.1 - 2026-11-04
;;; OBJETIVO: capas viales/manzanas + nombres de calles opcionales.
;;; MODO: sobre una COPIA de 146468_PLANOTIJUANA.dwg o de la plantilla DATRA.
;;; NUNCA modifica por si solo archivos del disco: los cambios quedan en la
;;; sesion hasta que el usuario ejecuta SAVEAS. Sin borrar, sin EXPLODE.
;;;
;;; COMANDOS:
;;;  CFEMAPA_LIMPIAR    Aplica perfil VIAS o URBANO, texto de calles opcional
;;;  CFEMAPA_NOMBRES    Alterna nombres de calle en la misma sesion
;;;  CFEMAPA_RESTAURAR Revierte capas y cambios de texto de la sesion
;;;  CFEMAPA_RESUMEN   Guarda reporte de estado y cambios
;;;
;;; LIMITACIONES: si lineas/vialidades y elementos irrelevantes comparten
;;; layer 0 dentro del mismo bloque, NO se puede clasificarlos semanticamente
;;; por capas. El comando genera advertencia; se requiere inspeccion visual.
;;; Los textos en definiciones de bloque utilizadas en Paper Space se protegen.
;;; En AutoCAD activar o desactivar layers actua globalmente: se conservan
;;; capas utilizadas por entidades de Paper Space y recursos DATRA/CFE.

(vl-load-com)

(setq *cfemap-estado* nil)
(setq *cfemap-capasmem* nil)
(setq *cfemap-textmem* nil)
(setq *cfemap-protegidos* nil)
(setq *cfemap-capas-papel* nil)
(setq *cfemap-visitados* nil)
(setq *cfemap-movidos* 0)
(setq *cfemap-calles* 0)
(setq *cfemap-ocultos* 0)
(setq *cfemap-errores* 0)
(setq *cfemap-lineas0* 0)
(setq *cfemap-perfil* "")
(setq *cfemap-nombres-activos* nil)

(defun cfemap:up (s) (if (= (type s) 'STR) (strcase s) ""))
(defun cfemap:in (a l) (if (member a l) T nil))
(defun cfemap:begins (s prefix)
  (= (substr (cfemap:up s) 1 (strlen prefix)) (cfemap:up prefix))
)
(defun cfemap:has (s substrng)
  (if (vl-string-search (cfemap:up substrng) (cfemap:up s)) T nil)
)
(defun cfemap:print (s) (princ (strcat "\n[CFEMAPA] " s)))
(defun cfemap:catlayer (n / s)
  (setq s (cfemap:up n))
  (cond
    ((cfemap:in s
       '("CALLES" "CARRETERA" "CARRETERA_S_PUENTE" "PUENTE"
         "CAMELLON" "BANQUETA" "BORDE_PAV" "BRECHA" "TERRACERIA"
         "PASO-DESNIVEL" "CORREDOR TIJUANA 2000" "TRAZA-URBANA"
         "FTRAZA" "CALLE" "VIALIDADES" "VIALIDAD" "EJE_VIAL"))
      "VIAL")
    ((cfemap:in s
       '("MANZANA" "MANZANAS" "MANZ" "MANZANA_IND" "MZA"
         "PREDIOS" "LIMITE-DE-PREDIOS" "LINDERO_FISICO"
         "CONSTRUCCIONES" "CONST" "CONST_IND" "RUSTICO"
         "LIMITE-INTERNACIONAL"))
      "URBANO")
    (T "OTRO")
  )
)
(defun cfemap:street-text (layername / s)
  (setq s (cfemap:up layername))
  (or (cfemap:in s '("NOMBRES_DE_CALLE" "DNOMBRESDECALLES"
                     "NOMBRESDECALLES" "CALLETXT" "CALLE_TEXTO"
                     "TEXT_CALLES" "TXTCALLE" "CALLES"))
      (cfemap:has s "NOMBRES_DE_CALLE")
  )
)
(defun cfemap:sheetlayer (n / s)
  (setq s (cfemap:up n))
  (or
    (cfemap:in s '("0" "DEFPOINTS"))
    (cfemap:begins s "DATRA")
    (cfemap:begins s "CFE_MAPA_")
    (cfemap:begins s "MARCO")
    (cfemap:begins s "A-")
    (cfemap:begins s "PLANO (")
    (cfemap:begins s "48 PIE DE PLANO")
    (cfemap:in s '("PIEPLANO" "ATT" "DET_DIB" "A-DETALLES"))
    (member s *cfemap-capas-papel*)
  )
)
(defun cfemap:keep (n perfil)
  (or (cfemap:sheetlayer n)
      (= (cfemap:catlayer n) "VIAL")
      (and (= perfil "URBANO") (= (cfemap:catlayer n) "URBANO"))
  )
)
(defun cfemap:doc () (vla-get-ActiveDocument (vlax-get-acad-object)))
(defun cfemap:layers () (vla-get-Layers (cfemap:doc)))
(defun cfemap:getlayer (name / result)
  (setq result (vl-catch-all-apply 'vla-Item (list (cfemap:layers) name)))
  (if (vl-catch-all-error-p result) nil result)
)
(defun cfemap:newlayer (name color / obj)
  (setq obj (cfemap:getlayer name))
  (if (not obj) (setq obj (vla-Add (cfemap:layers) name)))
  (vl-catch-all-apply 'vla-put-Color (list obj color))
  obj
)
(defun cfemap:layeron (name yes / layer)
  (if (setq layer (cfemap:getlayer name))
    (vl-catch-all-apply 'vla-put-LayerOn
      (list layer (if yes :vlax-true :vlax-false)))
  )
)

;;; Analiza los bloques usados EN PAPEL para no cambiar los titulos
;;; ni mover sus textos interiores a capas cartograficas.
(defun cfemap:protect-block (name / key hdr e d typ)
  (setq key (cfemap:up name))
  (if (and (/= key "") (not (member key *cfemap-protegidos*)))
    (progn
      (setq *cfemap-protegidos* (cons key *cfemap-protegidos*))
      (setq hdr (tblobjname "BLOCK" name))
      (if hdr
        (progn
          (setq e (entnext hdr))
          (while e
            (setq d (entget e))
            (setq typ (cdr (assoc 0 d)))
            (if (= typ "ENDBLK")
              (setq e nil)
              (progn
                (if (assoc 8 d)
                  (setq *cfemap-capas-papel*
                    (cons (cfemap:up (cdr (assoc 8 d))) *cfemap-capas-papel*))
                )
                (if (= typ "INSERT")
                  (cfemap:protect-block (cdr (assoc 2 d)))
                )
                (setq e (entnext e))
              )
            )
          )
        )
      )
    )
  )
)
(defun cfemap:protect-paper (/ r name)
  (setq *cfemap-protegidos* nil *cfemap-capas-papel* nil)
  (setq r (tblnext "BLOCK" T))
  (while r
    (setq name (cdr (assoc 2 r)))
    (if (cfemap:has (cfemap:up name) "*PAPER_SPACE")
      (cfemap:protect-block name)
    )
    (setq r (tblnext "BLOCK"))
  )
  (setq *cfemap-capas-papel* (vl-remove-if 'null *cfemap-capas-papel*))
)

;;; Cambia SOLO la CAPA, sin eliminar ni reemplazar geometria.
;;; Conserva (entidad . capa_original) para RESTAURAR en esta sesion.
(defun cfemap:movetext (entity newlayer / d old altered result)
  (setq d (entget entity))
  (setq old (cdr (assoc 8 d)))
  (if (not old) (setq old "0"))
  (if (/= (cfemap:up old) (cfemap:up newlayer))
    (progn
      (setq altered (subst (cons 8 newlayer) (assoc 8 d) d))
      (setq result (vl-catch-all-apply 'entmod (list altered)))
      (if (or (vl-catch-all-error-p result) (null result))
        (setq *cfemap-errores* (1+ *cfemap-errores*))
        (progn
          (setq *cfemap-textmem* (cons (cons entity old) *cfemap-textmem*))
          (setq *cfemap-movidos* (1+ *cfemap-movidos*))
        )
      )
    )
  )
)
(defun cfemap:process-block (name / key hdr e d typ original)
  (setq key (cfemap:up name))
  (if (and (/= key "")
           (not (member key *cfemap-visitados*))
           (not (member key *cfemap-protegidos*)))
    (progn
      (setq *cfemap-visitados* (cons key *cfemap-visitados*))
      (setq hdr (tblobjname "BLOCK" name))
      (if hdr
        (progn
          (setq e (entnext hdr))
          (while e
            (setq d (entget e))
            (setq typ (cdr (assoc 0 d)))
            (if (= typ "ENDBLK")
              (setq e nil)
              (progn
                (cond
                  ((= typ "INSERT")
                    (cfemap:process-block (cdr (assoc 2 d))))
                  ((member typ '("TEXT" "MTEXT" "ATTDEF" "ATTRIB"))
                    (setq original (cdr (assoc 8 d)))
                    (if (cfemap:street-text original)
                      (progn
                        (cfemap:movetext e "CFE_MAPA_NOMBRES_CALLE")
                        (setq *cfemap-calles* (1+ *cfemap-calles*))
                      )
                      (progn
                        (cfemap:movetext e "CFE_MAPA_TEXTOS_OCULTOS")
                        (setq *cfemap-ocultos* (1+ *cfemap-ocultos*))
                      )
                    )
                  )
                  ((and (= (cfemap:up (cdr (assoc 8 d))) "0")
                        (member typ '("LINE" "LWPOLYLINE" "POLYLINE" "ARC")))
                    (setq *cfemap-lineas0* (1+ *cfemap-lineas0*))
                  )
                )
                (setq e (entnext e))
              )
            )
          )
        )
      )
    )
  )
)
(defun cfemap:snapshot-layers (/ l)
  (setq *cfemap-capasmem* nil)
  (vlax-for l (cfemap:layers)
    (setq *cfemap-capasmem*
      (cons (cons (vla-get-Name l)
                  (= (vla-get-LayerOn l) :vlax-true))
            *cfemap-capasmem*))
  )
)
(defun cfemap:apply-layers (perfil / l name)
  (vl-cmdf "_.-LAYER" "_S" "0" "")
  (vlax-for l (cfemap:layers)
    (setq name (vla-get-Name l))
    (cond
      ((= (cfemap:up name) "CFE_MAPA_TEXTOS_OCULTOS")
        (cfemap:layeron name nil))
      ((= (cfemap:up name) "CFE_MAPA_NOMBRES_CALLE")
        (cfemap:layeron name *cfemap-nombres-activos*))
      ((cfemap:keep name perfil)
        (cfemap:layeron name T))
      (T (cfemap:layeron name nil))
    )
  )
)
(defun cfemap:report-path ()
  (strcat (getvar "DWGPREFIX") (vl-filename-base (getvar "DWGNAME"))
          "_CFEMAPA_LIMPIEZA.txt")
)
(defun cfemap:report (/ fh item)
  (setq fh (open (cfemap:report-path) "w"))
  (if fh
    (progn
      (write-line "CFE DATRA | FASE 3B | LIMPIEZA CARTOGRAFICA" fh)
      (write-line "Revision/resultado PRELIMINAR: validar visualmente antes de SAVEAS DWT." fh)
      (write-line (strcat "DWG: " (getvar "DWGNAME")) fh)
      (write-line (strcat "PERFIL: " *cfemap-perfil*) fh)
      (write-line (strcat "NOMBRES_CALLE_ACTIVOS: "
                     (if *cfemap-nombres-activos* "SI" "NO")) fh)
      (write-line (strcat "TEXTOS_REUBICADOS: " (itoa *cfemap-movidos*)) fh)
      (write-line (strcat "TEXTOS_CALLE_DETECTADOS: " (itoa *cfemap-calles*)) fh)
      (write-line (strcat "OTROS_TEXTOS_OCULTADOS: " (itoa *cfemap-ocultos*)) fh)
      (write-line (strcat "ERRORES_CAMBIO_TEXTO: " (itoa *cfemap-errores*)) fh)
      (write-line (strcat "PRIMITIVAS_CAPA_0_EN_BLOQUES_MODELO: "
                         (itoa *cfemap-lineas0*)) fh)
      (write-line "La clasificacion de TEXTO_CALLE se basa en nombre de capa, no en OCR." fh)
      (write-line "La deteccion de primitivas layer 0 no prueba que sean vias." fh)
      (write-line "Sin borrados de entidades; capas de fondo apagadas, no eliminadas." fh)
      (write-line "La restauracion en sesion depende de que el LISP siga cargado." fh)
      (write-line "LISTA DE CAPAS APAGADAS EN ESTE MOMENTO:" fh)
      (foreach item *cfemap-capasmem*
        (if (and (cfemap:getlayer (car item))
                 (= (vla-get-LayerOn (cfemap:getlayer (car item))) :vlax-false))
          (write-line (strcat "OFF\t" (car item)) fh)
        )
      )
      (close fh)
    )
  )
  (cfemap:print (strcat "Informe: " (cfemap:report-path)))
)
(defun cfemap:safe-workdir ()
  (if (cfemap:has (getvar "DWGPREFIX") "Auditorias-20261104T035633Z-1-001\\")
    (progn
      (cfemap:print "BLOQUEADO: el DWG esta dentro de la carpeta historica.")
      nil
    )
    T
  )
)

(defun c:CFEMAPA_LIMPIAR (/ p nombres answer confirm)
  (if *cfemap-estado*
    (cfemap:print "Ya hay un perfil aplicado. Use CFEMAPA_RESTAURAR primero.")
    (if (cfemap:safe-workdir)
      (progn
        (cfemap:print "Trabaje sobre una COPIA del DWG. No se grabara nada automaticamente.")
        (initget "V U")
        (setq p (getkword "\nPerfil [V=VIAS / U=VIAS+MANZANAS] <V>: "))
        (if (= p "U") (setq *cfemap-perfil* "URBANO")
                       (setq *cfemap-perfil* "VIAS"))
        (initget "S N")
        (setq nombres (getkword "\nMostrar nombres de calles [S/N] <N>: "))
        (setq *cfemap-nombres-activos* (= nombres "S"))
        (initget "SI NO")
        (setq confirm (getkword "\nAplicar a la COPIA actual [SI/NO] <NO>: "))
        (if (/= confirm "SI")
          (cfemap:print "Cancelado sin cambios.")
          (progn
            (setq *cfemap-textmem* nil *cfemap-visitados* nil
                  *cfemap-movidos* 0 *cfemap-calles* 0
                  *cfemap-ocultos* 0 *cfemap-errores* 0 *cfemap-lineas0* 0)
            (cfemap:protect-paper)
            (cfemap:snapshot-layers)
            (cfemap:newlayer "CFE_MAPA_NOMBRES_CALLE" 7)
            (cfemap:newlayer "CFE_MAPA_TEXTOS_OCULTOS" 8)
            (cfemap:print "Revisando texto en Model y bloques insertados...")
            (cfemap:process-block "*Model_Space")
            (cfemap:apply-layers *cfemap-perfil*)
            (setq *cfemap-estado* T)
            (vl-cmdf "_.REGENALL")
            (cfemap:report)
            (cfemap:print (strcat "Listo: " (itoa *cfemap-movidos*)
                     " textos tratados; " (itoa *cfemap-calles*)
                     " posibles nombres de calle."))
            (if (> *cfemap-lineas0* 0)
              (cfemap:print (strcat "ADVERTENCIA: hay "
                (itoa *cfemap-lineas0*)
                " lineas/arcos de layer 0 en bloques del mapa."
                " Puede quedar cartografia mezclada: revisar visualmente."))
            )
            (cfemap:print "Tras validar, use SAVEAS para guardar el DWG limpio.")
            (cfemap:print "Si no es correcto use CFEMAPA_RESTAURAR o cierre sin guardar.")
          )
        )
      )
    )
  )
  (princ)
)
(defun c:CFEMAPA_NOMBRES (/ r)
  (if (not *cfemap-estado*)
    (cfemap:print "Primero ejecute CFEMAPA_LIMPIAR.")
    (progn
      (setq *cfemap-nombres-activos* (not *cfemap-nombres-activos*))
      (cfemap:layeron "CFE_MAPA_NOMBRES_CALLE" *cfemap-nombres-activos*)
      (vl-cmdf "_.REGENALL")
      (cfemap:report)
      (cfemap:print (strcat "Nombres calle: "
              (if *cfemap-nombres-activos* "VISIBLES" "OCULTOS")))
    )
  )
  (princ)
)
(defun c:CFEMAPA_RESTAURAR (/ item data result)
  (if (not *cfemap-estado*)
    (cfemap:print "No hay cambios activos en esta sesion.")
    (progn
      (foreach item *cfemap-textmem*
        (setq data (entget (car item)))
        (if (and data (assoc 8 data))
          (vl-catch-all-apply 'entmod
            (list (subst (cons 8 (cdr item)) (assoc 8 data) data)))
        )
      )
      (foreach item *cfemap-capasmem*
        (cfemap:layeron (car item) (cdr item))
      )
      (cfemap:layeron "CFE_MAPA_NOMBRES_CALLE" nil)
      (cfemap:layeron "CFE_MAPA_TEXTOS_OCULTOS" nil)
      (setq *cfemap-estado* nil *cfemap-textmem* nil
            *cfemap-capasmem* nil)
      (vl-cmdf "_.REGENALL")
      (cfemap:print "Restauradas las capas y los textos originales de esta sesion.")
      (cfemap:print "Las dos capas de control vacias pueden permanecer en el DWG.")
    )
  )
  (princ)
)
(defun c:CFEMAPA_RESUMEN ()
  (if *cfemap-estado*
    (cfemap:report)
    (cfemap:print "No hay limpieza activa. Ejecute CFEMAPA_LIMPIAR."))
  (princ)
)
(princ "\nCFE MAPA LIMPIO 3B cargado. Comandos: CFEMAPA_LIMPIAR, CFEMAPA_NOMBRES, CFEMAPA_RESTAURAR, CFEMAPA_RESUMEN.")
(princ)
