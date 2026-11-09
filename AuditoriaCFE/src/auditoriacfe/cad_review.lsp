; A4.2.2. Elementos de revisión en Paper Space.
(defun datra:review-admin (date author reviewer / sel entity a d entry seen values)
  (setq sel (ssget "_X" (list '(0 . "INSERT") '(2 . "DATRA_CAJETIN_A1") (cons 410 datra:*layout*)))
        values (list (cons "FECHA" date) (cons "ELABORO" author) (cons "REVISO" reviewer)
                     '("CRS" . "EPSG:32611 DIAGNOSTICO") '("ESTADO" . "PRELIMINAR")))
  (if (or (not sel) (/= 1 (sslength sel))) (datra:fail "Cajetin de revision ausente"))
  (setq entity (ssname sel 0) a (entnext entity))
  (while (and a (= "ATTRIB" (cdr (assoc 0 (setq d (entget a))))))
    (if (setq entry (assoc (cdr (assoc 2 d)) values))
      (progn
        (if (not (entmod (subst (cons 1 (cdr entry)) (assoc 1 d) d)))
          (datra:fail "No se pudo escribir el cajetin de revision"))
        (setq seen (cons (car entry) seen))))
    (setq a (entnext a)))
  (if (/= (length seen) (length values)) (datra:fail "Campos de revision incompletos"))
  (entupd entity))

(defun datra:review-legend (/ sel i e d p item)
  (setq sel (ssget "_X" (list '(8 . "DATRA_A1_SIMBOLOS,DATRA_A1_TEXTO")
                            (cons 410 datra:*layout*))) i 0)
  (if sel (repeat (sslength sel)
    (setq e (ssname sel i) i (1+ i) d (entget e) p (cdr (assoc 10 d)))
    (if (or (member (cdr (assoc 1 d)) '("RUTA CONFIRMADA" "RAMAL CONFIRMADO"))
            (and (= (cdr (assoc 8 d)) "DATRA_A1_SIMBOLOS") p
                 (<= 707.0 (car p)) (<= (car p) 719.0)
                 (<= 322.0 (cadr p)) (<= (cadr p) 391.0)))
      (entdel e))))
  (foreach item '(("POSTE" 391.0 6.6666667) ("CAJA_EMP" 374.0 6.6666667) ("EXCEDENTE" 357.0 4.6153846))
    (datra:tag (datra:make (list '(0 . "INSERT") (cons 2 (strcat "DATRA_" (car item) "_V1"))
      (cons 8 (strcat "DATRA_" (car item))) (list 10 713.0 (cadr item) 0.0)
      (cons 41 (caddr item)) (cons 42 (caddr item)) (cons 43 (caddr item))
      '(67 . 1) (cons 410 datra:*layout*))) (strcat "LEYENDA_" (car item))))
  (datra:text "LEYENDA_P05" "DATRA_A4_REVISION" '(707.0 337.0 0.0) 2.5 "SIN RUTAS NI RAMALES CONFIRMADOS" T))

(defun datra:review-line (x1 y1 x2 y2)
  (datra:tag (datra:make (list '(0 . "LINE") '(8 . "DATRA_A4_REVISION")
    (list 10 x1 y1 0.0) (list 11 x2 y2 0.0) '(67 . 1) (cons 410 datra:*layout*))) "TABLA_CFE_REJILLA"))

(defun datra:review-table (rows / y row values x cell)
  (datra:text "TABLA_CFE_TITULO" "DATRA_A4_REVISION" '(151.0 61.0 0.0) 3.2
    "RESUMEN TECNICO DE AUDITORIA - CAMPOS ACREDITADOS" T)
  (setq y 54.0)
  (repeat 6 (datra:review-line 150.0 y 410.0 y) (setq y (- y 7.0)))
  (foreach x '(150.0 210.0 272.0 337.0 410.0) (datra:review-line x 19.0 x 54.0))
  (setq y 49.0)
  (foreach row (cons '("CONCEPTO" "INVENTARIO" "REPRESENTADOS" "NO DIBUJADOS") rows)
    (setq values row)
    (foreach x '(153.0 213.0 275.0 340.0)
      (setq cell (car values) values (cdr values))
      (datra:text "TABLA_CFE_CELDA" "DATRA_A4_REVISION" (list x y 0.0) 2.7
        (if (numberp cell) (itoa cell) cell) T))
    (setq y (- y 7.0)))
  (datra:text "TABLA_CFE_ANEXO" "DATRA_A4_REVISION" '(427.0 49.0 0.0) 2.7
    "COORDENADAS EN GRADOS DECIMALES: ANEXO DIGITAL CSV" T)
  (datra:text "TABLA_CFE_AMBITO" "DATRA_A4_REVISION" '(427.0 41.0 0.0) 2.7
    "Inventario identificado, incluido lo no dibujado." T)
  (datra:text "TABLA_CFE_ESTADO" "DATRA_A4_REVISION" '(427.0 33.0 0.0) 2.7
    "Revision documental - no publicable como FINAL." T)
  (datra:text "TABLA_CFE_VISIBILIDAD" "DATRA_A4_REVISION" '(427.0 25.0 0.0) 2.7
    "Visibilidad 300 m. Conteos del cajetin: dibujados." T))

(defun datra:review (date author reviewer rows)
  (setvar "CTAB" datra:*layout*)
  (datra:layer "DATRA_A4_REVISION" 7)
  (datra:review-admin date author reviewer)
  (datra:review-legend)
  (if (= datra:*layout* datra:*main-layout*) (datra:review-table rows)))
(princ)
