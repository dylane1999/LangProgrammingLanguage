from copy import deepcopy


class Interpreter:
    def __init__(self):
        self.environment = self.Environment({}, None)
        self.function_call_depth = 0
        self.return_value = 0
        self.isReturning = False
        self.output = ""

    class Closure:
        def __init__(self, parse, environment, parameters):
            self.parse = parse
            self.environment = environment
            self.parameters = parameters

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
        return self.output

    # FIXME If statemtns +n closire

    def __execute(self, node):
        try:
            if node.type == "program":
                    self.__execute_program(node)
            elif node.type == "print":
                    self.__execute_print(node)
            elif node.type == "assign":
                    self.__execute_assignment_statement(node)
            elif node.type == "declare":
                    self.__execute_declaration_statement(node)
            elif node.type == "if":
                    self.__execute_if_statement(node)
            elif node.type == "if_else":
                    self.__execute_if_else_statement(node)
            elif node.type == "while":
                    self.__execute_while_statement(node)
            elif node.type == "return":
                    self.__execute_return(node)
            else:
                self.__eval(node)
        except Exception as error:
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
            elif node.type == "!":
                return self.__eval_not(node)
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
            elif node.type == "function":
                return self.__eval_function(node)
            elif node.type == "call":
                return self.__eval_function_call(node)
            else:
                raise ValueError("unknown eval type")
        except ValueError as error:
            raise error

    # add a method here to get a var FIXME add an eval ! expression

    def __execute_program(self, program):
        for node in program.children:
            if self.isReturning:
                break
            self.__execute(node)


    def __execute_return(self, node):
        if self.function_call_depth <= 0:
            raise ValueError("can not return outside of a function")
        return_value = self.__eval(node.children[0])
        self.isReturning = True
        self.return_value = return_value


    def __execute_print(self, node):
        expression = self.__eval(node.children[0])
        if isinstance(expression, self.Closure):
            print("closure")
            self.output += "closure" + "\n"
            return
        if expression is True:
            print(1)
            self.output += "1" + "\n"
            return
        if expression is False:
            print(0)
            self.output += "0" + "\n"
            return
        print(expression)
        self.output += str(expression) + "\n"
        return 

    def __execute_assignment_statement(self, node):
        lookup = node.children[0]  # get the lookup
        env = self.__eval(lookup)
        env.variable_map[lookup.value] = self.__eval(node.children[1])  # set the var in the env = to the expression
        pass

    def __execute_declaration_statement(self, node):
        # eval things on the right side of the equation
        variable_name = node.children[0].value
        # if item already in keys throw a already declared error
        declared_vars = self.environment.variable_map.keys()
        if variable_name in declared_vars:
            raise ValueError("runtime error: variable already defined")
        self.environment.variable_map[variable_name] = self.__eval(node.children[1])
        # return

    def __execute_if_statement(self, node):
        conditional = self.__eval(node.children[0])
        if conditional:
            self.__push_env()  # add an env on stack
            self.__execute(node.children[1])
            self.__pop_env()  # pop env from the stack
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
        while self.__eval(condition) and not self.isReturning:
            self.__push_env()
            self.__execute(node.children[1])
            self.__pop_env()

    def __eval_function(self, node):
        current_env = self.environment  # copy the current env
        function_params = node.children[0].children
        params_array = []
        for param in function_params:
            params_array.append(param.value)
        function_closure = self.Closure(node, current_env, params_array)
        return function_closure

    def __eval_function_call(self, node):
        self.function_call_depth += 1  # set current depth plus one
        if node.children[0].type == "call":   # if child is a call eval call to get closure
            closure = self.__eval(node.children[0])
        else:
            # function_name = node.children[0].value  # if child is not a call get the func name from identifier child
            # function_env = self.__eval(node.children[0])  # get the closure through eval lookup
            closure = self.__eval(node.children[0])  # get the closure through eval lookup
        if closure is None:
            raise ValueError("undefined function")
        # if isinstance()
        # eval1 = self.__eval(node.children[0])
        arguments = node.children[1].children
        evaluated_args = []
        for arg in arguments:
            evaluated_args.append(self.__eval(arg))
        current_env = self.environment
        self.environment = closure.environment  # set the current env to the closure env
        self.__push_env()  # push a new env on stack
        # check that the len of closure params and call args are the same
        if len(closure.parameters) != len(evaluated_args):
            raise ValueError("incorrect number of arguments")
        for i in range(len(closure.parameters)):
            self.environment.variable_map[closure.parameters[i]] = evaluated_args[i]
        function_program = closure.parse.children[1]
        execute_result = self.__execute(function_program)  # execute the IR tree of the function
        self.__pop_env()
        self.environment = current_env  # set the env back to the current env
        return_value = self.return_value
        self.return_value = 0  # set return value back
        self.isReturning = False
        self.function_call_depth -= 1  # decrease function depth by one
        return return_value #return 0 or the return value

    def __eval_varloc(self, node):
        variable_name = node.value
        env = self.environment
        result_env = None
        try:
            while result_env is None:
                if variable_name in env.variable_map.keys():
                    result_env = env
                    break
                env = env.previous_env
        except AttributeError:
            raise ValueError("runtime error: undefined variable")
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

    def __eval_not(self, node):
        not_expression = not(self.__eval(node.children[0]))
        return not_expression


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


