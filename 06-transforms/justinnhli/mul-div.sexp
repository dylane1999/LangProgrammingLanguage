(sequence
    (declare a (* (* (* (* (* (* (* (* (* 1 2) 3) 4) 5) 6) 7) 8) 9) 10))
    (print (lookup a))
    (declare b (/ (/ (/ (/ (/ (/ (/ (/ (/ (/ (lookup a) 10) 9) 8) 7) 6) 5) 4) 3) 2) 1))
    (print (lookup b)) 
    (declare c (/ (/ (/ (/ (/ (/ (/ (/ (/ (/ 3628800 10) 9) 8) 7) 6) 5) 4) 3) 2) 1))
    (print (lookup c)))
