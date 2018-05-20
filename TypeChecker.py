import ast
from ScopeTable import ScopeTable, FloatType, StringType, IntType, VectorType, UnknownType, MatrixType, VoidType


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, ast.Node):
                            self.visit(item)
                elif isinstance(child, ast.Node):
                    self.visit(child)


def checkType(value, typ):
    return type(value) is typ


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.errors = False
        self.scope_table = ScopeTable()

    @staticmethod
    def checkMatrixExprType(type1, type2, lineno):
        if checkType(type1, VectorType) and checkType(type2, VectorType):
            if type1.size is None or type2.size is None:
                return VectorType()
            elif type1.size != type2.size:
                print("Vectors {1} and {2} don't have the same sizes at line {0}".format(lineno, type1, type2))
                return UnknownType()
            else:
                return VectorType(size=type1.size)
        elif checkType(type1, MatrixType) and checkType(type2, MatrixType):
            if type1.width is None or type2.width is None or type1.height is None or type2.height is None:
                return MatrixType()
            elif type1.width != type2.width or type1.height != type2.height:
                print("Matrix {1} and {2} don't have the same sizes at line {0}".format(lineno, type1, type2))
                return UnknownType()
            else:
                return MatrixType(width=type1.width, height=type1.height)
        elif checkType(type1, VectorType) and (checkType(type2, FloatType) or checkType(type2, IntType)):
            if type1.size is not None:
                return VectorType(size=type1.size)
            else:
                return VectorType()
        elif checkType(type1, MatrixType) and (checkType(type2, FloatType) or checkType(type2, IntType)):
            if type1.width is None or type2.width is None:
                return MatrixType()
            else:
                return MatrixType(width=type1.width, height=type1.height)
        return None

    @staticmethod
    def checkCompExprType(type1, type2, lineno):
        if checkType(type1, VectorType) and checkType(type2, VectorType):
            if type1.size is not None and type2.size is not None and type1.size != type2.size:
                print("Vectors {1} and {2} don't have the same sizes at line {0}".format(lineno, type1, type2))
                return IntType()
            else:
                return IntType()
        elif checkType(type1, MatrixType) and checkType(type2, MatrixType):
            if type1.width is not None and type2.width is not None and type1.height is not None and type2.height is not None and (
                    type1.width != type2.width or type1.height != type2.height):
                print("Matrix {1} and {2} don't have the same sizes at line {0}".format(lineno, type1, type2))
                return IntType()
            else:
                return IntType()
        elif (checkType(type1, FloatType) or checkType(type1, IntType)) and (
                checkType(type2, FloatType) or checkType(type2, IntType)):
            return IntType()
        elif checkType(type1, StringType) and checkType(type2, StringType):
            return IntType()
        return None

    @staticmethod
    def checkBasicType(type1, type2, op):
        if op == '+':
            if checkType(type1, IntType) and checkType(type2, IntType):
                if type1.value is not None and type2.value is not None:
                    return IntType(type1.value + type2.value)
                else:
                    return IntType()
            elif (checkType(type1, FloatType) or checkType(type1, IntType)) and (
                    checkType(type2, FloatType) or checkType(type2, IntType)):
                if type1.value is not None and type2.value is not None:
                    return FloatType(type1.value + type2.value)
                else:
                    return FloatType()
            elif checkType(type1, StringType) and checkType(type2, StringType):
                if type1.value is not None and type2.value is not None:
                    return StringType(type1.value + type2.value)
                else:
                    return StringType()
        elif op == '-':
            if checkType(type1, IntType) and checkType(type2, IntType):
                if type1.value is not None and type2.value is not None:
                    return IntType(type1.value - type2.value)
                else:
                    return IntType()
            elif (checkType(type1, FloatType) or checkType(type1, IntType)) and (
                    checkType(type2, FloatType) or checkType(type2, IntType)):
                if type1.value is not None and type2.value is not None:
                    return FloatType(type1.value - type2.value)
                else:
                    return FloatType()

        elif op == '/':
            if checkType(type1, IntType) and checkType(type2, IntType):
                if type1.value is not None and type2.value is not None:
                    return IntType(type1.value / type2.value)
                else:
                    return IntType()
            elif (checkType(type1, FloatType) or checkType(type1, IntType)) and (
                    checkType(type2, FloatType) or checkType(type2, IntType)):
                if type1.value is not None and type2.value is not None:
                    return FloatType(type1.value / type2.value)
                else:
                    return FloatType()

        elif op == '*':
            if checkType(type1, IntType) and checkType(type2, IntType):
                if type1.value is not None and type2.value is not None:
                    return IntType(type1.value * type2.value)
                else:
                    return IntType()
            elif (checkType(type1, FloatType) or checkType(type1, IntType)) and (
                    checkType(type2, FloatType) or checkType(type2, IntType)):
                if type1.value is not None and type2.value is not None:
                    return FloatType(type1.value * type2.value)
                else:
                    return FloatType()
            elif checkType(type1, StringType) and checkType(type2, StringType):
                if type1.value is not None and type2.value is not None:
                    return StringType(type1.value * type2.value)
                else:
                    return StringType()
        return None

    @staticmethod
    def checkExprType(type1, type2, op, lineno):
        result = None
        if checkType(type1, UnknownType) or checkType(type2, UnknownType):
            result = UnknownType()
        elif op == '.+' or op == '.-' or op == '.*' or op == './':
            result = TypeChecker.checkMatrixExprType(type1, type2, lineno)
        elif op == "==" or op == "!=" or op == ">=" or op == "<=" or op == ">" or op == "<":
            result = TypeChecker.checkCompExprType(type1, type2, lineno)
        else:
            result = TypeChecker.checkBasicType(type1, type2, op)
        if result is None:
            print("Types {1} and {2} cannot perform operation {3} at line {0}".format(lineno, type1, type2, op))
            return UnknownType()
        else:
            return result

    def putVariable(self, id, symbol):
        name = id.value
        scope = self.scope_table.find_variable_scope(name)
        if scope is None:
            self.scope_table.put(name, symbol)
            return symbol
        else:
            self.scope_table.put(name, symbol, scope)
        return symbol

    def visit_ConstValueNode(self, node):
        if checkType(node.value, float):
            return FloatType(node.value)
        if checkType(node.value, str):
            return StringType(node.value)
        if checkType(node.value, int):
            return IntType(node.value)
        return UnknownType()

    def visit_IdNode(self, node):
        scope = self.scope_table.find_variable_scope(node.value)
        if scope is None:
            print("Variable {1} not initialize at line {0}".format(node.lineno, node.value))
            return UnknownType()
        else:
            return self.scope_table.get(node.value, scope)

    def visit_ProgramNode(self, node):
        self.scope_table.pushScope("program")
        for instruction in node.instructions:
            self.visit(instruction)
        self.scope_table.popScope()

    def visit_BlockNode(self, node):
        self.scope_table.pushScope("block")
        for instruction in node.instructions:
            self.visit(instruction)
        self.scope_table.popScope()

    def visit_RangeNode(self, node):
        type1 = self.visit(node.start)
        type2 = self.visit(node.jump)
        self.visit(node.end)
        return self.checkExprType(type1, type2, '+', node.lineno)

    def visit_ForNode(self, node):
        self.scope_table.pushScope("loop")
        typ = self.visit(node.range)
        self.putVariable(node.id, typ)
        self.visit(node.body)
        self.scope_table.popScope()

    def visit_WhileNode(self, node):
        self.scope_table.pushScope("loop")
        self.visit(node.condition)
        self.visit(node.body)
        self.scope_table.popScope()
        return VoidType()

    def visit_IfNode(self, node):
        self.scope_table.pushScope("if")
        self.visit(node.condition)
        self.visit(node.body)
        self.scope_table.popScope()
        return VoidType()

    def visit_IfElseNode(self, node):
        self.scope_table.pushScope("if")
        self.visit(node.condition)
        self.visit(node.body)
        self.scope_table.popScope()
        self.scope_table.pushScope("if")
        self.visit(node.else_body)
        self.scope_table.popScope()
        return VoidType()

    def visit_BreakNode(self, node):
        if self.scope_table.find_scope("loop") is None:
            print("Break outside of loop at line {0}".format(node.lineno))
        return VoidType()

    def visit_ContinueNode(self, node):
        if self.scope_table.find_scope("loop") is None:
            print("Continue outside of loop at line {0}".format(node.lineno))
        return VoidType()

    def visit_ReturnNode(self, node):
        return self.visit(node.result)

    def visit_PrintNode(self, node):
        self.visit(node.printable)
        return VoidType()

    def visit_ConditionNode(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        return self.checkExprType(type1, type2, node.operator, node.lineno)

    def visit_AssignmentNode(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        val = None
        if node.operator == "=":
            val = type2
        else:
            if type1 is None:
                print("Left side is not initialize at line {0}".format(node.lineno))
                val = UnknownType()
            else:
                val = self.checkExprType(type1, type2, node.operator[0], node.lineno)
        if checkType(node.left.id, ast.AccessNode):
            return val
        else:
            return self.putVariable(node.left.id, val)

    def visit_AssignToNode(self, node):
        if checkType(node.id, ast.AccessNode):
            return self.visit(node.id)
        else:
            name = node.id.value
            scope = self.scope_table.find_scope(name)
            if scope is None:
                return None
            else:
                return self.scope_table.get(name, scope)

    def visit_AccessNode(self, node):
        typ = self.visit(node.id)
        seq = self.visit(node.specifier)
        result = None
        if checkType(typ, UnknownType):
            result = None
        elif checkType(typ, VectorType):
            if seq.size != 1:
                print("Expected Vector[1] type as index got {1} at line {0}".format(node.lineno, seq))
                result = None
            else:
                i = seq.value[0].value
                if not checkType(i, int):
                    result = None
                elif i >= typ.size:
                    print("Index out of boundaries at line {0}".format(node.lineno, seq.value[0]))
                    result = None
                elif i < 0:
                    print("Index must be positive at line {0}".format(node.lineno, seq.value[0]))
                    result = None
                elif typ.value is not None:
                    result = typ.value[i]
                else:
                    result = None
        elif checkType(typ, MatrixType):
            if seq.size != 2:
                print("Expected Vector[2] type as index got {1} at line {0}".format(node.lineno, seq))
                result = None
            else:
                i = seq.value[0].value
                j = seq.value[1].value
                if not checkType(j, int) or not checkType(j, int):
                    result = None
                elif i >= typ.width or j >= typ.height:
                    print("Index [{1},{2}] out of  boundaries at line {0}".format(node.lineno, seq.value[0],
                                                                                  seq.value[1]))
                    result = None
                elif i < 0 or j < 0:
                    print(
                        "Index [{1},{2}] must be positive at line {0}".format(node.lineno, seq.value[0], seq.value[1]))
                    result = None
                elif typ.value is not None:
                    result = typ.value[i].value[j]
                else:
                    result = None
        else:
            print("Expected access type got {1} at line {0}".format(node.lineno, typ))
        if result is None:
            return UnknownType()
        else:
            return result

    def visit_ExpressionNode(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        return self.checkExprType(type1, type2, node.operator, node.lineno)

    def visit_TranspositionNode(self, node):
        typ = self.visit(node.value)
        if checkType(typ, UnknownType):
            return UnknownType()
        elif checkType(typ, MatrixType):
            return MatrixType(width=typ.height, height=typ.width)
        else:
            print("Expected with wrong parameter, wanted type Matrix, got {1} at line {0}"
                  .format(node.lineno, typ))
            return UnknownType()

    def visit_NegationNode(self, node):
        typ = self.visit(node.value)
        if checkType(typ, IntType) or checkType(typ, FloatType):
            typ.value = -typ.value
        elif checkType(typ, StringType):
            print("Cannot perform negation on String at line {0}"
                  .format(node.lineno, typ))
            return UnknownType()
        else:
            typ.value = UnknownType()
        return typ

    def visit_FunctionNode(self, node):
        typ = self.visit(node.argument)
        if checkType(typ, IntType):
            value = typ.value
            if value is None or value >= 0:
                return MatrixType(width=typ.value, height=typ.value)
            else:
                print("Function initialize with wrong parameter, wanted type positive number, got {1} at line {0}"
                      .format(node.lineno, value))
        if checkType(typ, UnknownType):
            return MatrixType()
        print("Function initialize with wrong parameter, wanted type Int, got {1} at line {0}"
              .format(node.lineno, typ))
        return UnknownType()

    def visit_MatrixNode(self, node):
        values = []
        for val in node.rows:
            values.append(self.visit(val))
        size = values[0].size
        for val in values:
            if size != val.size:
                print("Matrix initialize with incompatible vectors at line {0}".format(node.lineno))
                return MatrixType()
        if len(values) == 1:
            return values[0]
        else:
            return MatrixType(values)

    def visit_SequenceNode(self, node):
        values = []
        for val in node.values:
            values.append(self.visit(val))
        return VectorType(values)

    def visit_ErrorNode(self, node):
        pass
