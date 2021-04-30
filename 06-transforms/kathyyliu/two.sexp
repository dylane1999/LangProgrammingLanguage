(sequence
    (declare x 2)
    (print (- (- (- (- (+ (+ (+ (+ 0 1) 2) 3) (lookup x)) 3) 2) 1) 0))
    (print (+ (+ (+ (+ (+ (+ (+ (+ 0 0) 0) 0) (lookup x)) 0) 0) 0) 0))
    (print (- (- (- (- (+ (- (- (- 0 0) 0) 0) (lookup x)) 0) 0) 0) 0))
)