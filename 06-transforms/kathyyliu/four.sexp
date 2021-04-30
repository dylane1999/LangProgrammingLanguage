(sequence
    (declare x 1)
    (ifelse (>= (+ 1 (/ 4 2)) (- (lookup x) (+ 1 (* 3 (lookup x))))) 
        (sequence (print 1))
        (sequence (print 0)))
)