(sequence
    (declare x 0)
    (print (* (* (+ (- (lookup x) 1) 1) (- (- 1 1) (lookup x))) (- (- 0 1) (lookup x)))))