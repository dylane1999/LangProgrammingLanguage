from interpreter import Interpreter


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

    def __str__(self):
        # return the value casted to string
        return str(self.value)


class StatementParse():  # fixme operation parse

    def __init__(self, index, type):
        self.index = index
        self.type = type
        self.children = []

    def __str__(self):
        # if statement parse print the operator type and children to string
        expression_result = ""
        expression_result += "("
        expression_result += self.type
        for child in self.children:
            expression_result += " " + child.__str__()
        expression_result += ")"
        return expression_result


class CallExpression(StatementParse):  # fixme operation parse

    def __init__(self, index, type, func_name):
        super().__init__(index, type)
        self.children = []
        self.func_name = func_name


class IdentifierParse(StatementParse):  # type of varloc or lookup, parse of an identifer
    def __init__(self, value, index, type):
        super().__init__(index, type)
        self.value = value

    def __str__(self):
        # return the value + varloc
        result = self.value
        result = "(" + self.type + " " + self.value + ")"
        return result


class AssignLocationParse(IdentifierParse):  # should have a type of varloc  (assign)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)
        self.value = value

    def __str__(self):
        # return the value + varloc
        result = "(" + self.type + " " + self.value + ")"
        return result


class DeclareLocationParse(IdentifierParse):  # should have a type of varloc  (declare)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)
        self.value = value

    def __str__(self):
        result = self.value
        return result


class ArgumentsParse(IdentifierParse):  # should have a type of varloc  (declare)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)
        self.value = value

    def __str__(self):
        result = self.value
        return result


class ParametersParse(IdentifierParse):  # should have a type of varloc  (declare)
    def __init__(self, value, index, type):
        super().__init__(value, index, type)

    def __str__(self):
        result = self.value
        return result


class ProgramParse():

    def __init__(self, index, type):
        self.index = index
        self.type = "program"
        self.children = []

    def __str__(self):
        expression_result = ""
        expression_result += "("
        expression_result += "sequence"
        for child in self.children:
            expression_result += " " + child.__str__()
        expression_result += ")"
        return expression_result


