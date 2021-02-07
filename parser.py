from interperter import  Interperter

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


class IntergerParse():

    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.type = "int"

    def to_string(self):
        # return the value casted to string
        return str(self.value)

class StatementParse():

    def __init__(self, index, type):
        self.index = index
        self.type = type
        self.children = []

    def to_string(self):
        # if statement parse print the operator type and children to string
        expression_result = ""
        expression_result += "("
        expression_result += self.type
        for child in self.children:
            expression_result += " " + child.to_string()
        expression_result += ")"
        return expression_result

class ProgramParse():

    def __init__(self, index, type):
        self.index = index
        self.children = []



class Parser:
    FAIL = Parse(0, -1)

    def parse(self, string, term):
        return self.__parse(string, 0, term)

    def __parse(self, string, index, term):  # main parse wrapper that calls each item to be parsed @each index
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
        elif term == "op_space":
            return self.__parse_optional_spaces(string, index)
        elif term == "req_space":
            return self.__parse_required_space(string, index)
        elif term == "space":
            return self.__parse_space(string, index)
        elif term == "comment":
            return self.__parse_comment(string, index)
        elif term == "newline":
            return self.__parse_newline(string, index)
        elif term == "add|sub":
            return self.__parse_add_sub_expression(string, index)
        elif term == "mult|div":
            return self.__parse_mult_div_expression(string, index)
        elif term == "program":
            return self.__parse_program(string, index)
        elif term == "statement":
            return self.__parse_statement(string, index)
        elif term == "expression":
            return self.__parse_expression(string, index)
        elif term == "print_statement":
            return self.__parse_print_statement(string, index)
        else:
            raise AssertionError("Unexpected Term " + term)

    def __parse_operand(self, string, index):
        parse = self.__parse(string, index, "integer")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "parenthesis")
        if parse != self.FAIL:
            return parse
        return self.FAIL  # may need to add index here to return

    def __parse_integer(self, string, index):
        parse = self.__parse(string, index, "op_space")  # checks for spaces at start of integer and adds to index
        if parse != self.FAIL:
            index = parse.index  # if parse of spaces was success add to index
        parsed = ""
        while index < len(string) and string[index].isdigit():  # loops through and adds to parsed while still a digit
            parsed += string[index]
            index += 1
        if parsed == '':
            return self.FAIL
        parse = self.__parse(string, index, "op_space")  # checks for spaces at end of integer and adds to index
        if parse != self.FAIL:
            index = parse.index  # if parse of spaces was success add to index
        return IntergerParse(int(parsed), index)  # returns the parsed int

    def __parse_optional_spaces(self, string, index):
        parsed = ""
        # loops through and adds to parsed while still a digit
        while index < len(string) and (string[index] == " " or string[index] == "\n" or string[index] == "#"):

            if index < len(string) and string[index] == " ":  # parse for spaces
                parse = self.__parse(string, index, "space")
                if parse == self.FAIL:
                    return self.FAIL
                parsed += parse.value  # add parsed space
                index = parse.index  # set index to index of after the space

            if index < len(string) and string[index] == "\n":  # parse for newline
                parse = self.__parse(string, index, "newline")
                if parse == self.FAIL:
                    return self.FAIL
                parsed += parse.value  # add parsed newline
                index = parse.index  # set index to index of after the newline

            if index < len(string) and string[index] == "#":  # parse for comment
                parse = self.__parse(string, index, "comment")
                if parse == self.FAIL:
                    return self.FAIL
                parsed += parse.value  # add parsed comment
                index = parse.index  # set index to index of after the comment

        if parsed == "":  # if nothing was parsed fail
            return self.FAIL
        return Parse(parsed, index)


    def __parse_required_space(self, string, index):
        parse = self.__parse(string, index, "op_space")
        if parse.value == " " or parse.value == "\n":
            return parse
        return self.FAIL


    def __parse_comment(self, string, index):
        parsed = ""
        #should parse until it gets to a newline
        while index < len(string) and string[index] != "\n":
            parsed += string[index]
            index += 1
        if parsed == "":
            return self.FAIL
        return Parse(parsed, index)


    def __parse_space(self, string, index):
        parsed = ""
        while index < len(string) and string[index] == " ":
            parsed += string[index]
            index += 1
        if parsed == "":
            return self.FAIL
        return Parse(parsed, index)

    def __parse_newline(self, string, index):
        parsed = ""
        while index < len(string) and string[index] == "\n":
            parsed += string[index]
            index += 1
        if parsed == "":
            return self.FAIL
        return Parse(parsed, index)


    def __parse_add_sub_expression(self, string, index):  # addition & subtraction function
        '''
        add_sub_expression   = mul_div_expression ( opt_space add_sub_operator opt_space mul_div_expression )*;
        :param string:
        :param index:
        :return: Parse of add|sub expression
        '''
        space_parse = self.__parse(string, index, "op_space")  # parse spaces before operand and add to index
        if space_parse != self.FAIL:
            index = space_parse.index
        left_parse = self.__parse(string, index, "mult|div")  # parses the mult expression (if no expression returns int
        if left_parse == self.FAIL:
            return self.FAIL
        index = left_parse.index
        parent = None # declare parent
        parse = None # declare parse to fail test
        while index < len(string) and parse != self.FAIL:
            if string[index] != "-" and string[index] != "+":  # parse +|- and if not then fail
                parse = self.FAIL
                break
            # parses the mult expression (if no expression returns int); jumps +1 because of the " +/-"
            right_parse = self.__parse(string, left_parse.index + 1,"mult|div")  # use left parse index (parent)
            if right_parse == self.FAIL:  # if operand was fail break
                parse = self.FAIL
                break
            if string[index] == "+":  # if the operation was addition +
                parent = StatementParse(right_parse.index, "+")
                parent.children.append(left_parse) # add right/left parse
                parent.children.append(right_parse)
                left_parse = parent  # set left parse to parent

            if string[index] == "-":  # if the operation was subtraction  -
                parent = StatementParse(right_parse.index, "-")
                parent.children.append(left_parse) # add right/left parse
                parent.children.append(right_parse)
                left_parse = parent  # set left parse to parent
            index = right_parse.index  # set index to right parse index
        if parent == None:
            return left_parse  # if there was no expression return the left operand
        return parent  # return the root level parent

    def __parse_mult_div_expression(self, string, index):  # parse multiplication and division
        '''
        mul_div_expression       = operand ( opt_space mul_div_operator opt_space operand )*;
        :param string:
        :param index:
        :return: Parse of mult|div expression
        '''
        space_parse = self.__parse(string, index, "op_space")  # parse spaces before operand and add to index
        if space_parse != self.FAIL:
            index = space_parse.index
        left_parse = self.__parse(string, index, "operand")  # parses the int at start of expression
        if left_parse == self.FAIL:
            return self.FAIL
        index = left_parse.index  # if not fail add result & index
        parent = None  # declare parent
        parse = None  # declare parse to fail test
        while index < len(string) and parse != self.FAIL:
            if string[index] != "*" and string[index] != "/":  # parse *|/ and if not then fail
                parse = self.FAIL
                break
            right_parse = self.__parse(string, left_parse.index + 1,"operand")  # parse next operand; index +1 for "* | /"
            if right_parse == self.FAIL:  # if operand was fail break
                parse = self.FAIL
                break
            if string[index] == "*":  # if the operation was mult *
                parent = StatementParse(right_parse.index, "*")
                parent.children.append(left_parse) # add right/left parse
                parent.children.append(right_parse)
                left_parse = parent  # set left parse to parent
            if string[index] == "/":  # if the operation was divide
                parent = StatementParse(right_parse.index, "/")
                parent.children.append(left_parse)  # add right/left parse
                parent.children.append(right_parse)
                left_parse = parent  # set left parse to parent
            index = right_parse.index  # set index to right parse index
        if parent == None:
            return left_parse  # if there was no expression return the left operand
        return parent

    def __parse_parenthesis(self, string, index):
        '''
        :param string:
        :param index:
        :return: Parsed parenthesized expression
        '''
        space_parse = self.__parse(string, index, "op_space")  # checks for space at start of parenthesis/ adds to index
        if space_parse != self.FAIL:
            index = space_parse.index  # if parse of spaces was success add to index
        if string[index] != '(':  # check if the string starts with open parenthesis
            return self.FAIL
        parse = self.__parse(string, index + 1, "add|sub")  # parses the addition string inside the parenthesis
        if parse == self.FAIL:  # if addition is not in grammar fails
            return self.FAIL
        if string[parse.index] != ")":  # checks char at end of addition string, if not a close paren, then fail
            return self.FAIL
        space_parse = self.__parse(string, parse.index + 1,"op_space")  # checks for space at end and adds to index
        if space_parse != self.FAIL:  # if spaces return with spaces index
            parse.index = space_parse.index
            return parse
        parse.index +=1
        return parse # add one index to account for close parent \ return statement parse

    def __parse_program(self, string, index):
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if op space add to index
            index = space_parse.index

        pass

    def __parse_statement(self, string, index):
        parse = self.__parse(string, index, "print_statement")  # try to parse print statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "expression")  # try to parse for expression
        if parse != self.FAIL:
            return parse
        return self.FAIL  # if no expression or print then fail

    def __parse_expression(self, string, index):
        parse = self.__parse(string, index, "add|sub")
        if parse == self.FAIL:
            return self.FAIL
        return parse

    def __parse_print_statement(self, string, index):
        print = string[0:5]  # check for print
        if print != "print":
            return self.FAIL
        index += 5  # skip to end of print
        parse = self.__parse(string, index, "req_space")  # parse the required one space or newline
        if parse == self.FAIL:
            return self.FAIL
        expression_parse = self.__parse(string, index, "expression")  # parse for the expression
        if expression_parse == self.FAIL:
            return self.FAIL
        index = expression_parse.index  # set index to end of expression
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if optional space, add to index
            index = space_parse.index
        if string[index] != ";":  # check for the ; end char
            return self.FAIL
        print_statement = StatementParse(index, "print")
        print_statement.children.append(expression_parse)
        return print_statement



    def test(self):
        parser = Parser()
        # test_parse(parser, "3+5+5*5", "add|sub", Parse(33, 9))
        # term = parser.parse("2+2*2", "add|sub")
        # print(term.to_string())
        # term = parser.parse("    2*     2+2", "add|sub")
        # term = parser.parse("2\n *2\n #fkldsalfja  \n+2 # asdfdesfklfkljsdk", "add|sub")
        term = parser.parse("print (2+2)*2;", "print_statement")
        # print(term.to_string())
        # test_parse(parser, "(5*5)+3+5", "add|sub", Parse(33, 9))

        interperter = Interperter()
        interperter.execute(term)


def test_parse(parser, string, term, expected):
    actual = parser.parse(string, term)
    assert actual is not None, 'Got None when parsing "{}"'.format(string)
    assert actual.value == expected.value, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )
    assert actual.index == expected.index, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )

def main():
    parser = Parser()
    parser.test()


if __name__ == '__main__':
    main()
