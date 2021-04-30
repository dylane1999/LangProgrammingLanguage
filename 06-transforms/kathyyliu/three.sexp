(sequence
    (declare x 1)
    (declare y 2)
    (declare z 3)
    (print (+ (+ (- (- (- 4 (lookup x)) (lookup y)) (lookup z)) 5) 6))
    (print (- (+ (- (+ (- 4 (lookup x)) 5) (lookup y)) 6) (lookup z)))
)