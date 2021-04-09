from transformer import ConstantFoldingTransform
from langParser import Parser
from interpreter import InterpreterService

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
    transformer = ConstantFoldingTransform()
    interpreter = InterpreterService()

    term = parser.test()
    # x = interpreter.execute(term)

    transformed_term = transformer.visit(term)
    print(transformed_term)
    # x = interpreter.execute(transformed_term)


if __name__ == '__main__':
    main()
