(sequence
    (declare x 2)
    (print (- 5 
        (- (+ (lookup x) 2) 
            (- (* 3 1) 
                (- (- 0 (lookup x)) 
                    (- 1 (* (lookup x) 2)))))))
)