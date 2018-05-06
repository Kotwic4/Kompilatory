class Node(object):
    pass


class ConstValueNode(Node):
    def __init__(self, value):
        self.value = value


class ProgramNode(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class BodyNode(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class RangeNode(Node):
    def __init__(self, start, end, jump=ConstValueNode(1)):
        self.start = start
        self.end = end
        self.jump = jump

    def __repr__(self):
        return '[ {} : {} : {} ]'.format(self.start, self.end, self.jump)


class ForNode(Node):
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class IfNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'IF {} THEN {}'.format(self.condition, self.body)


class IfElseNode(Node):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return 'IF {} THEN {} ELSE {}'.format(self.condition, self.body, self.else_body)


class BreakNode(Node):
    def __repr__(self):
        return 'BREAK'


class ContinueNode(Node):
    def __repr__(self):
        return 'CONTINUE'


class ReturnNode(Node):
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class PrintNode(Node):
    def __init__(self, printable):
        self.printable = printable

    def __repr__(self):
        return 'PRINT( {} )'.format(self.printable)


class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class AssignmentNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class AssignToNode(Node):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '{}'.format(self.id)


class AccessNode(Node):
    def __init__(self, id, specifier):
        self.id = id
        self.specifier = specifier

    def __repr__(self):
        return '{}[ {} ]'.format(self.id, self.specifier)


class ExpressionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class TranspositionNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "( {}' )".format(self.value)


class NegationNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '( -{} )'.format(self.value)


class FunctionNode(Node):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return '{}( {} )'.format(self.name, self.argument)


class MatrixNode(Node):
    def __init__(self, rows):
        self.rows = rows


class VectorNode(Node):
    def __init__(self, values):
        self.values = values

    def append(self, value):
        self.values.append(value)


class ErrorNode(Node):
    def __init__(self):
        pass
