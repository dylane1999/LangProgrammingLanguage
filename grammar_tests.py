# # integer tests
# test_parse(parser, "3", "integer", Parse(3, 1))
# test_parse(parser, "0", "integer", Parse(0, 1))
# test_parse(parser, "100", "integer", Parse(100, 3))
# test_parse(parser, "2021", "integer", Parse(2021, 4))
# test_parse(parser, "b", "integer", self.FAIL)
# test_parse(parser, "", "integer", self.FAIL)
# # addition tests
# test_parse(parser, "b", "addition", self.FAIL)
# test_parse(parser, "", "addition", self.FAIL)
# test_parse(parser, "3-", "addition", Parse(3, 1))
# test_parse(parser, "3++", "addition", Parse(3, 1))
# test_parse(parser, "3+4", "addition", Parse(7, 3))
# test_parse(parser, "2020+2021", "addition", Parse(4041, 9))
# test_parse(parser, "0+0", "addition", Parse(0, 3))
# test_parse(parser, "1+1+", "addition", Parse(2, 3))
# test_parse(parser, "1+1+-", "addition", Parse(2, 3))
# test_parse(parser, "0+0+0+0+0", "addition", Parse(0, 9))
# test_parse(parser, "42+0", "addition", Parse(42, 4))
# test_parse(parser, "40+42", "addition", Parse(82, 5))
# test_parse(parser, "123+234+456", "addition", Parse(813, 11))
# # parenthesis test cases
# test_parse(parser, "(0)", "parenthesis", Parse(0, 3))
# test_parse(parser, "(0+0)", "parenthesis", Parse(0, 5))
# test_parse(parser, "(1+2)", "parenthesis", Parse(3, 5))
# test_parse(parser, "(1+2+3)", "parenthesis", Parse(6, 7))
# test_parse(parser, "4+(1+2+3)", "addition", Parse(10, 9))
# test_parse(parser, "(1+2+3)+5", "addition", Parse(11, 9))
# test_parse(parser, "4+(1+2+3)+5", "addition", Parse(15, 11))
# test_parse(parser, "3+4+(5+6)+9", "addition", Parse(27, 11))
# # end to end test
# test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "addition", Parse(27, 25))
# # #spaces test
# test_parse(parser, "3 ", "integer", Parse(3, 2))
# test_parse(parser, " 3", "integer", Parse(3, 2))
# test_parse(parser, " 3 ", "integer", Parse(3, 3))
# test_parse(parser, "  3  ", "integer", Parse(3, 5))
# test_parse(parser, "    3  ", "integer", Parse(3, 7))
# test_parse(parser, "  3  +  4  ", "addition", Parse(7, 11))
# test_parse(parser, "(  3  +  4  )", "addition", Parse(7, 13))
# test_parse(parser, "   (  3  +  4  )", "addition", Parse(7, 16))
# test_parse(parser, "   (     3  +  4  )", "addition", Parse(7, 19))
# test_parse(parser, "3+    4       +5   +    5 +     9", "addition", Parse(26, 33))
# test_parse(parser, "3 + + ", "addition", Parse(3, 2))
# test_parse(parser, "3+    4       + (5   +   5  +     9)  ", "addition",
#            Parse(26, 38))  # the addition fails leading to a fail in index length
# # #subtraction test
# test_parse(parser, "5-3", "add|sub", Parse(2, 3))
# test_parse(parser, "3-5", "add|sub", Parse(-2, 3))
# test_parse(parser, "(5-6)-9", "add|sub", Parse(-10, 7))
# test_parse(parser, " (5-6)-9 ", "add|sub", Parse(-10, 9))
# test_parse(parser, " (5-6) -9 ", "add|sub", Parse(-10, 10))
#
# # retry addition as artithmetic
# test_parse(parser, "b", "add|sub", self.FAIL)
# test_parse(parser, "", "add|sub", self.FAIL)
# test_parse(parser, "3-", "add|sub", Parse(3, 1))
# test_parse(parser, "3++", "add|sub", Parse(3, 1))
# test_parse(parser, "3+4", "add|sub", Parse(7, 3))
# test_parse(parser, "2020+2021", "add|sub", Parse(4041, 9))
# test_parse(parser, "0+0", "add|sub", Parse(0, 3))
# test_parse(parser, "1+1+", "add|sub", Parse(2, 3))
# test_parse(parser, "1+1+-", "add|sub", Parse(2, 3))
# test_parse(parser, "0+0+0+0+0", "add|sub", Parse(0, 9))
# test_parse(parser, "42+0", "add|sub", Parse(42, 4))
# test_parse(parser, "40+42", "add|sub", Parse(82, 5))
# test_parse(parser, "123+234+456", "add|sub", Parse(813, 11))
# test_parse(parser, "5*234*456", "mult|div", Parse(813, 11))

