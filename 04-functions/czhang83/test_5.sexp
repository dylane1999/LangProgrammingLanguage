(sequence (declare a (function (parameters) (sequence))) (declare b (function (parameters) (sequence))) (declare c (lookup a)) (print (== (lookup a) (lookup b))) (print (== (lookup a) (lookup c))) (print (== (lookup b) (lookup c))) (print (== (call (lookup a) (arguments)) (call (lookup b) (arguments)))))