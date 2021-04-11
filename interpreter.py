import sys

# runtime error: type mismatch


class InterpreterService:
    def __init__(self):
        self.environment = self.Environment({}, None)
        self.function_call_depth = 0
        self.return_value = 0
        self.isReturning = False
        self.output = ""
        self.definingMethod = False

    class Closure:
        def __init__(self, parse, environment, parameters):
            self.parse = parse
            self.environment = environment
            self.parameters = parameters
            self.type = "closure"
            self.isMethod = False
            self.parentInstance = None

    class Class:
        def __init__(self, parse, environment):
            self.parse = parse
            self.environment = environment
            self.type = "class"

    class ClassInstance:
        def __init__(self, parse, environment, parent):
            self.parse = parse
            self.environment = environment
            self.type = "class_instance"
            self.instanceOf = parent

    class Environment:

        def __init__(self, variable_map, previous_env):
            self.variable_map = variable_map
            self.type_map = {}
            self.previous_env = previous_env

    def __push_env(self):
        new_env = self.Environment({}, self.environment)  # declare new env with previous of current env
        self.environment = new_env

    def __pop_env(self):
        previous_env = self.environment.previous_env  # get previous
        self.environment = previous_env  # set previous to current env

    def execute(self, node):
        try:
            self.__execute(node)
            return self.output
        except Exception as error:
            print(error)
            return self.output

    def __execute(self, node):
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
        elif node.type == "ifelse":
            self.__execute_if_else_statement(node)
        elif node.type == "while":
            self.__execute_while_statement(node)
        elif node.type == "return":
            self.__execute_return(node)
        else:
            self.__eval(node)

    def transform_eval(self, node):
        if node.type == "+":
            return self.__eval_plus(node)
        elif node.type == "-":
            return self.__eval_minus(node)
        elif node.type == "*":
            return self.__eval_mult(node)
        elif node.type == "/":
            return self.__eval_divide(node)

    def __eval(self, node):
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
            return self.__eval_call(node)
        elif node.type == "class":
            return self.__eval_class(node)
        elif node.type == "memloc":
            return self.__eval_memloc(node)
        elif node.type == "member":
            return self.__eval_member(node)
        else:
            raise ValueError("unknown eval type")

    def __execute_program(self, program):
        for node in program.children:
            if self.isReturning:
                break
            self.__execute(node)

    def __execute_return(self, node):
        if self.function_call_depth <= 0:
            self.output += "runtime error: returning outside function" + "\n"
            raise ValueError("runtime error: returning outside function")
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
        val_to_be_assigned = self.__eval(node.children[1])
        lookup = node.children[0]  # get the lookup
        var_name = lookup.value
        env = self.__eval(lookup)
        if node.children[0].type == "memloc" and (var_name not in env.variable_map.keys()):
            self.output += "runtime error: undefined member" + "\n"
            raise ValueError("runtime error: undefined member")
        # check the type safety
        self.__check_type_safety(var_name, val_to_be_assigned, env)
        env.variable_map[var_name] = val_to_be_assigned  # set the var in the env = to the expression
        # fails when assignig memloc node.left to temp,. it gets the temp env incorrectly
        # the prib is when its going to get the this, it gets the main env, not the node class env
        return

    # (assign (memloc (varloc this) value) (lookup value))
    def __execute_declaration_statement(self, node):
        type = "var"  # should be var if there is not type given
        # eval the value on left side
        val_assigned_index = 1
        var_name_index = 0
        if len(node.children) > 2:  # change index and get type
            val_assigned_index = 2
            var_name_index = 1
            type = node.children[0]
        variable_name = node.children[var_name_index].value  # get the var name
        val_to_be_assigned = self.__eval(node.children[val_assigned_index]) # eval the value
        self.environment.type_map[variable_name] = type  # add the type to env
        if type != "var":  # if not var check safety
            self.__check_type_safety(variable_name, val_to_be_assigned, self.environment)
        # if var name already in keys throw a already declared error
        declared_vars = self.environment.variable_map.keys()
        if variable_name in declared_vars:
            self.output += "runtime error: variable already defined" + "\n"
            raise ValueError("runtime error: variable already defined")
        self.environment.variable_map[variable_name] = val_to_be_assigned
        # return

    def __check_type_safety(self, var_name, value, env):
        expected_type = env.type_map[var_name]
        actual_type = self.__get_type(value)
        if expected_type != actual_type:
            self.output += "runtime error: type mismatch" + "\n"
            raise AssertionError("runtime error: type mismatch")
        return

    def __get_type(self, value):
        if isinstance(value, int):
            return "int"
        if isinstance(value, self.Closure):
            return "func"

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

    def __check_duplicate_args(self, argumentsArray):
        ''' Check if given list contains any duplicates '''
        args_as_strings = []
        for arg in argumentsArray:
            args_as_strings.append(arg.value)
        values = {k: 0 for k in args_as_strings}
        for arg in args_as_strings:
            values[arg] += 1
            if values[arg] > 1:
                return True
        return False

    def __check_for_this(self, argumentsArray):
        ''' Check if given list contains any duplicates '''
        args_as_strings = []
        for arg in argumentsArray:
            args_as_strings.append(arg.value)
        if "this" in args_as_strings:
            return True
        self.output += "runtime error: argument mismatch" + "\n"
        raise ValueError("runtime error: argument mismatch")

    def __eval_function(self, node):
        is_typed = len(node.children) == 3
        params_index = 0
        program_index = 1
        if is_typed:
            signature = node.children[0]
            params_index = 1
            program_index = 2
        current_env = self.environment  # copy the current env
        function_params = node.children[params_index].children
        contains_duplicates = self.__check_duplicate_args(function_params)
        if contains_duplicates:
            self.output += "runtime error: duplicate parameter" + "\n"
            raise ValueError("runtime error: duplicate parameter")
        params_array = []
        types_array = ["var" for i in range(len(function_params))]
        if is_typed:
            types_array = signature.children
        for param in function_params:
            params_array.append(param.value)
        function_closure = self.Closure(node, current_env, params_array)
        function_closure.types_array = types_array
        if self.definingMethod:
            self.__check_for_this(function_params)
            function_closure.isMethod = True
        return function_closure

    def __eval_call(self, node):
        self.function_call_depth += 1  # set current depth plus one
        closure = self.__eval(node.children[0])
        if closure is None:
            self.output += "runtime error: undefined function" + "\n"
            raise ValueError("runtime error: undefined function")
        if not (isinstance(closure, self.Closure) or isinstance(closure, self.Class)):
            self.output += "runtime error: calling a non-function" + "\n"
            raise ValueError("runtime error: calling a non-function")
        if isinstance(closure, self.Class):
            # declare a class instance
            classInstance = self.ClassInstance(closure.parse, closure.environment, node.func_name)
            return classInstance
        # if isinstance()
        # eval1 = self.__eval(node.children[0])
        has_signature = len(closure.parse.children) == 3
        arguments = node.children[1].children
        evaluated_args = []
        if closure.isMethod or ("this" in closure.parameters):
            # FIXME look for the parent/ add the methods's env
            evaluated_args.append(closure.environment)  # if a closure, append the class instance for the "this"
        for arg in arguments:
            evaluated_args.append(self.__eval(arg))
        current_env = self.environment
        self.environment = closure.environment  # set the current env to the closure env
        self.__push_env()  # push a new env on stack
        # check that the len of closure params and call args are the same
        if len(closure.parameters) != len(evaluated_args):
            self.output += "runtime error: argument mismatch" + "\n"
            raise ValueError("runtime error: argument mismatch")
        # add the type to the env
        for i in range(len(closure.parameters)):
            self.environment.type_map[closure.parameters[i]] = closure.types_array[i]  # add type to the env
            self.__check_type_safety(closure.parameters[i], evaluated_args[i], self.environment)  # check if type safe
            self.environment.variable_map[closure.parameters[i]] = evaluated_args[i]
        program_index = 1
        if has_signature:
            program_index = 2
        function_program = closure.parse.children[program_index]
        self.__execute(function_program)  # execute the IR tree of the function
        self.__pop_env()
        self.environment = current_env  # set the env back to the current env
        # FIXME CHECK THE RETURN VASLUE
        return_value = self.return_value
        self.return_value = 0  # set return value back
        self.isReturning = False
        self.function_call_depth -= 1  # decrease function depth by one
        if closure.types_array[-1] != "var":
            self.__check_return_type_safety(closure.types_array[-1], return_value)  # check return type safety
        return return_value  # return 0 or the return value


    def __check_return_type_safety(self, expected_type, value):
        actual_type = self.__get_type(value)
        if expected_type != actual_type:
            self.output += "runtime error: type mismatch" + "\n"
            raise AssertionError("runtime error: type mismatch")
        return False



    def __eval_class(self, node):
        self.__push_env()
        self.definingMethod = True
        for child in node.children:
            self.__execute(child)
        class_env = self.environment
        callable = self.Class(node, class_env)
        self.__pop_env()
        self.definingMethod = False
        return callable

    def __eval_memloc(self, node):
        try:
            instance_location = self.__eval(node.children[0])
            instance_name = node.children[0].value
            class_instance = instance_location.variable_map[instance_name]
            if isinstance(class_instance, self.Environment):  # if the instance is a class env then return
                return class_instance
            class_env = class_instance.environment
            return class_env
        except AttributeError:
            self.output += "runtime error: undefined variable" + "\n"
            raise ValueError("runtime error: undefined variable")
        return

        # return
        # pass

    def __eval_member(self, node):
        class_instance = self.__eval(node.children[0])  # eval class lookup
        member = node.children[1].value
        if isinstance(class_instance, self.Environment):
            class_env = class_instance
            value = class_env.variable_map[member]
            return value
        value = class_instance.environment.variable_map[member]
        if isinstance(value, self.Closure):
            value.isMethod = True
            value.parentInstance = class_instance
        return value

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
            return result_env
        except AttributeError:
            self.output += "runtime error: undefined variable" + "\n"
            raise ValueError("runtime error: undefined variable")
        # may need to check if this return the env

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
            self.output += "runtime error: undefined variable" + "\n"
            raise ValueError("runtime error: undefined variable")
        result_value = result_env.variable_map[variable_name]
        return result_value

    def __eval_plus(self, node):
        left_sum = self.__eval(node.children[0])
        right_sum = self.__eval(node.children[1])
        if isinstance(left_sum, self.Closure) or isinstance(right_sum, self.Closure):
            self.output += "runtime error: math operation on functions" + "\n"
            raise ValueError("runtime error: math operation on functions")
        sum = left_sum + right_sum
        return sum

    def __eval_minus(self, node):
        left_difference = self.__eval(node.children[0])
        right_difference = self.__eval(node.children[1])
        if isinstance(left_difference, self.Closure) or isinstance(right_difference, self.Closure):
            self.output += "runtime error: math operation on functions" + "\n"
            raise ValueError("runtime error: math operation on functions")
        difference = left_difference - right_difference
        return difference

    def __eval_divide(self, node):
        left_divide = self.__eval(node.children[0])
        right_divide = self.__eval(node.children[1])
        if isinstance(left_divide, self.Closure) or isinstance(right_divide, self.Closure):
            self.output += "runtime error: math operation on functions" + "\n"
            raise ValueError("runtime error: math operation on functions")
        if right_divide == 0:
            self.output += "runtime error: divide by zero" + "\n"
            raise ValueError("runtime error: divide by zero")
        quotient = left_divide // right_divide
        return quotient

    def __eval_mult(self, node):
        left_mult = self.__eval(node.children[0])
        right_mult = self.__eval(node.children[1])
        if isinstance(left_mult, self.Closure) or isinstance(right_mult, self.Closure):
            self.output += "runtime error: math operation on functions" + "\n"
            raise ValueError("runtime error: math operation on functions")
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
        not_expression = not (self.__eval(node.children[0]))
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
