from __future__ import print_function
import ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_with_ident(value, indent):
     print("| "*indent + str(value))


class TreePrinter:

    @addToClass(ast.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(ast.ConstValueNode)
    def printTree(self, indent=0):
        print_with_ident(self.value, indent)

    @addToClass(ast.ProgramNode)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(ast.BodyNode)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(ast.RangeNode)
    def printTree(self, indent=0):
        print_with_ident("Range", indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
        self.jump.printTree(indent + 1)

    @addToClass(ast.ForNode)
    def printTree(self, indent=0):
        print_with_ident("For", indent)
        self.id.printTree(indent+1)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(ast.WhileNode)
    def printTree(self, indent=0):
        print_with_ident("While", indent)
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(ast.IfNode)
    def printTree(self, indent=0):
        print_with_ident("If", indent)
        self.condition.printTree(indent + 1)
        print_with_ident("Then", indent)
        self.body.printTree(indent + 1)

    @addToClass(ast.IfElseNode)
    def printTree(self, indent=0):
        print_with_ident("If", indent)
        self.condition.printTree(indent + 1)
        print_with_ident("Then", indent)
        self.body.printTree(indent + 1)
        print_with_ident("Else", indent)
        self.else_body.printTree(indent + 1)

    @addToClass(ast.BreakNode)
    def printTree(self, indent=0):
        print_with_ident("Break", indent)

    @addToClass(ast.ContinueNode)
    def printTree(self, indent=0):
        print_with_ident("Continue", indent)

    @addToClass(ast.ReturnNode)
    def printTree(self, indent=0):
        print_with_ident("Return", indent)
        self.result.printTree(indent+1)

    @addToClass(ast.PrintNode)
    def printTree(self, indent=0):
        print_with_ident("Print", indent)
        self.printable.printTree(indent+1)

    @addToClass(ast.ConditionNode)
    def printTree(self, indent=0):
        print_with_ident(self.operator, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(ast.AssignmentNode)
    def printTree(self, indent=0):
        print_with_ident(self.operator, indent)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(ast.AssignToNode)
    def printTree(self, indent=0):
        self.id.printTree(indent)

    @addToClass(ast.AccessNode)
    def printTree(self, indent=0):
        print_with_ident("Access", indent)
        self.id.printTree(indent + 1)
        self.specifier.printTree(indent + 1)

    @addToClass(ast.ExpressionNode)
    def printTree(self, indent=0):
        print_with_ident(self.operator, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(ast.TranspositionNode)
    def printTree(self, indent=0):
        print_with_ident("Transposition", indent)
        self.value.printTree(indent + 1)

    @addToClass(ast.NegationNode)
    def printTree(self, indent=0):
        print_with_ident("Negation", indent)
        self.value.printTree(indent + 1)

    @addToClass(ast.FunctionNode)
    def printTree(self, indent=0):
        print_with_ident(self.name, indent)
        self.argument.printTree(indent+1)

    @addToClass(ast.MatrixNode)
    def printTree(self, indent=0):
        print_with_ident("Matrix", indent)
        for row in self.rows:
            row.printTree(indent+1)

    @addToClass(ast.SequenceNode)
    def printTree(self, indent=0):
        print_with_ident("Sequence", indent)
        for value in self.values:
            value.printTree(indent + 1)


