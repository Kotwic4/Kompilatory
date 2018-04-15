import ply.lex as lex

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


def t_ignore_COMMENT(t):
    r'\#.*'


def t_FLOAT(t):
    r'(\d+\.\d*|\.\d+)(e-?\d+)?'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'0|([1-9]\d*)'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"'
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
