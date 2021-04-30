(sequence (if (+ 1 (* 2 3)) (sequence (print (+ 1 (* 2 3))))) (declare x 0) (while (+ (+ (lookup x) 1) (* 2 3)) (sequence (print (+ 1 (* 2 3))) (assign (varloc x) (- 0 7)))))
