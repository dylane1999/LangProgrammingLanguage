(sequence (declare a (|| 2 (< (&& 1 2) (! (<= 3 (* 2 3)))))) (declare b (! (== (lookup a) (!= (>= 2 3) (> 1 0))))) (print (lookup a)) (print (lookup b)))