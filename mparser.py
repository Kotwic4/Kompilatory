import ast
import ply.yacc as yacc
import scaner

tokens = scaner.tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', '-')  # unary minus
)


def p_error(p):
    print('=' * 30)
    print('p_error')
    print("Illegal character %s" % p.value[0])
    print('=' * 30)


def p_start(p):
    """start : INSTRUCTIONS"""
    p[0] = p[1]
    print('p_start: {}'.format(p[0]))


def p_instructions(p):
    """INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                    | INSTRUCTION"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    print('p_instructions: {}'.format(p[0]))


def p_instruction(p):
    """INSTRUCTION : STATEMENT ';'
                   | IF_STATEMENT
                   | WHILE_STATEMENT
                   | FOR_STATEMENT"""
    p[0] = p[1]
    print('p_instruction: {}'.format(p[0]))


def p_statement(p):
    """STATEMENT : ASSIGNMENT
                 | KEYWORD"""
    p[0] = p[1]
    print('p_statement: {}'.format(p[0]))


def p_assignment(p):
    """ASSIGNMENT : LEFT_ASSIGNMENT ASSIGNMENT_OPERATOR EXPRESSION"""
    p[0] = ast.Assignment(p[1], p[2], p[3])
    print('p_assignment: {}'.format(p[0]))


def p_left_assignment(p):
    """LEFT_ASSIGNMENT : ID
                       | ACCESS"""
    p[0] = ast.AssignTo(p[1])
    print('p_left_assignment: {}'.format(p[0]))


def p_access(p):
    """ACCESS : ID '[' SEQUENCE ']'"""
    p[0] = ast.Access(p[1], p[3])
    print('p_access: {}'.format(p[0]))


def p_sequence(p):
    """SEQUENCE : SEQUENCE ',' EXPRESSION
                | EXPRESSION"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    print('p_sequence: {}'.format(p[0]))


def p_value(p):
    """VALUE : FLOAT
             | INT
             | STRING
             | ID
             | MATRIX
             | ACCESS"""
    p[0] = p[1]
    print('p_value: {}'.format(p[0]))


def p_matrix(p):
    """MATRIX : '[' ROWS ']'"""
    p[0] = p[2]
    print('p_matrix: {}'.format(p[0]))


def p_rows(p):
    """ROWS : ROWS ';' SEQUENCE
            | SEQUENCE"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    print('p_rows: {}'.format(p[0]))


def p_expression(p):
    """EXPRESSION : VALUE
                  | '-' EXPRESSION
                  | EXPRESSION "'"
                  | '(' EXPRESSION ')'
                  | EXPRESSION MATHEMATICAL_OPERATOR EXPRESSION
                  | FUNCTION '(' EXPRESSION ')'"""
    if len(p) == 2:  # VALUE
        p[0] = p[1]
    elif len(p) == 3 and p[1] == '-':  # '-' EXPRESSION
        p[0] = ast.Negation(p[2])
    elif len(p) == 3 and p[2] == "'":  # EXPRESSION "'"
        p[0] = ast.Transposition(p[1])
    elif len(p) == 4 and p[1] == '(' and p[3] == ')':  # '(' EXPRESSION ')'
        p[0] = p[2]
    elif len(p) == 5 and p[2] == '(' and p[4] == ')':  # FUNCTION '(' EXPRESSION ')'
        p[0] = ast.Function(p[1], p[3])
    elif len(p) == 4:
        p[0] = ast.Expression(p[1], p[2], p[3])
    print('p_expression: {}'.format(p[0]))


def p_keyword(p):
    """KEYWORD : PRINT SEQUENCE
               | BREAK
               | CONTINUE
               | RETURN EXPRESSION"""
    if p[1] == 'print':
        p[0] = ast.Print(p[2])
    elif p[1] == 'return':
        p[0] = ast.Return(p[2])
    elif p[1] == 'break':
        p[0] = ast.Break()
    elif p[1] == 'continue':
        p[0] = ast.Continue()
    print('p_keyword: {}'.format(p[0]))


def p_condition(p):
    """CONDITION : EXPRESSION COMPARISION_OPERATOR EXPRESSION"""
    p[0] = ast.Condition(p[1], p[2], p[3])
    print('p_condition: {}'.format(p[0]))


def p_body(p):
    """BODY : '{' INSTRUCTIONS '}'
            | INSTRUCTION"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[2]
    print('p_body: {}'.format(p[0]))


def p_if_statement(p):
    """IF_STATEMENT : IF '(' CONDITION ')' BODY
                    | IF '(' CONDITION ')' BODY ELSE BODY"""
    if len(p) == 8:
        p[0] = ast.IfElse(p[3], p[5], p[7])
    elif len(p) == 6:
        p[0] = ast.If(p[3], p[5])
    print('p_if_statement: {}'.format(p[0]))


def p_while_statement(p):
    """WHILE_STATEMENT : WHILE '(' CONDITION ')' BODY"""
    p[0] = ast.While(p[3], p[5])
    print('p_while_statement: {}'.format(p[0]))


def p_for_statement(p):
    """FOR_STATEMENT : FOR ID '=' RANGE BODY"""
    p[0] = ast.For(p[2], p[4], p[5])
    print('p_for_statement: {}'.format(p[0]))


def p_range(p):
    """RANGE : EXPRESSION ':' EXPRESSION
             | EXPRESSION ':' EXPRESSION ':' EXPRESSION"""
    if len(p) == 4:
        p[0] = ast.Range(p[1], p[3])
    elif len(p) == 6:
        p[0] = ast.Range(p[1], p[3], p[5])
    print('p_range: {}'.format(p[0]))


def p_assignment_operator(p):
    """ASSIGNMENT_OPERATOR : '='
                           | PLUS_ASSIGN
                           | MINUS_ASSIGN
                           | TIMES_ASSIGN
                           | DIVIDE_ASSIGN"""
    p[0] = p[1]
    print('p_assignment_operator: {}'.format(p[0]))


def p_comparision_operator(p):
    """COMPARISION_OPERATOR : '<'
                            | '>'
                            | EQ
                            | NEQ
                            | GE
                            | LE"""
    p[0] = p[1]
    print('p_comparision_operator: {}'.format(p[0]))


def p_mathematical_operator(p):
    """MATHEMATICAL_OPERATOR : '+'
                             | '-'
                             | '*'
                             | '/'
                             | M_PLUS
                             | M_MINUS
                             | M_TIMES
                             | M_DIVIDE"""
    p[0] = p[1]
    print('p_mathematical_operator: {}'.format(p[0]))


def p_function(p):
    """FUNCTION : EYE
                | ZEROS
                | ONES"""
    p[0] = p[1]
    print('p_function: {}'.format(p[0]))


parser = yacc.yacc()
