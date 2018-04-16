import sys

from ply import yacc

import mparser
import scaner

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example5.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    file.close()
    scaner = scaner.Scanner(text)

    # while True:
    #     tok = scaner.lexer.token()
    #     if not tok:
    #         break
    #     column = scaner.find_column(tok)
    #     print("(%d,%d): %s(%s)" % (tok.lineno, column, tok.type, tok.value))
    mparser = mparser.Parser(scaner,debug=True)
    parser = yacc.yacc(module=mparser)
    program = parser.parse(text, lexer=scaner.lexer)
    if mparser.error:
        sys.exit(1)

