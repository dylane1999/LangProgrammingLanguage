class Interperter():
    output_string = ""
    output_int = 0

    def execute(self, node):
        if node.type == "print":
            try:
                self.__execute_print(node)
            except AssertionError as error:
                print(error)
        else:
            self.eval(node)


    def eval(self, node):
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


    def __execute_print(self, node):
        result = self.eval(node.children[0])
        print(result)

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
        quotient = left_divide // right_divide
        return quotient


    def __eval_mult(self, node):
        left_mult = self.eval(node.children[0])
        right_mult = self.eval(node.children[1])
        product = left_mult * right_mult
        return product

    def __eval_int(self, node):
        return node.value
