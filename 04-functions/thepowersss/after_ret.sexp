(sequence (declare a (function (parameters) (sequence (print 1) (return 2) (print 3)))) (print (call (lookup a) (arguments))))