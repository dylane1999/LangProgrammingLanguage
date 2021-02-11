class Interpreter():
    output_string = ""
    output_int = 0

    def execute(self, node):
        try:
            if node.type == "print_statement":
                try:
                    return self.__execute_print(node)
                except Exception as error:
                    raise SyntaxError
            elif node.type == "assignment_statement":
                try:
                    self.__execute_assignment_statement(node)
                except Exception as error:
                    raise SyntaxError
            elif node.type == "declaration_statement":
                try:
                    self.__execute_declaration_statement(node)
                except Exception as error:
                    raise SyntaxError
            else:
                self.eval(node)

        except Exception as error:
            return "syntax error"



    def eval(self, node):
        try:
            if node.type == "+":
                return self.__eval_plus(node)
            elif node.type == "-":
                return self.__eval_minus(node)
            elif node.type == "*":
                return self.__eval_mult(node)
            elif node.type == "/":
                return self.__eval_divide(node)
            elif node.type == "int":
                return self.__eval_int(node)
        except Exception as error:
            return error


    def __execute_print(self, node):
        result = self.eval(node.children[0])
        print(result)
        return str(result)

    def __execute_assignment_statement(self, node):
        variable_name = node.children[0].value
        if self.__check_forbidden_names(variable_name):
            raise SyntaxError("forbidden variable name")
        assignment_result = self.eval(node.children[1])
        variable_name = assignment_result
        # @TODO find the correct Environment in the chain, then set its value to the eval of the right hand side
        return

    def __execute_declaration_statement(self, node):
        # eval things on the right side of the equation
        assignment_statement = node.children[0]
        # @TODO create the variable in the curent environemnt
        self.__execute_assignment_statement(assignment_statement)

        # if the var name is a forbidden then synatax erroe
        return


    def __eval_lookup(self, node):
        # @todo find the variable in the correct Environment in the chain nd use its value
        pass

    def __eval_plus(self, node):
        left_sum = self.eval(node.children[0])
        right_sum = self.eval(node.children[1])
        sum = left_sum + right_sum
        return sum

    def __eval_minus(self, node):
        left_difference = self.eval(node.children[0])
        right_difference = self.eval(node.children[1])
        difference = left_difference - right_difference
        return difference

    def __eval_divide(self, node):
        left_divide = self.eval(node.children[0])
        right_divide = self.eval(node.children[1])
        if right_divide == 0:
            raise Exception("runtime error: divide by zero")
        quotient = left_divide // right_divide
        return quotient


    def __eval_mult(self, node):
        left_mult = self.eval(node.children[0])
        right_mult = self.eval(node.children[1])
        product = left_mult * right_mult
        return product

    def __eval_int(self, node):
        return node.value


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
