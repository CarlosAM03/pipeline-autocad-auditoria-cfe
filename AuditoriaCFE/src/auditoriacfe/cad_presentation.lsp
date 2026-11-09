; Presentacion A1 ADR-002. Solo papel y camaras.
(defun datra:pages-check (names owner / n marker)
  (setq datra:*owner* owner)
  (setq datra:*main-layout* (car names))
  (foreach n (datra:layouts)
    (if (and (wcmatch n "DATRA_A4_*") (/= n datra:*main-layout*))
      (progn
        (setq marker (ssget "_X" (list '(0 . "TEXT") '(8 . "DATRA_A4_MARCA")
                                  (cons 410 n) '(-3 ("DATRA_CFE")))))
        (if (or (not (member n names)) (not marker) (/= (sslength marker) 1)
                (not (datra:owned (ssname marker 0))))
          (datra:fail "Layout reservado A4 ajeno o plan distinto: usar copia nueva"))))))

(defun datra:prepare-pages (names / name)
  ; Copiar marco antes de añadir títulos o marcas de la vista general.
  (foreach name names
    (if (not (member name (datra:layouts)))
      (progn
        (command "_.-LAYOUT" "_Copy" datra:*main-layout* name)
        (if (not (member name (datra:layouts))) (datra:fail "No se pudo copiar layout DATRA"))
        (setq datra:*new-layouts* (cons name datra:*new-layouts*))))))

(defun datra:page (name x y scale)
  (setq datra:*layout* name)
  (datra:camera x y scale)
  (datra:layer "DATRA_A4_MARCA" 7)
  (datra:layer "DATRA_A4_ETIQUETA" 7)
  (datra:layer "DATRA_A4_LIDER" 8))

(defun datra:sheet-attributes (audit number / selection e a d pair seen values)
  (setq selection (ssget "_X" (list '(0 . "INSERT") '(2 . "DATRA_CAJETIN_A1")
                         (cons 410 datra:*layout*)))
        values (list '("NOMBRE_PLANO" . "AUDITORIA PRELIMINAR")
                     (cons "AUDITORIA" audit) '("ESCALA" . "VER HOJA") (cons "NUM_PLANO" number)))
  (if (or (not selection) (/= (sslength selection) 1))
    (datra:fail "Cajetin DATRA requerido para numeracion A4"))
  (setq e (ssname selection 0) a (entnext e))
  (while (and a (= "ATTRIB" (cdr (assoc 0 (setq d (entget a))))))
    (setq pair (assoc (cdr (assoc 2 d)) values))
    (if pair
      (progn
        (if (not (entmod (subst (cons 1 (cdr pair)) (assoc 1 d) d)))
          (datra:fail "No se pudo actualizar cajetin A4"))
        (setq seen (cons (car pair) seen))))
    (setq a (entnext a)))
  (if (/= (length seen) (length values)) (datra:fail "Faltan atributos de presentacion A4"))
  (entupd e))

(defun datra:sheet-title (audit num total kind n scale / number)
  (setq number (strcat (rtos num 2 0) "/" (rtos total 2 0)))
  (datra:sheet-attributes audit number)
  (datra:text "HOJA_A4" "DATRA_A4_MARCA" '(150.0 570.0 0.0) 3.0
    (strcat "HOJA " number "  " kind
      "  |  Etiquetas primarias: " (rtos n 2 0) "  |  " (rtos scale 2 3) " unidades Model/mm") T)
  (datra:text "ACLARACION_A4" "DATRA_CONTROL" '(470.0 551.0 0.0) 2.3
    "EXCEDENTE EN MAPA: CIRCULO CON BARRA" T)
  (if (/= datra:*layout* datra:*main-layout*)
    (progn
      (datra:text "ESTADO" "DATRA_CONTROL" '(150.0 557.0 0.0) 3.0 datra:*mode* T)
      (datra:text "NOTA_A4" "DATRA_CONTROL" '(150.0 550.0 0.0) 2.4
        "Conteos del cajetin: inventario total de la auditoria. Lideres: anotaciones, no conexiones." T))))

(defun datra:annotation (id geo label ax ay ex ey x y h hi / entity)
  (setq entity (datra:make (list '(0 . "LINE") '(8 . "DATRA_A4_LIDER")
    (list 10 ax ay 0.0) (list 11 ex ey 0.0))))
  (datra:tag entity id)
  (datra:text id "DATRA_A4_ETIQUETA" (list x y 0.0) h geo T)
  (if (> hi 0)
    (datra:text id "DATRA_A4_ETIQUETA" (list x (+ y h 1.0) 0.0) hi label T)))
(princ)
