precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'))


def p_error(p):
    print("parsing error\n")


def p_start(p):
    """start : expression"""
    print("p[1]=", p[1])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_var(p):
    """expression : VAR"""
    p[0] = p[1]


def p_expression_sum(p):
    """EXPRESSION : EXPRESSION '+' EXPRESSION
                  | EXPRESSION '-' EXPRESSION"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]


def p_expression_mul(p):
    """EXPRESSION : EXPRESSION '*' EXPRESSION
                  | EXPRESSION '/' EXPRESSION"""
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    """EXPRESSION : '(' EXPRESSION ')'"""
    p[0] = p[2]


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""

def p_instructions_opt_1(p):
    """instructions_opt : instructions """

def p_instructions_opt_2(p):
    """instructions_opt : """

def p_instructions_1(p):
    """instructions : instructions instruction """

def p_instructions_2(p):
    """instructions : instruction """