
class Parse:

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __equals__(self, other):
        return (
                isinstance(other, Parse)
                and self.value == other.value
                and self.index == other.index
        )

    def __str__(self):
        return 'Parse(value={}, index{})'.format(self.value, self.index)

class Parser:

    FAIL = Parse(0, -1)

    def parse(self, string, term):
        return self.__parse(string, 0, term)

    def __parse(self, string, index, term):     # main parse wrapper that calls each item to be parsed @each index
        if index >= len(string):
            return self.FAIL
        elif term == "integer":
            return self.__parse_integer(string, index)
        elif term == "addition":
            return self.__parse_addition_expression(string, index)
        elif term == "subtraction":
            return self.__parse_subtraction_expression(string, index)
        elif term == "operand":
            return self.__parse_operand(string, index)
        elif term == "parenthesis":
            return self.__parse_parenthesis(string, index)
        elif term == "space":
            return self.__parse_spaces(string, index)
        elif term == "add|sub":
            return self.__parse_add_sub_expression(string, index)
        elif term == "mult|div":
            return self.__parse_mult_div_expression(string, index)
        else:
            raise AssertionError("Unexpected Term " + term)

    def __parse_operand(self, string, index):
        parse = self.__parse(string, index, "integer")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string,index, "parenthesis")
        if parse != self.FAIL:
            return parse
        return self.FAIL  # may need to add index here to return

    def __parse_integer(self, string, index):
        parse = self.__parse(string, index, "space")  # checks for spaces at start of integer and adds to index
        if parse != self.FAIL:
            index = parse.index     # if parse of spaces was success add to index
        parsed = ""
        while index < len(string) and string[index].isdigit():  # loops through and adds to parsed while still a digit
            parsed += string[index]
            index += 1
        if parsed == '':
            return self.FAIL
        parse = self.__parse(string, index, "space")        # checks for spaces at end of integer and adds to index
        if parse != self.FAIL:
            index = parse.index     # if parse of spaces was success add to index
        return Parse(int(parsed), index)  # returns the parsed int

    def __parse_spaces(self, string, index):
        parsed = ""
        while index < len(string) and string[index] == " ":  # loops through and adds to parsed while still a digit
            parsed += string[index]
            index += 1
        if parsed == "":
            return self.FAIL
        return Parse(parsed, index)

    def __parse_addition_expression(self, string, index): #  @todo add a parse for mult and div expression before and after
        parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
        if parse != self.FAIL:
            index = parse.index
        result = 0
        parse = self.__parse(string, index, "operand")  # parses the addition expression starting at the index given
        if parse == self.FAIL:
            return self.FAIL
        result = parse.value
        index = parse.index
        while index < len(string) and parse != self.FAIL:
            if string[index] != "+":  # parse + and if not then fail
                parse = self.FAIL
                break
            parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "+"
            if parse == self.FAIL:
                parse = self.FAIL
                break
            result += parse.value
            index = parse.index
        return Parse(result, index)

    def __parse_subtraction_expression(self, string, index):
        parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
        if parse != self.FAIL:
            index = parse.index
        result = 0
        parse = self.__parse(string, index, "operand")  # parses the subtraction expression starting at the index given
        if parse == self.FAIL:
            return self.FAIL
        result = parse.value
        index = parse.index
        while index < len(string) and parse != self.FAIL:
            if string[index] != "-":  # parse + and if not then fail
                parse = self.FAIL
                break
            parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "+"
            if parse == self.FAIL:
                parse = self.FAIL
                break
            result -= parse.value
            index = parse.index
        return Parse(result, index)

    def __parse_add_sub_expression(self, string, index):  # addition & subtraction function
        '''
        add_sub_expression   = mul_div_expression ( opt_space add_sub_operator opt_space mul_div_expression )*;

        :param string:
        :param index:
        :return: Parse of add|sub expression
        '''
        parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
        if parse != self.FAIL:
            index = parse.index
        result = 0
        # parse = self.__parse(string, index, "operand")  # parses the expression starting at the index given @FIXME change to become multdiv experssion
        parse = self.__parse(string, index, "mult|div")  # parses the mult expression (if no expression returns int
        if parse == self.FAIL:
            return self.FAIL
        result = parse.value
        index = parse.index
        while index < len(string) and parse != self.FAIL:
            if string[index] != "-" and string[index] != "+":  # parse +|- and if not then fail
                parse = self.FAIL
                break
            # parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "+ / -"
            parse = self.__parse(string, parse.index + 1, "mult|div")  # parses the mult expression (if no expression returns int); jumps +1 because of the " +/-"
            if parse == self.FAIL:      # if operand was fail break
                parse = self.FAIL
                break
            if string[index] == "+":        # if the operation was addition +
                result += parse.value
            if string[index] == "-":        # if the operation was subtraction  -
                result -= parse.value
            index = parse.index
        return Parse(result, index)

    def __parse_mult_div_expression(self, string, index):  # parse multiplication and division
        '''
        mul_div_expression       = operand ( opt_space mul_div_operator opt_space operand )*;

        :param string:
        :param index:
        :return: Parse of mult|div expression
        '''
        parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
        if parse != self.FAIL:
            index = parse.index
        parse = self.__parse(string, index, "operand")  # parses the int at start of expression
        if parse == self.FAIL:
            return self.FAIL
        result = parse.value    # if not fail add result & index
        index = parse.index
        while index < len(string) and parse != self.FAIL:
            if string[index] != "*" and string[index] != "/":  # parse *|/ and if not then fail
                parse = self.FAIL
                break
            parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "* | /"
            if parse == self.FAIL:      # if operand was fail break
                parse = self.FAIL
                break
            if string[index] == "*":        # if the operation was mult *
                result *= parse.value
            if string[index] == "/":        # if the operation was divide  @FIXME cahnge to int division
                result //= parse.value
            index = parse.index
        return Parse(result, index)

    def __parse_parenthesis(self, string, index): # @todo add a parse for mult and div
        '''

        :param string:
        :param index:
        :return: Parsed parenthesized expression
        '''
        parse = self.__parse(string, index, "space")  # checks for spaces at start of parenthesis and adds to index
        if parse != self.FAIL:
            index = parse.index     # if parse of spaces was success add to index
        if string[index] != '(':        # check if the string starts with open parenthesis
            return self.FAIL
        parse = self.__parse(string, index + 1, "add|sub")     # parses the addition string inside the parenthesis
        if parse == self.FAIL:        # if addition is not in grammar fails
            return self.FAIL
        if string[parse.index] != ")": # checks char at end of addition string, if not a close paren, then fail
            return self.FAIL
        space_parse = self.__parse(string,  parse.index+1, "space")  # checks for spaces at end of parenthesis and adds to index
        if space_parse != self.FAIL:        #if spaces return with spaces index
            return Parse(parse.value, space_parse.index)
            index = parse.index     # if parse of spaces was success add to index

        return Parse(parse.value, parse.index+1)  # add one index to account for close paren


    def test(self):
        parser = Parser()
        # # integer tests
        test_parse(parser, "3", "integer", Parse(3, 1))
        test_parse(parser, "0", "integer", Parse(0, 1))
        test_parse(parser, "100", "integer", Parse(100, 3))
        test_parse(parser, "2021", "integer", Parse(2021, 4))
        test_parse(parser, "b", "integer", self.FAIL)
        test_parse(parser, "", "integer", self.FAIL)
        # addition tests
        test_parse(parser, "b", "addition", self.FAIL)
        test_parse(parser, "", "addition", self.FAIL)
        test_parse(parser, "3-", "addition", Parse(3,1))
        test_parse(parser, "3++", "addition", Parse(3,1))
        test_parse(parser, "3+4", "addition", Parse(7, 3))
        test_parse(parser, "2020+2021", "addition", Parse(4041, 9))
        test_parse(parser, "0+0", "addition", Parse(0, 3))
        test_parse(parser, "1+1+", "addition", Parse(2, 3))
        test_parse(parser, "1+1+-", "addition", Parse(2, 3))
        test_parse(parser, "0+0+0+0+0", "addition", Parse(0, 9))
        test_parse(parser, "42+0", "addition", Parse(42, 4))
        test_parse(parser, "40+42", "addition", Parse(82, 5))
        test_parse(parser, "123+234+456", "addition", Parse(813, 11))
        # parenthesis test cases
        test_parse(parser, "(0)", "parenthesis", Parse(0, 3))
        test_parse(parser, "(0+0)", "parenthesis", Parse(0, 5))
        test_parse(parser, "(1+2)", "parenthesis", Parse(3, 5))
        test_parse(parser, "(1+2+3)", "parenthesis", Parse(6, 7))
        test_parse(parser, "4+(1+2+3)", "addition", Parse(10, 9))
        test_parse(parser, "(1+2+3)+5", "addition", Parse(11, 9))
        test_parse(parser, "4+(1+2+3)+5", "addition", Parse(15, 11))
        test_parse(parser, "3+4+(5+6)+9", "addition", Parse(27, 11))
        # end to end test
        test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "addition", Parse(27, 25))
        # #spaces test
        test_parse(parser, "3 ", "integer", Parse(3, 2))
        test_parse(parser, " 3", "integer", Parse(3, 2))
        test_parse(parser, " 3 ", "integer", Parse(3, 3))
        test_parse(parser, "  3  ", "integer", Parse(3, 5))
        test_parse(parser, "    3  ", "integer", Parse(3, 7))
        test_parse(parser, "  3  +  4  ", "addition", Parse(7, 11))
        test_parse(parser, "(  3  +  4  )", "addition", Parse(7, 13))
        test_parse(parser, "   (  3  +  4  )", "addition", Parse(7, 16))
        test_parse(parser, "   (     3  +  4  )", "addition", Parse(7, 19))
        test_parse(parser, "3+    4       +5   +    5 +     9", "addition", Parse(26, 33))
        test_parse(parser, "3 + + ", "addition", Parse(3, 2))
        test_parse(parser, "3+    4       + (5   +   5  +     9)  ", "addition", Parse(26, 38))  # the addition fails leading to a fail in index length
        # #subtraction test
        test_parse(parser, "5-3", "add|sub", Parse(2, 3))
        test_parse(parser, "3-5", "add|sub", Parse(-2, 3))
        test_parse(parser, "(5-6)-9", "add|sub", Parse(-10, 7))
        test_parse(parser, " (5-6)-9 ", "add|sub", Parse(-10, 9))
        test_parse(parser, " (5-6) -9 ", "add|sub", Parse(-10, 10))

        # retry addition as artithmetic
        test_parse(parser, "b", "add|sub", self.FAIL)
        test_parse(parser, "", "add|sub", self.FAIL)
        test_parse(parser, "3-", "add|sub", Parse(3,1))
        test_parse(parser, "3++", "add|sub", Parse(3,1))
        test_parse(parser, "3+4", "add|sub", Parse(7, 3))
        test_parse(parser, "2020+2021", "add|sub", Parse(4041, 9))
        test_parse(parser, "0+0", "add|sub", Parse(0, 3))
        test_parse(parser, "1+1+", "add|sub", Parse(2, 3))
        test_parse(parser, "1+1+-", "add|sub", Parse(2, 3))
        test_parse(parser, "0+0+0+0+0", "add|sub", Parse(0, 9))
        test_parse(parser, "42+0", "add|sub", Parse(42, 4))
        test_parse(parser, "40+42", "add|sub", Parse(82, 5))
        test_parse(parser, "123+234+456", "add|sub", Parse(813, 11))
        # parenthesis test cases
        test_parse(parser, "(0)", "parenthesis", Parse(0, 3))
        test_parse(parser, "(0+0)", "parenthesis", Parse(0, 5))
        test_parse(parser, "(1+2)", "parenthesis", Parse(3, 5))
        test_parse(parser, "(1+2+3)", "parenthesis", Parse(6, 7))
        test_parse(parser, "4+(1+2+3)", "add|sub", Parse(10, 9))
        test_parse(parser, "(1+2+3)+5", "add|sub", Parse(11, 9))
        test_parse(parser, "4+(1+2+3)+5", "add|sub", Parse(15, 11))
        test_parse(parser, "3+4+(5+6)+9", "add|sub", Parse(27, 11))

        # end to end test
        test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "addition", Parse(27, 25))

        # addition and subtraction test
        test_parse(parser, "3-5+1", "add|sub", Parse(-1, 5))
        test_parse(parser, "(5+7)-6+2", "add|sub", Parse(8, 9))
        test_parse(parser, "(  5+7)-6+  2", "add|sub", Parse(8, 13))
        test_parse(parser, "(5+(4+5))", "parenthesis", Parse(14, 9))
        test_parse(parser, "5*5", "mult|div", Parse(25, 3))
        test_parse(parser, "1   *  17   ", "mult|div", Parse(17, 12))
        test_parse(parser, "5*10*2", "mult|div", Parse(100, 6))
        test_parse(parser, "5/5", "mult|div", Parse(1, 3))
        test_parse(parser, "5+5/5", "add|sub", Parse(6, 5))
        test_parse(parser, "5*5/5", "mult|div", Parse(5, 5))
        test_parse(parser, "(5/5)", "mult|div", Parse(1, 5))
        test_parse(parser, "3+5+(5*5)", "add|sub", Parse(33, 9))



        '''
        ask justin more about how to parse mult div and addition together should it be one function - I was confused on how to read the info in the grammar posted on moodle can you go over that please 
        '''





        #still missing 2









def test_parse(parser, string, term, expected):
    actual = parser.parse(string, term)
    assert actual is not None, 'Got None when parsing "{}"'.format(string)
    assert actual.value == expected.value, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )
    assert actual.index == expected.index, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )
    # assert actual == expected, 'Parsing "{}"; expected {} but got {}'.format(
    #     string, expected, actual
    # )


def main():
    parser = Parser()
    parser.test()


if __name__ == '__main__':
    main()

