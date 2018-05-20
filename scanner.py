import ply.lex as lex


class Scanner:
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT'
    }

    tokens = [
                 'M_PLUS',
                 'M_MINUS',
                 'M_TIMES',
                 'M_DIVIDE',

                 'PLUS_ASSIGN',
                 'MINUS_ASSIGN',
                 'TIMES_ASSIGN',
                 'DIVIDE_ASSIGN',

                 'EQ',
                 'NEQ',
                 'GE',
                 'LE',

                 'ID',
                 'FLOAT',
                 'INT',
                 'STRING'
             ] + list(reserved.values())

    literals = "+-*/()[]{}:,;'><="

    t_M_PLUS = r'\.\+'
    t_M_MINUS = r'\.-'
    t_M_TIMES = r'\.\*'
    t_M_DIVIDE = r'\./'
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GE = r'>='
    t_LE = r'<='

    t_ignore = ' \t\r'

    def __init__(self):
        self.lexer = lex.lex(object=self)

    def t_ignore_COMMENT(self, t):
        r'\#.*'

    def t_FLOAT(self, t):
        r'(\d+\.\d*|\.\d+)(e-?\d+)?'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'0|([1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
        t.lexer.skip(1)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def find_column(self, token):
        line_start = self.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
