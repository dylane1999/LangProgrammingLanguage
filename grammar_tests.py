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

# term = parser.parse("var x = 1; if (x == 1){ var x = 2; print x;} print x; ", "program")  #DONE
#         term = parser.parse("var a = 1; var b = 1; var c = 1 ; var d =
#                 term = parser.parse("if (10 > 2 == 1){ print 1; }", "program")1 ; var e = 1 ; var f = 1 ; if (a ==1 && b == 1 || c ==1 && d ==1  || e ==1 && f ==1){ print 1; }", "program")


# 1+2*b;
#  2-(i-1)+56; parses i-1 incorrect
#   2-i-2;
    # 1-1-i;
# 2-(i-1)+(b*31);

# print 24 / 3 / 2 / 1 / (24 * 0);
# print (1 + 2) + (c - 8); # 59
# print (1 + 2) - (4 + d); # -129

# print (1 + 2) + (4 - d); # -121
# print (1 + 2) + (4 - 8); # -1
# print (1 + 2) + (4 + d); # 135
 # print (1 + b) + (c + d); # 225
# print (a + 2) + (4 + 8); # 30
# print (a + 2) + (4 + d); # 150
# print (a + 2) + (c + 8); # 90
# print (a + 2) + (c + d); # 210
# print (a + b) + (4 + 8); # 60
# print (a + b) + (4 + d); # 180
# print (a + b) + (c + 8); # 120
# print (a + b) + (c + d); # 240
# print (1 + 2) + (4 - 8); # -1