# # parenthesis test cases
# test_parse(parser, "(0)", "parenthesis", Parse(0, 3))
# test_parse(parser, "(0+0)", "parenthesis", Parse(0, 5))
# test_parse(parser, "(1+2)", "parenthesis", Parse(3, 5))
# test_parse(parser, "(1+2+3)", "parenthesis", Parse(6, 7))
# test_parse(parser, "4+(1+2+3)", "add|sub", Parse(10, 9))
# test_parse(parser, "(1+2+3)+5", "add|sub", Parse(11, 9))
# test_parse(parser, "4+(1+2+3)+5", "add|sub", Parse(15, 11))
# test_parse(parser, "3+4+(5+6)+9", "add|sub", Parse(27, 11))
#
# # end to end test
# test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "addition", Parse(27, 25))
#
# # addition and subtraction test
# test_parse(parser, "3-5+1", "add|sub", Parse(-1, 5))
# test_parse(parser, "(5+7)-6+2", "add|sub", Parse(8, 9))
# test_parse(parser, "(  5+7)-6+  2", "add|sub", Parse(8, 13))
# test_parse(parser, "(5+(4+5))", "parenthesis", Parse(14, 9))
# test_parse(parser, "5*5", "mult|div", Parse(25, 3))
# test_parse(parser, "1   *  17   ", "mult|div", Parse(17, 12))
# test_parse(parser, "5*10*2", "mult|div", Parse(100, 6))
# test_parse(parser, "5/5", "mult|div", Parse(1, 3))
# test_parse(parser, "5+5/5", "add|sub", Parse(6, 5))
# test_parse(parser, "5*5/5", "mult|div", Parse(5, 5))
# test_parse(parser, "(5/5)", "mult|div", Parse(1, 5))


# test_parse(parser, "3+5+5*5", "add|sub", Parse(33, 9))
# term = parser.parse("2+2*2", "add|sub")
# print(term.to_string())
# term = parser.parse("    2*     2+2", "add|sub")
# term = parser.parse("2\n *2\n #fkldsalfja  \n+2 # asdfdesfklfkljsdk", "add|sub")
# term = parser.parse("print 5+5*2;", "print_statement")
# test_parse(parser, "(5*5)+3+5", "add|sub", Parse(33, 9))
#
# term = parser.parse("var testVar = 5+5*2;", "declaration_statement")
#
# x = interpreter.execute(term)
# term = parser.parse("var testVar = 5+5*2;", "declaration_statement")
#
# x = interpreter.execute(term)
# print(x)


# term = parser.parse("var foo = 5+5*2; print foo; var bar = foo; print bar;", "program") #6
# print(term.to_string())
# term = parser.parse("print foo;; print foo;", "program") #7
# print(term.to_string())
# term = parser.parse("var foo = 5+5*2; print foo; var bar = 5; print bar;", "program") #8
# print(term.to_string())
# term = parser.parse("var  = 5+5*2;", "declaration_statement")  # test for no variable
# print(term.to_string())

# var a = 1; var b = 1; var c = 1 ; var d = 1 ; var e = 1 ; var f = 1 ; if ((a ==1 && b == 1) && (c ==1 && d ==1 ) && (e ==1 && f ==1)){ print 1; }

