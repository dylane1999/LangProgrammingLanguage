(sequence (declare a (function (signature int) (parameters) (sequence (return 3)))) (declare b (function (signature func) (parameters) (sequence (return (function (parameters) (sequence)))))) (print (call (lookup a) (arguments))) (print (call (lookup b) (arguments))) (declare c (function (signature func) (parameters) (sequence (return 3)))) (print (call (lookup c) (arguments))))