# var a = 16;
# var b = 32;
# var c = 64;
# var d = 128;
# print (1 + 2) - (4 - 8); # 7
# print (1 + 2) + (4 + 8); # 15
# print (1 + 2) + (4 + d); # 135
# print (1 + 2) + (c + 8); # 75
# print (1 + 2) + (c + d); # 195
# print (1 + b) + (4 + 8); # 45
# print (1 + b) + (4 + d); # 165
# print (1 + b) + (c + 8); # 105
# print (1 + b) + (c + d); # 225
# print (a + 2) + (4 + 8); # 30
# print (a + 2) + (4 + d); # 150
# print (a + 2) + (c + 8); # 90
# print (a + 2) + (c + d); # 210
# print (a + b) + (4 + 8); # 60
# print (a + b) + (4 + d); # 180
# print (a + b) + (c + 8); # 120
# print (a + b) + (c + d); # 240
# print (1 + 2) + (4 - 8); # -1
# print (1 + 2) + (4 - d); # -121
# print (1 + 2) + (c - 8); # 59
# print (1 + 2) + (c - d); # -61
# print (1 + b) + (4 - 8); # 29
# print (1 + b) + (4 - d); # -91
# print (1 + b) + (c - 8); # 89
# print (1 + b) + (c - d); # -31
# print (a + 2) + (4 - 8); # 14
# print (a + 2) + (4 - d); # -106
# print (a + 2) + (c - 8); # 74
# print (a + 2) + (c - d); # -46
# print (a + b) + (4 - 8); # 44
# print (a + b) + (4 - d); # -76
# print (a + b) + (c - 8); # 104
# print (a + b) + (c - d); # -16
# print (1 + 2) - (4 + 8); # -9
# print (1 + 2) - (4 + d); # -129
# print (1 + 2) - (c + 8); # -69
# print (1 + 2) - (c + d); # -189
# print (1 + b) - (4 + 8); # 21
# print (1 + b) - (4 + d); # -99
# print (1 + b) - (c + 8); # -39
# print (1 + b) - (c + d); # -159
# print (a + 2) - (4 + 8); # 6
# print (a + 2) - (4 + d); # -114
# print (a + 2) - (c + 8); # -54
# print (a + 2) - (c + d); # -174
# print (a + b) - (4 + 8); # 36
# print (a + b) - (4 + d); # -84
# print (a + b) - (c + 8); # -24
# print (a + b) - (c + d); # -144
# print (1 + 2) - (4 - 8); # 7
# print (1 + 2) - (4 - d); # 127
# print (1 + 2) - (c - 8); # -53
# print (1 + 2) - (c - d); # 67
# print (1 + b) - (4 - 8); # 37
# print (1 + b) - (4 - d); # 157
# print (1 + b) - (c - 8); # -23
# print (1 + b) - (c - d); # 97
# print (a + 2) - (4 - 8); # 22
# print (a + 2) - (4 - d); # 142
# print (a + 2) - (c - 8); # -38
# print (a + 2) - (c - d); # 82
# print (a + b) - (4 - 8); # 52
# print (a + b) - (4 - d); # 172
# print (a + b) - (c - 8); # -8
# print (a + b) - (c - d); # 112
# print (1 - 2) + (4 + 8); # 11
# print (1 - 2) + (4 + d); # 131
# print (1 - 2) + (c + 8); # 71
# print (1 - 2) + (c + d); # 191
# print (1 - b) + (4 + 8); # -19
# print (1 - b) + (4 + d); # 101
# print (1 - b) + (c + 8); # 41
# print (1 - b) + (c + d); # 161
# print (a - 2) + (4 + 8); # 26
# print (a - 2) + (4 + d); # 146
# print (a - 2) + (c + 8); # 86
# print (a - 2) + (c + d); # 206
# print (a - b) + (4 + 8); # -4
# print (a - b) + (4 + d); # 116
# print (a - b) + (c + 8); # 56
# print (a - b) + (c + d); # 176
# print (1 - 2) + (4 - 8); # -5
# print (1 - 2) + (4 - d); # -125
# print (1 - 2) + (c - 8); # 55
# print (1 - 2) + (c - d); # -65
# print (1 - b) + (4 - 8); # -35
# print (1 - b) + (4 - d); # -155
# print (1 - b) + (c - 8); # 25
# print (1 - b) + (c - d); # -95
# print (a - 2) + (4 - 8); # 10
# print (a - 2) + (4 - d); # -110
# print (a - 2) + (c - 8); # 70
# print (a - 2) + (c - d); # -50
# print (a - b) + (4 - 8); # -20
# print (a - b) + (4 - d); # -140
# print (a - b) + (c - 8); # 40
# print (a - b) + (c - d); # -80
# print (1 - 2) - (4 + 8); # -13
# print (1 - 2) - (4 + d); # -133
# print (1 - 2) - (c + 8); # -73
# print (1 - 2) - (c + d); # -193
# print (1 - b) - (4 + 8); # -43
# print (1 - b) - (4 + d); # -163
# print (1 - b) - (c + 8); # -103
# print (1 - b) - (c + d); # -223
# print (a - 2) - (4 + 8); # 2
# print (a - 2) - (4 + d); # -118
# print (a - 2) - (c + 8); # -58
# print (a - 2) - (c + d); # -178
# print (a - b) - (4 + 8); # -28
# print (a - b) - (4 + d); # -148
# print (a - b) - (c + 8); # -88
# print (a - b) - (c + d); # -208
# print (1 - 2) - (4 - 8); # 3
# print (1 - 2) - (4 - d); # 123
# print (1 - 2) - (c - 8); # -57
# print (1 - 2) - (c - d); # 63
# print (1 - b) - (4 - 8); # -27
# print (1 - b) - (4 - d); # 93
# print (1 - b) - (c - 8); # -87
# print (1 - b) - (c - d); # 33
# print (a - 2) - (4 - 8); # 18
# print (a - 2) - (4 - d); # 138
# print (a - 2) - (c - 8); # -42
# print (a - 2) - (c - d); # 78
# print (a - b) - (4 - 8); # -12
# print (a - b) - (4 - d); # 108
# print (a - b) - (c - 8); # -72
# print (a - b) - (c - d); # 48