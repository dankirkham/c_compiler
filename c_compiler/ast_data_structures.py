import textwrap
from itertools import zip_longest

indent = lambda s: textwrap.indent(s, '\t')

class Program:
    def __init__(self, function_declaration):
        self.function_declaration = function_declaration

    def __repr__(self):
        return '''Program:
{}'''.format(indent(repr(self.function_declaration)))

class Function:
    def __init__(self, name, statements, symbol_map):
        self.name = name
        self.statements = statements
        self.symbol_map = symbol_map

    def __repr__(self):
        s = "Function '{}':\n".format(self.name)

        for statement in self.statements:
            s += indent(repr(statement))

        return s

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return '''ReturnStatement:
{}'''.format(indent(repr(self.expression)))

class DeclareStatement:
    def __init__(self, expression, identifier):
        self.expression = expression
        self.identifier = identifier

    def __repr__(self):
        return '''DeclareStatement:
\tIdentifier: {}
Expression: {}'''.format(self.identifier, indent(repr(self.expression)))

class Variable:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return '''Variable: {}\n'''.format(repr(self.identifier))

class Constant:
    def __init__(self, integer):
        self.integer = integer

    def __repr__(self):
        return '''IntegerLiteral: {}\n'''.format(repr(self.integer))

class UnaryOperator:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return '''UnaryOperator: {}
Expression: {}'''.format(self.operator, repr(self.expression))

class BinaryOperator:
    def __init__(self, operation, expression1, expression2):
        self.operation = operation
        self.expression1 = expression1
        self.expression2 = expression2

    def __repr__(self):
        s = "BinaryOperator:\n"

        s += repr(self.expression1)
        s += "Operation: " + self.operation
        s += repr(self.expression2)

        return s
