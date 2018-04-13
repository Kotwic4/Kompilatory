import sys
from scaner import lexer, find_column

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    file.close()
    lexer = lexer
    lexer.input(text)

    while True:
        tok = lexer.token()
        if not tok:
            break
        column = find_column(text, tok)
        print("(%d,%d): %s(%s)" % (tok.lineno, column, tok.type, tok.value))
