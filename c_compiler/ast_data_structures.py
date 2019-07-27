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
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement

    def __repr__(self):
        return '''Function "{}":
{}'''.format(self.name, indent(repr(self.statement)))

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return '''ReturnStatement:
{}'''.format(indent(repr(self.expression)))

class Constant:
    def __init__(self, integer):
        self.integer = integer

    def __repr__(self):
        return '''IntegerLiteral: {}\n'''.format(repr(self.integer))

class UnaryOperator:
    def __init__(self, operator, factor):
        self.operator = operator
        self.factor = factor

    def __repr__(self):
        return '''UnaryOperator: {}
Factor: {}'''.format(self.operator, repr(self.factor))

class Expression:
    def __init__(self, logical_and_expressions, operations):
        self.logical_and_expressions = logical_and_expressions
        self.operations = operations

    def __repr__(self):
        s = "Expression:\n"

        for logical_and_expression, operation in zip_longest(self.logical_and_expressions, self.operations):
            s += repr(logical_and_expression)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s

class LogicalAndExpression:
    def __init__(self, equality_expressions, operations):
        self.equality_expressions = equality_expressions
        self.operations = operations

    def __repr__(self):
        s = "LogicalAndExpression:\n"

        for equality_expression, operation in zip_longest(self.equality_expressions, self.operations):
            s += repr(equality_expression)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s

class EqualityExpression:
    def __init__(self, relational_expressions, operations):
        self.relational_expressions = relational_expressions
        self.operations = operations

    def __repr__(self):
        s = "EqualityExpression:\n"

        for relational_expression, operation in zip_longest(self.relational_expressions, self.operations):
            s += repr(relational_expression)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s

class RelationalExpression:
    def __init__(self, additive_expressions, operations):
        self.additive_expressions = additive_expressions
        self.operations = operations

    def __repr__(self):
        s = "RelationalExpression:\n"

        for additive_expression, operation in zip_longest(self.additive_expressions, self.operations):
            s += repr(additive_expression)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s

class AdditiveExpression:
    def __init__(self, terms, operations):
        self.terms = terms
        self.operations = operations

    def __repr__(self):
        s = "AdditiveExpression:\n"

        for term, operation in zip_longest(self.terms, self.operations):
            s += repr(term)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s

class Term:
    def __init__(self, factors, operations):
        self.factors = factors
        self.operations = operations

    def __repr__(self):
        s = "Term:\n"

        for factor, operation in zip_longest(self.factors, self.operations):
            s += repr(factor)
            if operation:
                s += "Operation: {}\n".format(operation)

        return s
