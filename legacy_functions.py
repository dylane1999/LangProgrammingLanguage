def __parse_addition_expression(self, string,
                                index):  # @todo add a parse for mult and div expression before and after
    parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
    if parse != self.FAIL:
        index = parse.index
    result = 0
    parse = self.__parse(string, index, "operand")  # parses the addition expression starting at the index given
    if parse == self.FAIL:
        return self.FAIL
    result = parse.value
    index = parse.index
    while index < len(string) and parse != self.FAIL:
        if string[index] != "+":  # parse + and if not then fail
            parse = self.FAIL
            break
        parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "+"
        if parse == self.FAIL:
            parse = self.FAIL
            break
        result += parse.value
        index = parse.index
    return Parse(result, index)


def __parse_subtraction_expression(self, string, index):
    parse = self.__parse(string, index, "space")  # parse spaces before operand and add to index
    if parse != self.FAIL:
        index = parse.index
    result = 0
    parse = self.__parse(string, index, "operand")  # parses the subtraction expression starting at the index given
    if parse == self.FAIL:
        return self.FAIL
    result = parse.value
    index = parse.index
    while index < len(string) and parse != self.FAIL:
        if string[index] != "-":  # parse + and if not then fail
            parse = self.FAIL
            break
        parse = self.__parse(string, parse.index + 1, "operand")  # parse the next operand; jumps +1 because of "+"
        if parse == self.FAIL:
            parse = self.FAIL
            break
        result -= parse.value
        index = parse.index
    return Parse(result, index)