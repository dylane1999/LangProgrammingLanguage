(sequence
    (print (- (+ (* 1 2) 1) 3))
    (declare x 2)
    (print (- (+ (* 1 (lookup x)) 1) 3))
)