import sys

from ply import yacc

from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from mparser import Parser


def read_file():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example10B.m"
        file = open(filename, "r")
        text = file.read()
        file.close()
        return text
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)


def parse(text):
    m_parser = Parser(debug=False)
    parser = yacc.yacc(module=m_parser)
    ast = parser.parse(text, lexer=m_parser.scanner)
    if m_parser.error:
        sys.exit(1)
    return ast


def print_tree(ast):
    TreePrinter()
    ast.printTree()


def check_semantic(ast):
    type_checker = TypeChecker()
    type_checker.visit(ast)
    if type_checker.errors:
        sys.exit(1)


def main():
    text = read_file()
    ast = parse(text)
    # print_tree(ast)
    check_semantic(ast)


if __name__ == '__main__':
    main()
