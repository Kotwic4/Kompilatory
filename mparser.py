import ply.yacc as yacc

import ast
import scaner


class Parser:

    def __init__(self, scanner, debug=False):
        self.scanner = scanner
        self.debug = debug
        self.error = False

    tokens = scaner.Scanner.tokens

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN'),
        ('right', '='),
        ('nonassoc', '>', '<', 'EQ', 'NEQ', 'GE', 'LE',),
        ('left', 'STH'),
        ('left', '+', '-', 'M_PLUS', 'M_MINUS'),
        ('left', '*', '/', 'M_TIMES', 'M_DIVIDE'),
        ('left', 'TRANSPOSE'),
        ('right', 'UNARY')
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")
        self.error = True

    def p_start(self, p):
        """start : INSTRUCTIONS"""
        p[0] = p[1]
        if self.debug:
            print('p_start: {}'.format(p[0]))

    def p_instructions(self, p):
        """INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                        | INSTRUCTION"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        if self.debug:
            print('p_instructions: {}'.format(p[0]))

    def p_instruction(self, p):
        """INSTRUCTION : STATEMENT ';'
                       | IF_STATEMENT
                       | WHILE_STATEMENT
                       | FOR_STATEMENT"""
        p[0] = p[1]
        if self.debug:
            print('p_instruction: {}'.format(p[0]))

    def p_statement(self, p):
        """STATEMENT : ASSIGNMENT
                     | KEYWORD"""
        p[0] = p[1]
        if self.debug:
            print('p_statement: {}'.format(p[0]))

    def p_assignment(self, p):
        """ASSIGNMENT : LEFT_ASSIGNMENT ASSIGNMENT_OPERATOR EXPRESSION"""
        p[0] = ast.Assignment(p[1], p[2], p[3])
        if self.debug:
            print('p_assignment: {}'.format(p[0]))

    def p_left_assignment(self, p):
        """LEFT_ASSIGNMENT : ID
                           | ACCESS"""
        p[0] = ast.AssignTo(p[1])
        if self.debug:
            print('p_left_assignment: {}'.format(p[0]))

    def p_access(self, p):
        """ACCESS : ID '[' SEQUENCE ']'"""
        p[0] = ast.Access(p[1], p[3])
        if self.debug:
            print('p_access: {}'.format(p[0]))

    def p_sequence(self, p):
        """SEQUENCE : SEQUENCE ',' EXPRESSION
                    | EXPRESSION"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        if self.debug:
                print('p_sequence: {}'.format(p[0]))

    def p_value(self, p):
        """VALUE : FLOAT
                 | INT
                 | STRING
                 | ID
                 | MATRIX
                 | ACCESS"""
        p[0] = p[1]
        if self.debug:
            print('p_value: {}'.format(p[0]))

    def p_matrix(self, p):
        """MATRIX : '[' ROWS ']'"""
        p[0] = p[2]
        if self.debug:
            print('p_matrix: {}'.format(p[0]))

    def p_rows(self, p):
        """ROWS : ROWS ';' SEQUENCE
                | SEQUENCE"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        if self.debug:
            print('p_rows: {}'.format(p[0]))

    def p_expression(self, p):
        """EXPRESSION : VALUE
                      | '-' EXPRESSION %prec UNARY
                      | EXPRESSION "'" %prec TRANSPOSE
                      | '(' EXPRESSION ')'
                      | EXPRESSION MATHEMATICAL_OPERATOR EXPRESSION %prec STH
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
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_keyword(self, p):
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
        if self.debug:
            print('p_keyword: {}'.format(p[0]))

    def p_condition(self, p):
        """CONDITION : EXPRESSION COMPARISION_OPERATOR EXPRESSION"""
        p[0] = ast.Condition(p[1], p[2], p[3])
        if self.debug:
            print('p_condition: {}'.format(p[0]))

    def p_body(self, p):
        """BODY : '{' INSTRUCTIONS '}'
                | INSTRUCTION"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[2]
        if self.debug:
            print('p_body: {}'.format(p[0]))

    def p_if_statement(self, p):
        """IF_STATEMENT : IF '(' CONDITION ')' BODY %prec IFX
                        | IF '(' CONDITION ')' BODY ELSE BODY"""
        if len(p) == 8:
            p[0] = ast.IfElse(p[3], p[5], p[7])
        elif len(p) == 6:
            p[0] = ast.If(p[3], p[5])
        if self.debug:
            print('p_if_statement: {}'.format(p[0]))

    def p_while_statement(self, p):
        """WHILE_STATEMENT : WHILE '(' CONDITION ')' BODY"""
        p[0] = ast.While(p[3], p[5])
        if self.debug:
            print('p_while_statement: {}'.format(p[0]))

    def p_for_statement(self, p):
        """FOR_STATEMENT : FOR ID '=' RANGE BODY"""
        p[0] = ast.For(p[2], p[4], p[5])
        if self.debug:
            print('p_for_statement: {}'.format(p[0]))

    def p_range(self, p):
        """RANGE : EXPRESSION ':' EXPRESSION
                 | EXPRESSION ':' EXPRESSION ':' EXPRESSION"""
        if len(p) == 4:
            p[0] = ast.Range(p[1], p[3])
        elif len(p) == 6:
            p[0] = ast.Range(p[1], p[3], p[5])
        if self.debug:
            print('p_range: {}'.format(p[0]))

    def p_assignment_operator(self, p):
        """ASSIGNMENT_OPERATOR : '='
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | TIMES_ASSIGN
                               | DIVIDE_ASSIGN"""
        p[0] = p[1]
        if self.debug:
            print('p_assignment_operator: {}'.format(p[0]))

    def p_comparision_operator(self, p):
        """COMPARISION_OPERATOR : '<'
                                | '>'
                                | EQ
                                | NEQ
                                | GE
                                | LE"""
        p[0] = p[1]
        if self.debug:
            print('p_comparision_operator: {}'.format(p[0]))

    def p_mathematical_operator(self, p):
        """MATHEMATICAL_OPERATOR : '+'
                                 | '-'
                                 | '*'
                                 | '/'
                                 | M_PLUS
                                 | M_MINUS
                                 | M_TIMES
                                 | M_DIVIDE"""
        p[0] = p[1]
        if self.debug:
            print('p_mathematical_operator: {}'.format(p[0]))

    def p_function(self, p):
        """FUNCTION : EYE
                    | ZEROS
                    | ONES"""
        p[0] = p[1]
        if self.debug:
            print('p_function: {}'.format(p[0]))
