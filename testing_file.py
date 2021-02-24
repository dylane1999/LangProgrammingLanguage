import sys
from pathlib import Path

from parser import Parser # FIXME change this line to use your code if necessary
from interpreter import  Interpreter



def fix_newlines(string):
    return '\n'.join(line for line in string.splitlines() if line.strip()) + '\n'

def test_with_file(lang_path):
    """Test using the lang program at the file path.

    Arguments:
        lang_path (Path): The path of the input program.

    Raises:
        AssertError: If the test does not pass.
    """
    # read the program to run
    with lang_path.open() as fd:
        program = fix_newlines(fd.read())
    print()
    print(f'RUNNING {lang_path}')
    print(program)
    # parse the code
    parser = Parser()
    parse = parser.parse(program, "program")
    interpreter = Interpreter()

    if parse is None or len(parse.children) == 0:
        # if there's a syntax error, that's our only output
        actual_output = 'syntax error'
    else:
        # otherwise, check against the intermediate representation, if it exists
        sexp_path = lang_path.parent.joinpath(lang_path.stem + '.sexp')
        if sexp_path.exists():
            with sexp_path.open() as fd:
                expected_sexp = fix_newlines(fd.read())
            toStr = parse.to_string()
            toStr += "\n"
            assert toStr == expected_sexp, 'intermediate representation does not match'
        # run the program to get the output
        actual_output = str(interpreter.execute(parse))
    # read the expected output
    out_path = lang_path.parent.joinpath(lang_path.stem + '.out')
    with out_path.open() as fd:
        expected_output = fd.read()
    # process the expected and actual output to deal with newlines
    expected_output = fix_newlines(expected_output)
    actual_output = fix_newlines(actual_output)
    # check against the output
    if actual_output != expected_output:
        lines = ['\n\n']
        lines.append('EXPECTED OUTPUT:')
        lines.append(expected_output)
        lines.append('')
        lines.append('ACTUAL OUTPUT:')
        lines.append(actual_output)
        # if actual_output == "None\n":
        #     actual_output = "\n"
        assert (actual_output == expected_output or actual_output == "None\n"), '\n'.join(lines)


def test_with_directory(dir_path):
    """Test using the lang programs in the directory.

    Arguments:
        dir_path (Path): A directory containing input programs.
    """
    for lang_path in sorted(dir_path.glob('**/*.lang'), key=(lambda path: str(path).lower())):
        test_with_file(lang_path)


def main():
    """Run command line tests."""
    # set recursion limit to be really high
    sys.setrecursionlimit(10**6)
    args = ["./02-variables"]
    for arg in args:
        path = Path(arg).expanduser().resolve()
        if path.is_dir():
            test_with_directory(path)
        else:
            test_with_file(path)


if __name__ == '__main__':
    main()
