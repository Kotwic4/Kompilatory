import ast
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)

ExpressionDict = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '.+': lambda x, y: [[x[i][j] + y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    '.-': lambda x, y: [[x[i][j] - y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    '.*': lambda x, y: [[x[i][j] * y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    './': lambda x, y: [[x[i][j] / y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
}

AssignmentDict = {
    '=': lambda x, y: y,
    '+=': lambda x, y: x + y,
    '-=': lambda x, y: x - y,
    '*=': lambda x, y: x * y,
    '/=': lambda x, y: x / y,
}

FunctionDict = {
    'zeros': lambda x: [[0 for _ in range(x)] for _ in range(x)],
    'ones': lambda x: [[1 for _ in range(x)] for _ in range(x)],
    'eye': lambda x: [[1 if j == i else 0 for j in range(x)] for i in range(x)],
}

ConditionDict = {
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
}


class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(ast.ConstValueNode)
    def visit(self, node):
        return node.value

    @when(ast.IdNode)
    def visit(self, node):
        return self.memory_stack.get(node.value)

    @when(ast.ProgramNode)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(ast.BlockNode)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(ast.RangeNode)
    def visit(self, node):
        return range(node.start.accept(self), node.end.accept(self) + 1, node.jump.accept(self))

    @when(ast.ForNode)
    def visit(self, node):
        r = None
        self.memory_stack.push()
        for i in node.range.accept(self):
            self.memory_stack.insert(node.id.value, i)
            try:
                r = node.body.accept(self)
            except ContinueException as e:
                continue
            except BreakException as e:
                break
            except ReturnValueException as e:
                return e.value
        self.memory_stack.pop()
        return r

    @when(ast.WhileNode)
    def visit(self, node):
        r = None
        self.memory_stack.push()
        while node.condition.accept(self):
            try:
                r = node.body.accept(self)
            except ContinueException as e:
                continue
            except BreakException as e:
                break
            except ReturnValueException as e:
                return e.value
        self.memory_stack.pop()
        return r

    @when(ast.IfNode)
    def visit(self, node):
        self.memory_stack.push()
        if node.condition.accept(self):
            node.body.accept(self)
        self.memory_stack.pop()

    @when(ast.IfElseNode)
    def visit(self, node):
        self.memory_stack.push()
        if node.condition.accept(self):
            node.body.accept(self)
        else:
            node.else_body.accept(self)
        self.memory_stack.pop()

    @when(ast.BreakNode)
    def visit(self, node):
        raise BreakException()

    @when(ast.ContinueNode)
    def visit(self, node):
        raise ContinueException()

    @when(ast.ReturnNode)
    def visit(self, node):
        raise ReturnValueException(node.result.accept(self))

    @when(ast.PrintNode)
    def visit(self, node):
        for value in node.printable.accept(self):
            print(value, end=' ')
        print('\b')

    @when(ast.ConditionNode)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ConditionDict[node.operator](r1, r2)

    @when(ast.AssignmentNode)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        self.memory_stack.insert(node.left.id.value, AssignmentDict[node.operator](r1, r2))

    @when(ast.AssignToNode)
    def visit(self, node):
        return self.memory_stack.get(node.id.value)

    @when(ast.AccessNode)
    def visit(self, node):
        m = node.id.accept(self)
        for value in node.specifier.accept(self):
            m = m[value]
        return m

    @when(ast.ExpressionNode)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ExpressionDict[node.operator](r1, r2)

    @when(ast.TranspositionNode)
    def visit(self, node):
        return [list(x) for x in zip(*node.value.accept(self))]

    @when(ast.NegationNode)
    def visit(self, node):
        return -node.value.accept(self)

    @when(ast.FunctionNode)
    def visit(self, node):
        return FunctionDict[node.name](node.argument.accept(self))

    @when(ast.MatrixNode)
    def visit(self, node):
        l = []
        for row in node.rows:
            l.append(row.accept(self))
        return l

    @when(ast.SequenceNode)
    def visit(self, node):
        l = []
        for value in node.values:
            l.append(value.accept(self))
        return l

    @when(ast.ErrorNode)
    def visit(self, node):
        pass
