from interpreter import  Interpreter

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



class StatementParse():  # fixme operation parse

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


class IdentifierParse(StatementParse):  # type of varloc or lookup, parse of an identifer
    def __init__(self, value, index, type):
        super().__init__(index, type)
        self.value = value

    def to_string(self):
        # return the value + varloc
        result = self.value
        result = "(" + self.type + " " + self.value + ")"
        return result


class AssignLocationParse(IdentifierParse):  # should have a type of varloc  (assign)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)
        self.value = value

    def to_string(self):
        # return the value + varloc
        result = "(" + self.type + " " + self.value + ")"
        return result



class DeclareLocationParse(IdentifierParse):  # should have a type of varloc  (declare)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)
        self.value = value

    def to_string(self):
        result = self.value
        return result





class ProgramParse():

    def __init__(self, index, type):
        self.index = index
        self.type = "program"
        self.children = []

    def to_string(self):
        expression_result = ""
        expression_result += "("
        expression_result += "sequence"
        for child in self.children:
            expression_result += " " + child.to_string()
        expression_result += ")"
        return expression_result



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
        elif term == "expression_statement":
            return self.__parse_expression_statement(string, index)
        elif term == "print_statement":
            return self.__parse_print_statement(string, index)
        elif term == "identifier_first_char":
            return self.__parse_identifier_first_char(string, index)
        elif term == "identifier_char":
            return self.__parse_identifier_char(string, index)
        elif term == "identifier":
            return self.__parse_identifier(string, index)
        elif term == "location":
            return self.__parse_location(string, index)
        elif term == "assignment_statement":
            return self.__parse_assignment_statement(string, index)
        elif term == "declaration_statement":
            return self.__parse_declaration_statement(string, index)
        elif term == "comp_expression":
            return self.__parse_comp_expression(string, index)
        elif term == "comp_operator":
            return self.__parse_comp_operator(string, index)
        elif term == "not_expression":
            return self.__parse_not_expression(string, index)
        elif term == "optional_not_expression":
            return self.__parse_optional_not_expression(string, index)
        elif term == "and_operator":
            return self.__parse_and_operator(string, index)
        elif term == "or_operator":
            return self.__parse_or_operator(string, index)
        elif term == "and_expression":
            return self.__parse_and_expression(string, index)
        elif term == "or_expression":
            return self.__parse_or_expression(string, index)
        elif term == "while_statement":
            return self.__parse_while_statement(string, index)
        elif term == "if_else_statement":
            return self.__parse_if_else_statement(string, index)
        elif term == "if_statement":
            return self.__parse_if_statement(string, index)
        else:
            raise AssertionError("Unexpected Term " + term)

        __parse_and_expression


    def __parse_operand(self, string, index):
        parse = self.__parse(string, index, "integer")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "parenthesis")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "identifier")
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
        parsed = ""
        parse = self.__parse(string, index, "op_space")
        if parse == self.FAIL:  # if op space was fail then fail
            return self.FAIL
        parsed += parse.value
        if len(parsed) >= 1:  # if parse length is not at least one then fail
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
        program = ProgramParse(index, "program")
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if op space add to index
            index = space_parse.index
        statement_parse = None
        while index < len(string) and statement_parse != self.FAIL:
            statement_parse = self.__parse(string, index, "statement")
            if statement_parse == self.FAIL:
                break
            program.children.append(statement_parse)  # add the statement to the program
            index = statement_parse.index  # add the current statement parse to current index
            space_parse = self.__parse(string, index, "op_space")
            if space_parse != self.FAIL:  # if op space add to index
                index = space_parse.index
        program.index = index  # set program index = index
        return program  # return the program

    def __parse_statement(self, string, index):
        parse = self.__parse(string, index, "declaration_statement")  # try to parse declare statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "assignment_statement")  # try to parse for assign statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "if_else_statement")  # try to parse for if_else statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "if_statement")  # try to parse for if statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "while_statement")  # try to parse for while statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "print_statement")  # try to parse for print statement
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "expression_statement")  # try to parse for expression
        if parse != self.FAIL:
            return parse
        return self.FAIL  # if no expression or print then fail

    def __parse_expression(self, string, index):
        parse = self.__parse(string, index, "or_expression")
        if parse == self.FAIL:
            return self.FAIL
        return parse

    def __parse_expression_statement(self, string, index):
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if optional space, add to index
            index = space_parse.index
        parse = self.__parse(string, index, "expression")
        if parse == self.FAIL:
            return self.FAIL
        if string[index] != ";":  # check for the ; end char
            return self.FAIL
        parse.index += 1 # add one index for the semi colon
        return parse

    def __parse_print_statement(self, string, index):
        # check for spaces at the start of a print statement
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if optional space, add to index
            index = space_parse.index
        print = string[index:index + 5]  # check for print
        if print != "print":
            return self.FAIL
        index += 5  # skip to end of print
        parse = self.__parse(string, index, "req_space")  # parse the required one space or newline
        if parse == self.FAIL:
            return self.FAIL
        index +=1  # add one for req space
        expression_parse = self.__parse(string, index, "expression")  # parse for the expression
        if expression_parse == self.FAIL:
            return self.FAIL
        index = expression_parse.index  # set index to end of expression
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if optional space, add to index
            index = space_parse.index
        if string[index] != ";":  # check for the ; end char
            return self.FAIL
        index += 1 # add one index for the semi colon
        print_statement = StatementParse(index, "print")
        print_statement.children.append(expression_parse)
        return print_statement


    def __parse_identifier_first_char(self, string, index):
        parsed = ""
        if (not string[index].isalpha()) and (string[index] != "_"):  # if string is not a letter and string not a _
            return self.FAIL
        parsed += string[index]
        index += 1
        return Parse(parsed, index)

    def __parse_identifier_char(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isalnum():  # loops and adds to parsed while still alphanumeric
            parsed += string[index]
            index +=1
        return Parse(parsed, index)


    def __parse_identifier(self, string, index):
        parsed = ""
        parse_first_char = self.__parse(string, index, "identifier_first_char")  # get first char
        if parse_first_char == self.FAIL:  # check for fail
            return self.FAIL
        parsed += parse_first_char.value  # add index and value
        index = parse_first_char.index
        parse_remaining = self.__parse(string, index, "identifier_char")  # parse for remaining chars
        parsed += parse_remaining.value
        index = parse_remaining.index  # add index and value
        return IdentifierParse(parsed, index, "lookup")  # parse all identifers initially as a lookup


    def __parse_location(self, string, index):
        parse_identifier = self.__parse(string, index, "identifier")
        if parse_identifier == self.FAIL:
            return self.FAIL
        return parse_identifier

    def __parse_assignment_statement(self, string, index):
        location_parse = self.__parse(string, index, "location")  # parse the location
        if location_parse == self.FAIL:
            return self.FAIL
        # change var_lovation to be a VarLocation parse object
        var_location = AssignLocationParse(location_parse.value, location_parse.index, "varloc")
        index = var_location.index  # add var_location index
        op_space = self.__parse(string, index, "op_space")
        if op_space != self.FAIL:
            index = op_space.index  # if optional space then add to index
        if string[index] != "=":
            return self.FAIL  # if the next char is not a = then fail
        index += 1  # add one for the =
        op_space = self.__parse(string, index, "op_space")
        if op_space != self.FAIL:
            index = op_space.index  # if optional space then add to index
        expression_parse = self.__parse(string, index, "expression")  # parse for an expression statement
        if expression_parse == self.FAIL:
            return self.FAIL
        index = expression_parse.index  # add expression_parse to index
        op_space = self.__parse(string, index, "op_space")
        if op_space != self.FAIL:
            index = op_space.index  # if optional space then add to index
        if string[index] != ";":
            return self.FAIL  #  check for the ; end char
        index += 1  # add one index for the semi colon
        assignment_parse = StatementParse(index, "assign")
        assignment_parse.children.append(var_location)
        assignment_parse.children.append(expression_parse)  # add the location & expression parse as children
        return assignment_parse


    def __parse_declaration_statement(self, string, index):
        var = string[index:index+3]  # check for var
        if var != "var":
            return self.FAIL
        index += 3  # skip to end of var
        req_space = self.__parse(string, index, "req_space")  # parse the required one space or newline
        if req_space == self.FAIL:
            return self.FAIL
        index +=1  # add one for req space
        assignment_statement = self.__parse(string, index, "assignment_statement")
        if assignment_statement == self.FAIL:
            return self.FAIL  # if no assignment then fail
        index = assignment_statement.index  # set index to assign index
        variable = assignment_statement.children[0]  # get the variable from assignment
        expression = assignment_statement.children[1]  # get the expression from assignment (rhs)
        declaration_statement = StatementParse(index, "declare")
        identifier = DeclareLocationParse(variable.value, variable.index, variable.type)  # make var into identifier parse
        declaration_statement.children.append(identifier)
        declaration_statement.children.append(expression)  # add variable & expression as children of declare statement
        return declaration_statement


    def __parse_comp_expression(self, string, index):
        left_expression = self.__parse(string,index, "add|sub")  # parse the lhs add|sub expression
        if left_expression == self.FAIL:
            return self.FAIL
        index = left_expression.index  # add lhs to index
        parent = None  # declare parent
        parse = None  # declare parse to fail test
        while index <len(string) and parse != self.FAIL:
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            operator = self.__parse(string,index, "comp_operator")
            if operator == self.FAIL:
                parse = self.FAIL
                break
            index = operator.index  # add operator to index
            right_expression = self.__parse(string, index, "add|sub")  # parse the rhs add|sub expression
            if right_expression == self.FAIL:
                parse = self.FAIL
                break
            index = right_expression.index  # add right expression to index
            parent = StatementParse(index, operator.value)  #  new statement with type of operator value
            parent.children.append(left_expression)
            parent.children.append(right_expression)
            left_expression = parent
        if parent == None:
            return left_expression  # if there was no comparison return the left expression
        return parent


    def __parse_comp_operator(self, string, index):
        if string[index: index +2] == "==":  # bc right bound is exclusive add an extra +1
            return Parse("==", index +2)  # return index + 2 for each char
        elif string[index: index + 2] == "!=":
            return Parse("!=", index +2)
        elif string[index: index + 2] == "<=":
            return Parse("<=", index +2)
        elif string[index: index + 2] == ">=":
            return Parse(">=", index +2)
        elif string[index: index + 1] == "<":
            return Parse("<", index +1)  # add +1 for 1 char
        elif string[index: index + 1] == ">":
            return Parse(">", index +1)
        return self.FAIL  # if no operator then fail


    def __parse_not_expression(self, string, index):
        if string[index] != "!":
            return self.FAIL
        index += 1  # add one for !
        req_space = self.__parse(string,index, "req_space")
        if req_space == self.FAIL:  # if no req_space fail
            return self.FAIL
        index = req_space.index
        comp_expression = self.__parse(string,index, "comp_expression")
        if comp_expression == self.FAIL:
            return self.FAIL
        index = comp_expression.index  # add comp exp to index
        not_expression = StatementParse(index, "not_expression")
        not_expression.children.append("!")
        not_expression.children.append(comp_expression)
        return not_expression



    def __parse_optional_not_expression(self, string, index):
        not_expression = self.__parse(string, index, "not_expression")
        if not_expression != self.FAIL:
            return not_expression
        comp_expression = self.__parse(string, index, "comp_expression")
        if comp_expression != self.FAIL:
            return comp_expression
        return self.FAIL


    def __parse_and_operator(self, string, index):
        if string[index: index + 2] == "&&":
            return Parse("&&", index + 2)  # return index + 2 for each char
        return self.FAIL

    def __parse_or_operator(self, string, index):
        if string[index: index + 2] == "||":
            return Parse("||", index + 2)  # return index + 2 for each char
        return self.FAIL

    def __parse_and_expression(self, string, index):
        left_expression = self.__parse(string, index, "optional_not_expression")
        if left_expression == self.FAIL:  # if no left expression fail
            return self.FAIL
        index = left_expression.index  # add left exp to index
        parent = None  # declare parent
        parse = None  # declare parse to test fail
        while index < len(string) and parse != self.FAIL:
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            and_operator = self.__parse(string,index, "and_operator")  # check for and operator
            if and_operator == self.FAIL:
                parse = self.FAIL
                break
            index = and_operator.index  # add operator to index
            right_expression = self.__parse(string, index, "optional_not_expression")  # parse the rhs expression
            if right_expression == self.FAIL:
                parse = self.FAIL
                break
            index = right_expression.index  # add right exp to index
            parent = StatementParse(index, and_operator.value)  # new statement parse of and type
            parent.children.append(left_expression)
            parent.children.append(right_expression)
            left_expression = parent
        if parent == None:
            return left_expression # if there was no comparison return the left expression
        return parent


    def __parse_or_expression(self, string, index):
        left_expression = self.__parse(string, index, "and_expression")
        if left_expression == self.FAIL:  # if no left expression fail
            return self.FAIL
        index = left_expression.index  # add left exp to index
        parent = None  # declare parent
        parse = None  # declare parse to test fail
        while index < len(string) and parse != self.FAIL:
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            or_operator = self.__parse(string,index, "or_operator")  # check for and operator
            if or_operator == self.FAIL:
                parse = self.FAIL
                break
            index = or_operator.index  # add operator to index
            right_expression = self.__parse(string, index, "and_expression")  # parse the rhs expression
            if right_expression == self.FAIL:
                parse = self.FAIL
                break
            index = right_expression.index  # add right exp to index
            parent = StatementParse(index, or_operator.value)  # new statement parse of and type
            parent.children.append(left_expression)
            parent.children.append(right_expression)
            left_expression = parent
        if parent == None:
            return left_expression # if there was no comparison return the left expression
        return parent

    def __parse_if_statement(self, string, index):
        if_key = string[index: index + 2]
        if if_key != "if":  # check that starts with if
            return self.FAIL
        index += 2  # add 2 for if
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "(":
            return self.FAIL
        index += 1 # add index for open paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        qualifying_expression = self.__parse(string, index, "expression")
        if qualifying_expression == self.FAIL:
            return self.FAIL
        index = qualifying_expression.index  # add exp to index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != ")":  # check for close paren
            return self.FAIL
        index += 1  # add index for close paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "{":  # check for open curly brace
            return self.FAIL
        index += 1  # add one for curly brace
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        program = self.__parse(string, index, "program")   # parse the program
        if program == self.FAIL:
            return self.FAIL
        index = program.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "}":  # check for close curly brace
            return self.FAIL
        index += 1  # add one for closing curly brace
        if_statement = StatementParse(index, "if")
        if_statement.children.append(qualifying_expression)
        if_statement.children.append(program)
        return if_statement


    def __parse_if_else_statement(self, string, index):
        if_statement = self.__parse(string, index, "if_statement")
        if if_statement == self.FAIL:
            return self.FAIL
        index = if_statement.index  # add if statement to index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        else_key = string[index: index + 4]
        if else_key != "else":
            return self.FAIL
        index += 4 # add 4 for else
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        else_key = string[index: index + 4]
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "{":  # check for open curly brace
            return self.FAIL
        index += 1  # add one for curly brace
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        else_program = self.__parse(string, index, "program")  # parse the program
        if else_program == self.FAIL:
            return self.FAIL
        index = else_program.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "}":  # check for close curly brace
            return self.FAIL
        index += 1  # add one for closing curly brace
        # ir tree will be qualifiter, if, else
        qualifying_statement = if_statement.children[0]
        if_program = if_statement.children[1]
        if_else_statement = StatementParse(index, "if_else")
        if_else_statement.children.append(qualifying_statement)
        if_else_statement.children.append(if_program)
        if_else_statement.children.append(else_program)
        return if_else_statement




    def __parse_while_statement(self, string, index):
        while_key = string[index: index+5]
        if while_key != "while":  # check that starts with while
            return self.FAIL
        index += 5 # add 5 for while
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "(":
            return self.FAIL
        index += 1 # add index for open paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        qualifying_expression = self.__parse(string, index, "expression")
        if qualifying_expression == self.FAIL:
            return self.FAIL
        index = qualifying_expression.index  # add exp to index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != ")":  # check for close paren
            return self.FAIL
        index += 1  # add index for close paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "{":  # check for open curly brace
            return self.FAIL
        index += 1  # add one for curly brace
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        program = self.__parse(string, index, "program")   # parse the program
        if program == self.FAIL:
            return self.FAIL
        index = program.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "}":  # check for close curly brace
            return self.FAIL
        index += 1  # add one for closing curly brace
        while_statement = StatementParse(index, "while")
        while_statement.children.append(qualifying_expression)
        while_statement.children.append(program)
        return while_statement



    def test(self):
        parser = Parser()
        interpreter = Interpreter()

        # term = parser.parse("if (1) { print 1;  };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x+3*5) { print 1; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x+3*5) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x<1) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x<=1) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x=1) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x>=1) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x=>1) { print 1; var x=5; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x<=1) { print 1; var x=5; } else{ print 2; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("while (x==1) { print 1; };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("if (x<=1) { print 1; var x=5; } else{ while (x==1) { print 1; } };", "program")  # 6
        # print(term.to_string())
        # term = parser.parse("var x = 0; print x; x = (5 * 5) / 5; if (x){ print 45 * 645+54; }", "program")  # 6
        # term = parser.parse("var x = 1; if (x == 1){ var x = 2; print x;} print x; ", "program")  DONE
        term = parser.parse("var x = 1; if (x == 1 && x ==1 ) { if (x == 1) { if (x == 1) { if (x == 1) { print x; } }   }} print x; ", "program")

        # interpreter.execute(term)
        print(term.to_string())











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
