from interpreter import InterpreterService
from langParser import *
import sys
from math import copysign
from copy import deepcopy


class ConstantFoldingTransform:
    def __init__(self):
        self.interpreter = InterpreterService()
        self.parser = Parser()
        self.sign = lambda x: copysign(1, x)

    def is_add_sub(self, node):
        return node.type in '+-'

    def is_mul_div(self, node):
        return node.type in '*/'

    def visit(self, node):
        if not hasattr(node, "children"):
            return node
        children = []
        for child in node.children:
            if isinstance(child, StatementParse):
                child = self.visit(child)
                if not self.is_add_sub(node) and self.is_add_sub(child):
                    child = self.add_sub_transform(child)
            children.append(child)
        node.children = children
        if self.is_mul_div(node):
            return self.mul_div_transform(node)
        else:
            return node

    def add_sub_transform(self, node):
        untouched_node = deepcopy(node)
        try:
            # problem with expansion
            child_one = self.expand(node.children[0])
            if node.type == "-":
                node.children[1] = self.flip_sign(node.children[1])
            child_two = self.expand(node.children[1])
            if isinstance(child_one, IntergerParse) and isinstance(child_two, IntergerParse):
                simple_add = child_one.value + child_two.value
                return IntergerParse(simple_add, 0)
            new_statement = self.arrange_terms(child_one, child_two)
            if new_statement is not None:
                return new_statement
        except Exception:  # if an unexpected type like logical operators will fail and return untouched node
            return untouched_node  # FIXME

    def mul_div_transform(self, node):
        child_one = node.children[0]
        child_two = node.children[1]
        if self.is_divide_by_zero(node):  # if divide by zero don't change
            return node
        if isinstance(child_one, IntergerParse) and isinstance(child_two, IntergerParse):
            result_mult_div = self.interpreter.transform_eval(node)
            return IntergerParse(result_mult_div, 0)
        return node  # FIXME

    def is_divide_by_zero(self, node):

        # recursively check children for the error
        if self.is_node_divide_by_zero(node):
            return True
        is_error = False
        if node.type == "/":
            for child in node.children:
                if child.type == "/":
                    if self.is_divide_by_zero(child):
                        is_error = True
                        return
        return is_error

    def is_node_divide_by_zero(self, node):
        try:
            # check if child two has a divide by zero error
            if node.type == "/":
                child_two = node.children[1]
                if child_two.value == 0:
                    return True
        except Exception:
            return False

    def arrange_terms(self, child_one, child_two):
        all_children = []
        # get all children from 1
        if isinstance(child_one, list):
            for child in child_one:
                all_children.append(child)
        else:
            all_children.append(child_one)

        # get all children from 2
        if isinstance(child_two, list):
            for child in child_two:
                all_children.append(child)
        else:
            all_children.append(child_two)

        # move the constants to the back
        result_sum = 0
        remaining_children = []
        for child in all_children:
            if isinstance(child, IntergerParse):
                result_sum += child.value
            else:
                remaining_children.append(child)

        resulting_parse_tree = self.get_new_parse_tree(result_sum, remaining_children)
        return resulting_parse_tree

    def get_new_parse_tree(self, result_sum, remaining_children):
        if len(remaining_children) == 0:
            if result_sum < 0:
                new_statement = StatementParse(0, "-")
                new_statement.children.append(IntergerParse(0, 0))
                new_statement.children.append(IntergerParse(result_sum * -1, 0))
                return new_statement
            return IntergerParse(result_sum, 0)
        result_sum = IntergerParse(result_sum, 0)
        if result_sum.value != 0:
            remaining_children.append(result_sum)  # add the sum as the last child
        if not self.is_positive(remaining_children[0]):  # re-arange a postive value to be fist if there is not already
            first_positive = self.find_first_positive(remaining_children)
            if first_positive is not None:
                remaining_children.remove(first_positive)  # remove the first positive
                remaining_children.insert(0, first_positive)  # and add it in back in at the front
            else:
                remaining_children.insert(0, IntergerParse(0, 0))  # add a zero up front if all negative
        # now create the new IR representation
        result_string = ""
        result_string += self.get_child_as_string(remaining_children[0])
        remaining_children.pop(0)  # remove the elemnt at 0 that was just added
        for child in remaining_children:
            if self.is_positive(child):
                result_string += " + " + self.get_child_as_string(child)
            else:
                child = self.flip_sign(child)
                result_string += " - " + self.get_child_as_string(child)
        result_string += ";"
        new_ir_tree = self.parser.parse(result_string)
        return new_ir_tree.children[0]

    def get_child_as_string(self, node):
        if node.type in "*/":
            return self.mult_div_as_string(node)
        if node.type in "+-":
            return self.add_sub_as_string(node)
        if isinstance(node, CallExpression):
            return self.call_expression_as_string(node)
        return str(node.value)
    #create a get string as add minus

    def call_expression_as_string(self, node):
        result_string = ""
        var_name = node.children[0].value
        arguments = node.children[1].children
        result_string += " " + var_name + "(" + " "
        for arg in arguments:
            result_string += arg.value + ", "
        result_string += " )"
        return result_string




    def mult_div_as_string(self, node):
        result_string = "("
        child_one = self.get_child_as_string(node.children[0])
        result_string += child_one + " "
        child_two = self.get_child_as_string(node.children[1])
        result_string += " " + node.type + " "
        result_string += child_two + ") "
        return result_string

    def add_sub_as_string(self, node):
        result_string = "("
        child_one = self.get_child_as_string(node.children[0])
        result_string += child_one + " "
        child_two = self.get_child_as_string(node.children[1])
        result_string += " " + node.type + " "
        result_string += child_two + ") "
        return result_string

    def deprecated_get_new_parse_tree(self, result_sum, remaining_children):
        result_sum = IntergerParse(result_sum, 0)
        if result_sum.value != 0:
            remaining_children.append(result_sum)  # add the sum as the last child
        if not self.is_positive(remaining_children[0]):  # re-arange a postive value to be fist if there is not already
            first_positive = self.find_first_positive(remaining_children)
            remaining_children.remove(first_positive)  # remove the first positive
            remaining_children.insert(0, first_positive)  # and add it in back in at the front
        # now create the new IR representation
        sign = self.get_sign(remaining_children[1])  # get the sign of the next element
        new_statement = StatementParse(0, sign)
        new_statement.children.append(remaining_children[0])
        remaining_children.pop(0)  # remove the elemnt at 0 that was just added
        parent = new_statement
        counter = 0
        for child in remaining_children:
            sign = self.get_sign(child)
            flipped_child = child
            if not self.is_positive(child):
                flipped_child = self.flip_sign(child)
            if len(parent.children) <= 1:
                parent.children.append(flipped_child)
            else:
                new_statement = StatementParse(0, sign)
                new_statement.children.append(parent)
                if counter + 1 >= len(remaining_children):
                    new_statement.children.append(flipped_child)
                parent = new_statement
            counter += 1
        return parent

    def find_first_positive(self, list_of_children):
        for child in list_of_children:
            if self.is_positive(child):
                return child
        return None

    def recursive_solution(self, child_one, child_two):
        remaining_children = []
        result_sum = child_two.value
        for child in child_one:
            if isinstance(child, IntergerParse):
                result_sum += child.value
            else:
                remaining_children.append(child)
        # remaining_children.append(result)
        result_sum = IntergerParse(result_sum, 0)
        if result_sum.value != 0:
            remaining_children.append(result_sum)  # add the sum as the last child
        if not self.is_positive(remaining_children[0]):  # re-arange a postive value to be fist if there is not already
            first_positive = self.find_first_positive(remaining_children)
            remaining_children.remove(first_positive)  # remove the first positive
            remaining_children.insert(0, first_positive)  # and add it in back in at the front
        # now create the new IR representation
        sign = self.get_sign(remaining_children[1])  # get the sign of the next element
        new_statement = StatementParse(0, sign)
        new_statement.children.append(remaining_children[0])
        remaining_children.pop(0)  # remove the elemnt at 0 that was just added
        parent = new_statement
        counter = 0
        for child in remaining_children:
            sign = self.get_sign(child)
            flipped_child = child
            if not self.is_positive(child):
                flipped_child = self.flip_sign(child)
            if len(parent.children) <= 1:
                parent.children.append(flipped_child)
            else:
                new_statement = StatementParse(0, sign)
                new_statement.children.append(parent)
                if counter + 1 >= len(remaining_children):
                    new_statement.children.append(flipped_child)
                parent = new_statement
            counter += 1
        return parent

    # if sign == "-":  # FIXME instead use the flip sign function
    #     node.children[0] = self.flip_sign(node.children[0])
    #     node.children[1] = self.flip_sign(node.children[1])

    def expand(self, node):
        all_children = []
        if hasattr(node, "children") and node.type == "-":
            node.children[1] = self.flip_sign(node.children[1])
        if hasattr(node, "children") and len(node.children) != 0 and node.type in '+-':
            for child in node.children:
                    # all chidlren = all chidlren retiurn val
                if child.type in "+-":
                    all_children += self.expand(child)  # could require fixme - the sign of the flipped children
                    continue
                all_children.append(child)
            return all_children
        return node

    def flip_sign(self, node):
        if isinstance(node, IntergerParse):
            node.value = node.value * -1
            return node
        if node.type in '*/':
            node = self.flip_mult_div_sign(node)
            return node
        if node.type in "+-":
            if node.type == "+":
                node = self.flip_add(node)
            elif node.type == "-":
                node = self.flip_sub(node)
            return node
        if isinstance(node, CallExpression):
            node.sign = "-"
            return node
        if node.value[0] == "-":
            node.value = node.value[1:]
            node.sign = "+"
            return node
        node.value = "-" + node.value
        node.sign = "-"
        return node

    def flip_add(self, node):
        node.type = "+"
        # set to plus and set all values as opposite
        for child in node.children:
            self.flip_sign(child)
        return node

    def flip_sub(self, node):
        if self.is_positive(node.children[1]):  # flip the sign to negative because it should be
            self.flip_sign(node.children[1])  # flip child after - sign
        node.type = "+"
        # set to plus and set all values as opposite
        for child in node.children:
            self.flip_sign(child)
        return node

    def make_negative(self, node):
        if node.type in '*/':
            node.sign = "-"
            return node
        if isinstance(node, IntergerParse):
            node.value = node.value * -1
            return node
        if node.type in "+-":
            node = self.flip_sub(node)
            return node
        node.value = "-" + node.value
        node.sign = "-"
        return node

    def get_sign(self, node):
        is_positive = self.is_positive(node)
        if is_positive:
            return "+"
        return "-"

    def flip_mult_div_sign(self, node):
        if hasattr(node, "sign"):
            if node.sign == "-":
                node.sign = "+"
            else:
                node.sign = "-"
            return node
        else:
            node.sign = "-"
            return node

    def is_positive(self, node):
        '''
        returns True for positive sign, False for negative sign
        :param node:
        :return: True(+) or False(-)
        '''
        if node.type in "*/":
            if hasattr(node, "sign"):
                if node.sign == "-":
                    return False
                else:
                    return True
            else:
                return True
        if isinstance(node, CallExpression):
            if hasattr(node, "sign"):
                if node.sign == "-":
                    return False
                else:
                    return True
            else:
                return True
        if isinstance(node, IntergerParse):
            if node.value < 0:
                return False
            else:
                return True
        try:
            if node.value[0] == "-":
                return False
        except AttributeError:
            return True
        return True