class Parser:
    FAIL = Parse(0, -1)

    def parse(self, string):
        try:
            parse = self.__parse(string, 0, "program")
            if len(string) != parse.index:
                raise ValueError("index error/ syntax error")
            return self.__parse(string, 0, "program")
        except Exception as error:
            print("syntax error")
            return None

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
        elif term == "add_sub_operator":
            return self.__parse_add_sub_operator(string, index)
        elif term == "mult_div_operator":
            return self.__parse_mult_div_operator(string, index)
        elif term == "parameters":
            return self.__parse_parameters(string, index)
        elif term == "function":
            return self.__parse_function(string, index)
        elif term == "op_close_paren":
            return self.__parse_optional_close_paren(string, index)
        elif term == "arguments":
            return self.__parse_arguments(string, index)
        elif term == "function_call":
            return self.__parse_function_call(string, index)
        elif term == "call_expression":
            return self.__parse_call_expression(string, index)
        elif term == "return_statement":
            return self.__parse_return_statement(string, index)
        else:
            raise AssertionError("Unexpected Term " + term)

    def __parse_operand(self, string, index):
        parse = self.__parse(string, index, "parenthesis")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "function")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "identifier")
        if parse != self.FAIL:
            return parse
        parse = self.__parse(string, index, "integer")
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
        # should parse until it gets to a newline
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
        space_parse = self.__parse(string, index, "op_space")  # parse spaces
        if space_parse != self.FAIL:
            index = space_parse.index
        left_parse = self.__parse(string, index, "mult|div")  # parses the mult expression (if no expression returns int
        if left_parse == self.FAIL:
            return self.FAIL
        index = left_parse.index
        parent = None  # declare parent
        parse = None  # declare parse to fail test
        while index < len(string) and parse != self.FAIL:
            space_parse = self.__parse(string, index, "op_space")  # parse spaces
            if space_parse != self.FAIL:
                index = space_parse.index
            operator = self.__parse(string, index, "add_sub_operator")
            if operator == self.FAIL:
                parse = self.FAIL
                break
            index += 1  # add one for +/-
            space_parse = self.__parse(string, index, "op_space")  # parse spaces
            if space_parse != self.FAIL:
                index = space_parse.index
            # parses the mult expression (if no expression returns int); jumps +1 because of the " +/-"
            right_parse = self.__parse(string, index, "mult|div")  # use left parse index (parent)
            if right_parse == self.FAIL:  # if operand was fail break
                parse = self.FAIL
                break
            parent = StatementParse(right_parse.index, operator.value)
            parent.children.append(left_parse)  # add right/left parse
            parent.children.append(right_parse)
            left_parse = parent  # set left parse to parent
            index = right_parse.index  # set index to right parse index
        if parent is None:
            return left_parse  # if there was no expression return the left operand
        return parent  # return the root level parent

    def __parse_mult_div_expression(self, string, index):  # parse multiplication and division
        '''
        mul_div_expression       = operand ( opt_space mul_div_operator opt_space operand )*;
        :param string:
        :param index:
        :return: Parse of mult|div expression
        '''
        op_space = self.__parse(string, index, "op_space")  # parse spaces before operand and add to index
        if op_space != self.FAIL:
            index = op_space.index
        left_parse = self.__parse(string, index, "call_expression")  # parses the int at start of expression
        if left_parse == self.FAIL:
            return self.FAIL
        index = left_parse.index  # if not fail add result & index
        parent = None  # declare parent
        parse = None  # declare parse to fail test
        while index < len(string) and parse != self.FAIL:
            op_space = self.__parse(string, index, "op_space")  # parse spaces before operand and add to index
            if op_space != self.FAIL:
                index = op_space.index
            operator = self.__parse(string, index, "mult_div_operator")
            if operator == self.FAIL:
                parse = self.FAIL
                break
            index += 1  # add one for * or //
            op_space = self.__parse(string, index, "op_space")  # parse spaces before operand and add to index
            if op_space != self.FAIL:
                index = op_space.index
            right_parse = self.__parse(string, index, "call_expression")  # parse next operand; index +1 for "* | /"
            if right_parse == self.FAIL:  # if operand was fail break
                parse = self.FAIL
                break
            parent = StatementParse(right_parse.index, operator.value)
            parent.children.append(left_parse)  # add right/left parse
            parent.children.append(right_parse)
            left_parse = parent  # set left parse to parent
            index = right_parse.index  # set index to right parse index
        if parent is None:
            return left_parse  # if there was no expression return the left operand
        return parent

    def __parse_add_sub_operator(self, string, index):
        if string[index] == "+":
            return Parse("+", index + 1)
        elif string[index] == "-":
            return Parse("-", index + 1)
        else:
            return self.FAIL

    def __parse_mult_div_operator(self, string, index):
        if string[index] == "*":
            return Parse("*", index + 1)
        elif string[index] == "/":
            return Parse("/", index + 1)
        else:
            return self.FAIL

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
        parse = self.__parse(string, index + 1, "expression")  # parses the expression inside the parenthesis
        if parse == self.FAIL:  # if addition is not in grammar fails
            return self.FAIL
        if string[parse.index] != ")":  # checks char at end of addition string, if not a close paren, then fail
            return self.FAIL
        space_parse = self.__parse(string, parse.index + 1, "op_space")  # checks for space at end and adds to index
        if space_parse != self.FAIL:  # if spaces return with spaces index
            parse.index = space_parse.index
            return parse
        parse.index += 1
        return parse  # add one index to account for close parent \ return statement parse

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
        declare_parse = self.__parse(string, index, "declaration_statement")  # try to parse declare statement
        if declare_parse != self.FAIL:
            return declare_parse
        assign_parse = self.__parse(string, index, "assignment_statement")  # try to parse for assign statement
        if assign_parse != self.FAIL:
            return assign_parse
        if_else_parse = self.__parse(string, index, "if_else_statement")  # try to parse for if_else statement
        if if_else_parse != self.FAIL:
            return if_else_parse
        if_parse = self.__parse(string, index, "if_statement")  # try to parse for if statement
        if if_parse != self.FAIL:
            return if_parse
        while_parse = self.__parse(string, index, "while_statement")  # try to parse for while statement
        if while_parse != self.FAIL:
            return while_parse
        return_parse = self.__parse(string, index, "return_statement")  # try to parse for while statement
        if return_parse != self.FAIL:
            return return_parse
        print_parse = self.__parse(string, index, "print_statement")  # try to parse for print statement
        if print_parse != self.FAIL:
            return print_parse
        expression_parse = self.__parse(string, index, "expression_statement")  # try to parse for expression
        if expression_parse != self.FAIL:
            return expression_parse
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
        index = parse.index
        if string[index] != ";":  # check for the ; end char
            return self.FAIL
        parse.index += 1  # add one index for the semi colon
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
        index = parse.index  # add index for req space
        expression_parse = self.__parse(string, index, "expression")  # parse for the expression
        if expression_parse == self.FAIL:
            return self.FAIL
        index = expression_parse.index  # set index to end of expression
        space_parse = self.__parse(string, index, "op_space")
        if space_parse != self.FAIL:  # if optional space, add to index
            index = space_parse.index
        if string[index] != ";":  # check for the ; end char
            return self.FAIL
        index += 1  # add one index for the semi colon
        print_statement = StatementParse(index, "print")
        print_statement.children.append(expression_parse)
        return print_statement

    def __parse_identifier_first_char(self, string, index):
        parsed = ""
        if (not string[index].isalpha()) and (string[index] != "_"):  # if string is not a letter and string not a _
            return self.FAIL
            # raise ValueError("starts with illegal char")
        parsed += string[index]
        index += 1
        return Parse(parsed, index)

    def __parse_identifier_char(self, string, index):
        parsed = ""
        while index < len(string) and (string[index].isalnum() or string[index] == "-" or string[
            index] == "_"):  # loops and adds to parsed while still alphanumeric
            parsed += string[index]
            index += 1
        return Parse(parsed, index)

    def __parse_identifier(self, string, index):
        parsed = ""
        first_index = index
        parse_first_char = self.__parse(string, index, "identifier_first_char")  # get first char
        if parse_first_char == self.FAIL:  # check for fail
            return self.FAIL
        parsed += parse_first_char.value  # add index and value
        index = parse_first_char.index
        identifier_parse = self.__parse(string, index, "identifier_char")  # parse for remaining chars
        parsed += identifier_parse.value
        index = identifier_parse.index  # add index and value
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
        if index >= len(string) or string[index] != ";":
            return self.FAIL  # check for the ; end char
        index += 1  # add one index for the semi colon
        assignment_parse = StatementParse(index, "assign")
        assignment_parse.children.append(var_location)
        assignment_parse.children.append(expression_parse)  # add the location & expression parse as children
        return assignment_parse

    def __parse_declaration_statement(self, string, index):
        var = string[index:index + 3]  # check for var
        if var != "var":
            return self.FAIL
        index += 3  # skip to end of var
        req_space = self.__parse(string, index, "req_space")  # parse the required one space or newline
        if req_space == self.FAIL:
            return self.FAIL
        index += 1  # add one for req space
        assignment_statement = self.__parse(string, index, "assignment_statement")
        if assignment_statement == self.FAIL:
            return self.FAIL  # if no assignment then fail
        index = assignment_statement.index  # set index to assign index
        variable = assignment_statement.children[0]  # get the variable from assignment
        expression = assignment_statement.children[1]  # get the expression from assignment (rhs)
        declaration_statement = StatementParse(index, "declare")
        identifier = DeclareLocationParse(variable.value, variable.index,
                                          variable.type)  # make var into identifier parse
        declaration_statement.children.append(identifier)
        declaration_statement.children.append(expression)  # add variable & expression as children of declare statement
        if self.__check_forbidden_names(declaration_statement.children[0].value):  # pass var name as arg
            raise ValueError("syntax error")  # check for exceptions on variable name
        return declaration_statement

    def __check_forbidden_names(self, string):
        if string == "print":
            return True
        elif string == "var":
            return True
        elif string == "if":
            return True
        elif string == "while":
            return True
        elif string == "funct":
            return True
        elif string == "ret":
            return True
        elif string == "class":
            return True
        elif string == "int":
            return True
        elif string == "bool":
            return True
        elif string == "string":
            return True
        return False  # return a boolean if the identifier name is one of the forbidden names

    def __parse_comp_expression(self, string, index):
        left_expression = self.__parse(string, index, "add|sub")  # parse the lhs add|sub expression
        if left_expression == self.FAIL:
            return self.FAIL
        index = left_expression.index  # add lhs to index
        parent = None  # declare parent
        parse = None  # declare parse to fail test
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        operator = self.__parse(string, index, "comp_operator")
        if operator == self.FAIL:
            return left_expression
        index = operator.index  # add operator to index
        right_expression = self.__parse(string, index, "add|sub")  # parse the rhs add|sub expression
        if right_expression == self.FAIL:
            return left_expression
        index = right_expression.index  # add right expression to index
        parent = StatementParse(index, operator.value)  # new statement with type of operator value
        parent.children.append(left_expression)
        parent.children.append(right_expression)
        left_expression = parent
        if parent is None:
            return left_expression  # if there was no comparison return the left expression
        return parent

    def __parse_comp_operator(self, string, index):
        if string[index: index + 2] == "==":  # bc right bound is exclusive add an extra +1
            return Parse("==", index + 2)  # return index + 2 for each char
        elif string[index: index + 2] == "!=":
            return Parse("!=", index + 2)
        elif string[index: index + 2] == "<=":
            return Parse("<=", index + 2)
        elif string[index: index + 2] == ">=":
            return Parse(">=", index + 2)
        elif string[index: index + 1] == "<":
            return Parse("<", index + 1)  # add +1 for 1 char
        elif string[index: index + 1] == ">":
            return Parse(">", index + 1)
        return self.FAIL  # if no operator then fail

    def __parse_not_expression(self, string, index):
        if string[index] != "!":
            return self.FAIL
        index += 1  # add one for !
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        comp_expression = self.__parse(string, index, "comp_expression")
        if comp_expression == self.FAIL:
            return self.FAIL
        index = comp_expression.index  # add comp exp to index
        not_expression = StatementParse(index, "!")
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
            and_operator = self.__parse(string, index, "and_operator")  # check for and operator
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
        if parent is None:
            return left_expression  # if there was no comparison return the left expression
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
            or_operator = self.__parse(string, index, "or_operator")  # check for and operator
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
        if parent is None:
            return left_expression  # if there was no comparison return the left expression
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
        index += 1  # add index for open paren
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
        program = self.__parse(string, index, "program")  # parse the program
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
        index += 4  # add 4 for else
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
        if_else_statement = StatementParse(index, "ifelse")
        if_else_statement.children.append(qualifying_statement)
        if_else_statement.children.append(if_program)
        if_else_statement.children.append(else_program)
        return if_else_statement

    def __parse_while_statement(self, string, index):
        while_key = string[index: index + 5]
        if while_key != "while":  # check that starts with while
            return self.FAIL
        index += 5  # add 5 for while
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "(":
            return self.FAIL
        index += 1  # add index for open paren
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
        program = self.__parse(string, index, "program")  # parse the program
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

    def __parse_function(self, string, index):
        func_keyword = string[index:index + 4]
        if func_keyword != "func":  # if doesn't start with func then fail
            return self.FAIL
        index += 4  # add 4 for func
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "(":  # if no open paren, fail
            return self.FAIL
        index += 1  # add 1 for paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        params_parse = self.__parse(string, index, "parameters")  # parse program parameters
        index = params_parse.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != ")":
            return self.FAIL  # check for close paren
        index += 1  # add one for paren
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "{":
            return self.FAIL  # check for open curly brace
        index += 1  # add one for curly brace
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        program_parse = self.__parse(string, index, "program")
        if program_parse == self.FAIL:  # parse program, add to index
            return self.FAIL
        index = program_parse.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != "}":
            return self.FAIL  # check for close curly brace
        index += 1  # add one for curly brace
        function_parse = StatementParse(index, "function")
        function_parse.children.append(params_parse)  # add params to children
        function_parse.children.append(program_parse)  # add programs in funct to children
        return function_parse

    def __parse_parameters(self, string, index):
        all_parameters_parse = StatementParse(index, "parameters")  # decalre statement
        identifier_parse = self.__parse(string, index, "identifier")  # parse identifier
        if identifier_parse != self.FAIL:
            index = identifier_parse.index  # add indentifier to index
            param_parse = ParametersParse(identifier_parse.value, identifier_parse.index,
                                          "parameters")  # create param parse
            all_parameters_parse.children.append(param_parse)
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        parse = None
        while index < len(string) and parse != self.FAIL:
            if string[index] != ",":  # if no , break
                parse = self.FAIL
                break
            index += 1  # add one for ,
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            identifier_parse = self.__parse(string, index, "identifier")  # parse identifier
            if identifier_parse == self.FAIL:
                parse = self.FAIL
                break
            index = identifier_parse.index  # add identifier to index
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            param_parse = ParametersParse(identifier_parse.value, identifier_parse.index,
                                          "parameters")  # create param parse
            all_parameters_parse.children.append(param_parse)  # add the identifier to args
        all_parameters_parse.index = index  # set param index to index
        return all_parameters_parse  # get all params and return

    def __parse_optional_close_paren(self, string, index):
        parsed = ""
        if string[index] == ")":
            return Parse(")", index + 1)
        else:
            return Parse("", index)

    def __parse_call_expression(self, string, index):
        operand_parse = self.__parse(string, index, "operand")
        if operand_parse == self.FAIL:
            return self.FAIL
        index = operand_parse.index
        parent = None
        parse = None
        lhs = operand_parse
        while index < len(string) and parse != self.FAIL:
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            function_call_parse = self.__parse(string, index, "function_call")
            if function_call_parse == self.FAIL:
                parse = self.FAIL
                break
            index = function_call_parse.index  # set index to funct call parse
            parent = CallExpression(index, "call", operand_parse.value)
            parent.children.append(lhs)
            parent.children.append(function_call_parse)  # add the function arguments
            lhs = parent
        if parent is None:
            return operand_parse
        parent.index = index  # set call exp index to index
        return parent

    def __parse_function_call(self, string, index):
        if string[index] != "(":
            return self.FAIL
        index += 1
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        arguments_parse = self.__parse(string, index, "arguments")  # get func arguments
        index = arguments_parse.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != ")":
            return self.FAIL
        index += 1
        function_call = StatementParse(index, "arguments")
        function_call.children = arguments_parse.children  # set function call children to args children
        return function_call

    def __parse_arguments(self, string, index):
        argument_parse = StatementParse(index, "arguments")
        expression_parse = self.__parse(string, index, "expression")
        if expression_parse != self.FAIL:
            index = expression_parse.index
            argument_parse.children.append(expression_parse)  # if there was an argument add to children
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        parse = None  # declare parse
        while index < len(string) and parse != self.FAIL:
            if string[index] != ",":
                parse = self.FAIL
                break
            index += 1  # add one for comma
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
            expression_parse = self.__parse(string, index, "expression")
            if expression_parse == self.FAIL:
                parse = self.FAIL
                break
            index = expression_parse.index
            argument_parse.children.append(expression_parse)
            op_space = self.__parse(string, index, "op_space")  # parse optional space
            if op_space != self.FAIL:
                index = op_space.index  # add op_space to index
        argument_parse.index = index  # add index to arg parse
        return argument_parse

    def __parse_return_statement(self, string, index):
        ret_key = string[index:index + 3]
        if ret_key != "ret":  # check for return key and add to index
            return self.FAIL
        index += 3
        req_space = self.__parse(string, index, "req_space")
        if req_space == self.FAIL:  # if no req_space fail
            return self.FAIL
        index = req_space.index
        expression_parse = self.__parse(string, index, "expression")
        if expression_parse == self.FAIL:
            return self.FAIL
        index = expression_parse.index
        op_space = self.__parse(string, index, "op_space")  # parse optional space
        if op_space != self.FAIL:
            index = op_space.index  # add op_space to index
        if string[index] != ";":
            return self.FAIL
        index += 1
        return_statement = StatementParse(index, "return")
        return_statement.children.append(expression_parse)
        return return_statement

    def test(self):
        parser = Parser()
        interpreter = Interpreter()

        # term = parser.parse("var x = 0; x = x + 5*44; print x;", "program")  # 6
        # term = parser.parse("var printer = func(){ print 1; }; ", "program")  # 6
        term = parser.parse('''# testing comparison expression syntax and it only allowing one 'tail'

if (1 < 2 > 3 != 4){
    print 1;
}
else {
    print 0;
}''')  # test for function insdie of a dunction
        # term = parser.parse("var a = 1; var outer = func(){ var inner = func(){print a;}; ret inner; };  var foo = outer(); a =3; foo(); ", "program")  # test for function insdie of a dunction

        # term = parser.parse("var a = 1; var outer = func(){ var a = 2; print a; }; outer(); ", "program")  # test for function insdie of a dunction

        print(term.__str__())
        x = interpreter.execute(term)
        #  ret inner;


#  var a = 1; var outer = func(){ var a = 2; var inner = func(){ print a;}; ret inner ; };
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
