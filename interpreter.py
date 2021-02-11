



class Interpreter:
    def __init__(self):
        self.environment = self.Environment({}, None)

    class Environment:
        def __init__(self, variable_map, previous_env):
            self.variable_map = variable_map
            self.previous_env = previous_env


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
        env = self.environment
        result_env = None
        while (env is not None):
            if variable_name in env.variable_map.keys():
                result_env = env
                break
            env = env.previous_env

        if result_env == None:  # if the var name does not exist it is undefined
            raise Exception("variable is not defined")
        assignment_result = self.eval(node.children[1])
        result_env.variable_map[variable_name] = assignment_result  # set the variable as the key in the env dict
        return

    def __execute_declaration_statement(self, node):
        # eval things on the right side of the equation
        assignment_statement = node.children[0]
        variable_name = assignment_statement.children[0].value
        #if item already in keys throw a already declared error
        declared_vars = self.environment.variable_map.keys()
        if variable_name in declared_vars:
            raise Exception("variable already defined")
        if self.__check_forbidden_names(variable_name):
            raise Exception("forbidden variable name")  # check for exceptions on variable name
        self.environment.variable_map[variable_name] = ""
        self.__execute_assignment_statement(assignment_statement)
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
