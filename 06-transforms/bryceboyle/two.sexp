(sequence (declare printer (function (parameters b) (sequence (if (== (lookup b) 14) (sequence (print (lookup b))))))) (call (lookup printer) (arguments (- (+ (* 2 7) 1) 1))))
