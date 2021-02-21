



class Interpreter:
    def __init__(self):
        self.environment = self.Environment({}, None)


    class Environment:

        def __init__(self, variable_map, previous_env):
            self.variable_map = variable_map
            self.previous_env = previous_env



    def __push_env(self):
        new_env = self.Environment({}, self.environment)  # declare new env with previous of current env
        self.environment = new_env

    def __pop_env(self):
        previous_env = self.environment.previous_env  # get previous
        self.environment = previous_env  # set previous to current env


    def execute(self, node):
        self.__execute(node)




    def __execute(self, node):
        try:
            if node.type == "program":
                try:
                    return self.__execute_program(node)
                except ValueError as error:
                    raise error
            elif node.type == "print":
                try:
                    return self.__execute_print(node)
                except ValueError as error:
                    raise error
            elif node.type == "assign":
                try:
                    self.__execute_assignment_statement(node)
                except ValueError as error:
                    print(error)
            elif node.type == "declare":
                try:
                    self.__execute_declaration_statement(node)
                except ValueError as error:
                    raise error
            elif node.type == "if":
                try:
                    self.__execute_if_statement(node)
                except ValueError as error:
                    raise error
            elif node.type == "if_else":
                try:
                    self.__execute_if_else_statement(node)
                except ValueError as error:
                    print(error)
            elif node.type == "while":
                try:
                    self.__execute_while_statement(node)
                except ValueError as error:
                    raise error
            else:
                self.__eval(node)

        except ValueError as error:
            print(error)
            raise SystemExit



    def __eval(self, node):
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
            elif node.type == "lookup":
                return self.__eval_lookup(node)
            elif node.type == "varloc":
                return self.__eval_varloc(node)
            elif node.type == "==":
                return self.__eval_equals(node)
            elif node.type == "!=":
                return self.__eval_not_equals(node)
            elif node.type == "<=":
                return self.__eval_less_than_equal(node)
            elif node.type == ">=":
                return self.__eval_greater_than_equal(node)
            elif node.type == "<":
                return self.__eval_less_than(node)
            elif node.type == ">":
                return self.__eval_greater_than(node)
            elif node.type == "&&":
                return self.__eval_and_statement(node)
            elif node.type == "||":
                return self.__eval_or_statement(node)
            else:
                raise ValueError("unknown eval type")
        except ValueError as error:
            raise error
# add a method here to get a var

    def __execute_program(self, program):
        for node in program.children:
            self.__execute(node)


    def __execute_print(self, node):
        expression = self.__eval(node.children[0])
        # if isinstance(expression, self.Environment):
        #     print(expression.variable_map[node.children[0].value])  # get the value out of the correct env
        #     return
        print(expression)
        return


        #
        # y = self.__eval(x)
        # lookup = node.children[0]
        # env = self.__eval(lookup)
        # result = env.variable_map[lookup.value]  # get the value out of the correct env
        # print(result)
        # return str(result)

    def __execute_assignment_statement(self, node):
        lookup = node.children[0] # get the lookup
        env = self.__eval(lookup)
        env.variable_map[lookup.value] = self.__eval(node.children[1])  # set the var in the env = to the expression




    def __execute_declaration_statement(self, node):
        # eval things on the right side of the equation
        variable_name = node.children[0].value
        # if item already in keys throw a already declared error
        declared_vars = self.environment.variable_map.keys()
        if variable_name in declared_vars:
            raise ValueError("variable already defined")
        if self.__check_forbidden_names(variable_name):
            raise ValueError("forbidden variable name")  # check for exceptions on variable name
        self.environment.variable_map[variable_name] = self.__eval(node.children[1])
        return



    def __eval_varloc(self, node):
        variable_name = node.value
        env = self.environment
        result_env = None
        while result_env is None:
            if variable_name in env.variable_map.keys():
                result_env = env
                break
            env = env.previous_env

        return result_env


    def __eval_lookup(self, node):
        variable_name = node.value
        env = self.environment
        result_env = None
        while (result_env is None) and (env is not None):
            if variable_name in env.variable_map.keys():
                result_env = env
                break
            env = env.previous_env
        if env is None:
            raise ValueError("variable not defined")
        result_value = result_env.variable_map[variable_name]
        return result_value
    # throw an error in here if there is no value

    # Eval lookup should return the env that the variable is in

    def __execute_if_statement(self, node):
        conditional = self.__eval(node.children[0])
        if conditional:
            self.__push_env()  # add an env on stack
            self.__execute(node.children[1])
            self.__pop_env()  #  pop env from the stack
        return

    def __execute_if_else_statement(self, node):
        conditional = self.__eval(node.children[0])
        self.__push_env()  # add an env on stack
        if conditional:
            self.__execute(node.children[1])
        else:
            self.__execute(node.children[2])
        self.__pop_env()
        return

    def __execute_while_statement(self, node):
        condition = (node.children[0])
        while self.__eval(condition):
            self.__push_env()
            self.__execute(node.children[1])
            self.__pop_env()


    def __eval_plus(self, node):
        left_sum = self.__eval(node.children[0])
        right_sum = self.__eval(node.children[1])
        sum = left_sum + right_sum
        return sum

    def __eval_minus(self, node):
        left_difference = self.__eval(node.children[0])
        right_difference = self.__eval(node.children[1])
        difference = left_difference - right_difference
        return difference

    def __eval_divide(self, node):
        left_divide = self.__eval(node.children[0])
        right_divide = self.__eval(node.children[1])
        if right_divide == 0:
            raise ValueError("runtime error: divide by zero")
        quotient = left_divide // right_divide
        return quotient


    def __eval_mult(self, node):
        left_mult = self.__eval(node.children[0])
        right_mult = self.__eval(node.children[1])
        product = left_mult * right_mult
        return product

    def __eval_int(self, node):
        return node.value

    #for each comparison type I will have to eval both sides and return a boolean if they meet the specied type

    def __eval_equals(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs == rhs:
            return True
        return False


    def __eval_not_equals(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs != rhs:
            return True
        return False

    def __eval_less_than(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs < rhs:
            return True
        return False


    def __eval_greater_than(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs > rhs:
            return True
        return False

    def __eval_less_than_equal(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs <= rhs:
            return True
        return False

    def __eval_greater_than_equal(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs >= rhs:
            return True
        return False


    def __eval_and_statement(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs and rhs:
            return True
        return False


    def __eval_or_statement(self, node):
        lhs = self.__eval(node.children[0])
        rhs = self.__eval(node.children[1])
        if lhs or rhs:
            return True
        return False

# diudnt add and or OR

# CREATE a varloc that returns the env and the lookup should return the env




    ##eval all conditonals


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
