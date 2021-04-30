(sequence (declare i 2) (while (< (lookup i) 10) (sequence (assign (varloc i) (- (+ 3 (lookup i)) 1)))) (print (lookup i)))
