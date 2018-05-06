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
        ('left', '+', '-', 'M_PLUS', 'M_MINUS'),
        ('left', '*', '/', 'M_TIMES', 'M_DIVIDE'),
        ('left', 'TRANSPOSE'),
        ('right', 'UNARY')
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_column(p),
                                                                                      p.type,
                                                                                      p.value))
        else:
            print("Unexpected end of input")
        self.error = True

    def p_start(self, p):
        """start : INSTRUCTIONS"""
        p[0] = ast.ProgramNode(p[1])
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
                       | BODY_STATEMENT
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
        """ASSIGNMENT : LEFT_ASSIGNMENT '=' EXPRESSION
                      | LEFT_ASSIGNMENT PLUS_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT MINUS_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT TIMES_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT DIVIDE_ASSIGN EXPRESSION"""
        p[0] = ast.AssignmentNode(p[1], p[2], p[3])
        if self.debug:
            print('p_assignment: {}'.format(p[0]))

    def p_left_assignment(self, p):
        """LEFT_ASSIGNMENT : CONST_ID
                           | ACCESS"""
        p[0] = ast.AssignToNode(p[1])
        if self.debug:
            print('p_left_assignment: {}'.format(p[0]))

    def p_access(self, p):
        """ACCESS : CONST_ID '[' SEQUENCE ']'"""
        p[0] = ast.AccessNode(p[1], p[3])
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
        """VALUE : CONST_VALUE
                 | MATRIX
                 | ACCESS"""
        p[0] = p[1]
        if self.debug:
            print('p_value: {}'.format(p[0]))

    def p_const_value(self, p):
        """CONST_VALUE : FLOAT
                       | INT
                       | STRING
                       | ID"""
        p[0] = ast.ConstValueNode(p[1])
        if self.debug:
            print('p_const_value: {}'.format(p[0]))

    def p_const_id(self, p):
        """CONST_ID : ID"""
        p[0] = ast.ConstValueNode(p[1])
        if self.debug:
            print('p_const_id: {}'.format(p[0]))

    def p_matrix(self, p):
        """MATRIX : '[' ROWS ']'"""
        p[0] = ast.MatrixNode(p[2])
        if self.debug:
            print('p_matrix: {}'.format(p[0]))

    def p_rows(self, p):
        """ROWS : ROWS ';' SEQUENCE
                | SEQUENCE"""
        if len(p) == 2:
            p[0] = [ast.VectorNode(p[1])]
        elif len(p) == 4:
            p[1].append(ast.VectorNode(p[3]))
            p[0] = p[1]
        if self.debug:
            print('p_rows: {}'.format(p[0]))

    def p_expression(self, p):
        """EXPRESSION : VALUE
                      | '(' EXPRESSION ')'
                      | '-' EXPRESSION %prec UNARY
                      | EXPRESSION "'" %prec TRANSPOSE
                      | EXPRESSION '+' EXPRESSION
                      | EXPRESSION '-' EXPRESSION
                      | EXPRESSION '*' EXPRESSION
                      | EXPRESSION '/' EXPRESSION
                      | EXPRESSION M_PLUS EXPRESSION
                      | EXPRESSION M_MINUS EXPRESSION
                      | EXPRESSION M_TIMES EXPRESSION
                      | EXPRESSION M_DIVIDE EXPRESSION
                      | EYE '(' EXPRESSION ')'
                      | ZEROS '(' EXPRESSION ')'
                      | ONES '(' EXPRESSION ')'"""
        if len(p) == 2:  # VALUE
            p[0] = p[1]
        elif len(p) == 3 and p[1] == '-':  # '-' EXPRESSION
            p[0] = ast.NegationNode(p[2])
        elif len(p) == 3 and p[2] == "'":  # EXPRESSION "'"
            p[0] = ast.TranspositionNode(p[1])
        elif len(p) == 4 and p[1] == '(' and p[3] == ')':  # '(' EXPRESSION ')'
            p[0] = p[2]
        elif len(p) == 5 and p[2] == '(' and p[4] == ')':  # FUNCTION '(' EXPRESSION ')'
            p[0] = ast.FunctionNode(p[1], p[3])
        elif len(p) == 4:
            p[0] = ast.ExpressionNode(p[1], p[2], p[3])
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_keyword(self, p):
        """KEYWORD : PRINT SEQUENCE
                   | BREAK
                   | CONTINUE
                   | RETURN EXPRESSION"""
        if p[1] == 'print':
            p[0] = ast.PrintNode(p[2])
        elif p[1] == 'return':
            p[0] = ast.ReturnNode(p[2])
        elif p[1] == 'break':
            p[0] = ast.BreakNode()
        elif p[1] == 'continue':
            p[0] = ast.ContinueNode()
        if self.debug:
            print('p_keyword: {}'.format(p[0]))

    def p_condition(self, p):
        """CONDITION : EXPRESSION '<' EXPRESSION
                     | EXPRESSION '>' EXPRESSION
                     | EXPRESSION EQ EXPRESSION
                     | EXPRESSION NEQ EXPRESSION
                     | EXPRESSION GE EXPRESSION
                     | EXPRESSION LE EXPRESSION"""
        p[0] = ast.ConditionNode(p[1], p[2], p[3])
        if self.debug:
            print('p_condition: {}'.format(p[0]))

    def p_body_statement(self, p):
        """BODY_STATEMENT : '{' INSTRUCTIONS '}'"""
        p[0] = ast.BodyNode(p[2])
        if self.debug:
            print('p_body_statement: {}'.format(p[0]))

    def p_if_statement(self, p):
        """IF_STATEMENT : IF '(' CONDITION ')' INSTRUCTION %prec IFX
                        | IF '(' CONDITION ')' INSTRUCTION ELSE INSTRUCTION"""
        if len(p) == 8:
            p[0] = ast.IfElseNode(p[3], p[5], p[7])
        elif len(p) == 6:
            p[0] = ast.IfNode(p[3], p[5])
        if self.debug:
            print('p_if_statement: {}'.format(p[0]))

    def p_while_statement(self, p):
        """WHILE_STATEMENT : WHILE '(' CONDITION ')' INSTRUCTION"""
        p[0] = ast.WhileNode(p[3], p[5])
        if self.debug:
            print('p_while_statement: {}'.format(p[0]))

    def p_for_statement(self, p):
        """FOR_STATEMENT : FOR CONST_ID '=' RANGE INSTRUCTION"""
        p[0] = ast.ForNode(p[2], p[4], p[5])
        if self.debug:
            print('p_for_statement: {}'.format(p[0]))

    def p_range(self, p):
        """RANGE : EXPRESSION ':' EXPRESSION
                 | EXPRESSION ':' EXPRESSION ':' EXPRESSION"""
        if len(p) == 4:
            p[0] = ast.RangeNode(p[1], p[3])
        elif len(p) == 6:
            p[0] = ast.RangeNode(p[1], p[3], p[5])
        if self.debug:
            print('p_range: {}'.format(p[0]))
