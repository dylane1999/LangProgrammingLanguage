(sequence (declare hat (function (parameters cat) (sequence (return (- (+ (+ 1 (lookup cat)) 2) (* 3 (lookup cat))))))) (print (call (lookup hat) (arguments 2))))
