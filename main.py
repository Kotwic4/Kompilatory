import sys

from parser import parser
from scaner import lexer, find_column

# operatory binare: +, -, *, /
# macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
# operatory przypisania: =, +=, -=, *=, /=
# operatory relacyjne: <, >, <=, >=, !=, ==
# nawiasy: (,), [,], {,}
# operator zakresu: :
# transpozycja macierzy: '
# przecinek i średnik: , ;

# słowa kluczowe: if, else, for, while
# instructions break, continue and return
# słowa kluczowe: eye, zeros and ones
# słowa kluczowe: print
# identyfikatory
# liczby całkowite
# liczby zmiennoprzecinkowe


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example0.m"
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

    parser.parse(text, lexer=lexer)
