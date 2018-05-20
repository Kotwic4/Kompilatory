class Type:
    pass


class FloatType(Type):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self) -> str:
        return "Float[{0}]".format(self.value)


class IntType(Type):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self) -> str:
        return "Int[{0}]".format(self.value)


class StringType(Type):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self) -> str:
        return "String[{0}]".format(self.value)


class VectorType(Type):
    def __init__(self, value=None, size=0):
        if value is not None:
            size = len(value)
        self.size = size
        self.value = value

    def __repr__(self) -> str:
        return "Vector[{0}]".format(self.size)


class MatrixType(Type):
    def __init__(self, value=None, width=0, height=0):
        if value is not None:
            height = len(value)
            width = value[0].size
        self.value = value
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return "Matrix[{0},{1}]".format(self.width, self.height)


class UnknownType(Type):
    def __init__(self):
        self.value = None

    def __repr__(self) -> str:
        return "UnknownType"


class VoidType(Type):
    def __repr__(self):
        return "Void"


class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        return self.symbols[name]


class ScopeTable:

    def __init__(self):
        self.scopes = {0: SymbolTable('root', 0)}
        self.current_scope_number = 0

    def put(self, name, symbol, scope_number=None):
        if scope_number is None:
            scope_number = self.current_scope_number
        return self.scopes[scope_number].put(name, symbol)

    def get(self, name, scope_number=None):
        if scope_number is None:
            scope_number = self.current_scope_number
        return self.scopes[scope_number].get(name)

    def find_variable_scope(self, name):
        for scope_number in range(self.current_scope_number, -1, -1):
            scope = self.scopes[scope_number]
            if name in scope.symbols:
                return scope.number
        return None

    def find_scope(self, name):
        for scope_number in range(self.current_scope_number, -1, -1):
            scope = self.scopes[scope_number]
            if scope.name == name:
                return scope.number
        return None

    def pushScope(self, name):
        self.current_scope_number += 1
        self.scopes[self.current_scope_number] = SymbolTable(name, self.current_scope_number)
        return self.current_scope_number

    def popScope(self):
        self.scopes.pop(self.current_scope_number)
        self.current_scope_number -= 1
        return self.current_scope_number
