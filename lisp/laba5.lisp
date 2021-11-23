(ql:quickload "cl-csv")

(defun readcsv ()
  (cl-csv:read-csv #P"data.csv"))

(defparameter *dataset* (cl-csv:read-csv #P"data.csv"))

(defun math_expectation (x)
  (defun sumup (x)
    (if (equal x nil) 0
        (+ (car x) (sumup (cdr x)))
        )
    )
  (if
   (equal x nil) 0
   (/(sumup x) (list-length x))
   )
  )

(defun math_expectation2 (x)
  (defun sumup (x)
    (if (equal x nil) 0
        (+ (parse-integer (car (cddar x)) ) (sumup (cdr x)))
        )
    )
  (if
   (equal x nil) 0
   (float (/(sumup x) (list-length x)))
   )
  )


(defun math_expectation_dispersion (x)
  (defun sumup (x)
    (if (equal x nil) 0
        (+ (parse-integer (car (cdar x)) ) (sumup (cdr x)))
        )
    )
  (if
   (equal x nil) 0
   (float (/(sumup x) (list-length x)))
   )
  )

(defparameter *score_math_expect* (math_expectation_dispersion *dataset*) )

(defun dispercion (x)
  (defun sumup (x)
    (if (equal x nil) 0
        (+ (square (- (parse-integer (car (cdar x)) ) *score_math_expect*)) (sumup (cdr x)))
        )
    )
  (if
   (equal x nil) 0
   (float (/(sumup x) (list-length x)))
   )
  )

(defun output_result ()
  (print "1a")
  (princ "Math expectation time: ")
  (write (math_expectation2 *dataset*))
  (print "1b")
  (princ "Dispersion score: ")
  (write (dispercion *dataset*)))
