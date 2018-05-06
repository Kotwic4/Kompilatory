import sys

from ply import yacc

import mparser
import scaner
from TreePrinter import TreePrinter

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example6.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    file.close()
    scaner = scaner.Scanner(text)
    mparser = mparser.Parser(scaner, debug=False)
    parser = yacc.yacc(module=mparser)
    program = parser.parse(text, lexer=scaner.lexer)
    if mparser.error:
        sys.exit(1)
    program.printTree()
