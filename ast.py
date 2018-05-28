class Node:
    def accept(self, visitor):
        return visitor.visit(self)


class ConstValueNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class IdNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class ProgramNode(Node):
    def __init__(self, instructions, lineno):
        self.instructions = instructions
        self.lineno = lineno


class BlockNode(Node):
    def __init__(self, instructions, lineno):
        self.instructions = instructions
        self.lineno = lineno


class RangeNode(Node):
    def __init__(self, start, end, lineno, jump=None):
        if jump is None:
            jump = ConstValueNode(1, lineno)
        self.start = start
        self.end = end
        self.jump = jump
        self.lineno = lineno

    def __repr__(self):
        return '[ {} : {} : {} ]'.format(self.start, self.end, self.jump)


class ForNode(Node):
    def __init__(self, id, range, body, lineno):
        self.id = id
        self.range = range
        self.body = body
        self.lineno = lineno

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class WhileNode(Node):
    def __init__(self, condition, body, lineno):
        self.condition = condition
        self.body = body
        self.lineno = lineno

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class IfNode(Node):
    def __init__(self, condition, body, lineno):
        self.condition = condition
        self.body = body
        self.lineno = lineno

    def __repr__(self):
        return 'IF {} THEN {}'.format(self.condition, self.body)


class IfElseNode(Node):
    def __init__(self, condition, body, else_body, lineno):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.lineno = lineno

    def __repr__(self):
        return 'IF {} THEN {} ELSE {}'.format(self.condition, self.body, self.else_body)


class BreakNode(Node):
    def __init__(self, lineno):
        self.lineno = lineno

    def __repr__(self):
        return 'BREAK'


class ContinueNode(Node):
    def __init__(self, lineno):
        self.lineno = lineno

    def __repr__(self):
        return 'CONTINUE'


class ReturnNode(Node):
    def __init__(self, result, lineno):
        self.result = result
        self.lineno = lineno

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class PrintNode(Node):
    def __init__(self, printable, lineno):
        self.printable = printable
        self.lineno = lineno

    def __repr__(self):
        return 'PRINT( {} )'.format(self.printable)


class ConditionNode(Node):
    def __init__(self, left, operator, right, lineno):
        self.left = left
        self.operator = operator
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class AssignmentNode(Node):
    def __init__(self, left, operator, right, lineno):
        self.left = left
        self.operator = operator
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class AssignToNode(Node):
    def __init__(self, id, lineno):
        self.id = id
        self.lineno = lineno

    def __repr__(self):
        return '{}'.format(self.id)


class AccessNode(Node):
    def __init__(self, id, specifier, lineno):
        self.id = id
        self.specifier = specifier
        self.lineno = lineno

    def __repr__(self):
        return '{}[ {} ]'.format(self.id, self.specifier)


class ExpressionNode(Node):
    def __init__(self, left, operator, right, lineno):
        self.left = left
        self.operator = operator
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class TranspositionNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "( {}' )".format(self.value)


class NegationNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return '( -{} )'.format(self.value)


class FunctionNode(Node):
    def __init__(self, name, argument, lineno):
        self.name = name
        self.argument = argument
        self.lineno = lineno

    def __repr__(self):
        return '{}( {} )'.format(self.name, self.argument)


class MatrixNode(Node):
    def __init__(self, rows, lineno):
        self.rows = rows
        self.lineno = lineno


class SequenceNode(Node):
    def __init__(self, values, lineno):
        self.values = values
        self.lineno = lineno

    def append(self, value):
        self.values.append(value)


class ErrorNode(Node):
    def __init__(self):
        pass
