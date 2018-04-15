class Range:
    def __init__(self, start, end, jump=1):
        self.start = start
        self.end = end
        self.jump = jump

    def __repr__(self):
        return '[ {} : {} : {} ]'.format(self.start, self.end, self.jump)


class For:
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class If:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'IF {} THEN {}'.format(self.condition, self.body)


class IfElse:
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return 'IF {} THEN {} ELSE {}'.format(self.condition, self.body, self.else_body)


class Break:
    def __repr__(self):
        return 'BREAK'


class Continue:
    def __repr__(self):
        return 'CONTINUE'


class Return:
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print:
    def __init__(self, printable):
        self.printable = printable

    def __repr__(self):
        return 'PRINT( {} )'.format(self.printable)


class Condition:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class Assignment:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class AssignTo:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '{}'.format(self.id)


class Access:
    def __init__(self, id, specifier):
        self.id = id
        self.specifier = specifier

    def __repr__(self):
        return '{}[ {} ]'.format(self.id, self.specifier)


class Expression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '( {} {} {} )'.format(self.left, self.operator, self.right)


class Transposition:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "( {}' )".format(self.value)


class Negation:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '( -{} )'.format(self.value)


class Function:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return '{}( {} )'.format(self.name, self.argument)