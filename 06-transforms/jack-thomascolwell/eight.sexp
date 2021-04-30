(sequence (declare x (function (parameters a) (sequence (print (+ (+ (lookup a) 1) (* 2 3)))))) (call (lookup x) (arguments (+ 1 (* 2 3)))) )
