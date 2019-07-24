import textwrap

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
        return '''IntegerLiteral: {}'''.format(repr(self.integer))

class UnaryOperator:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return '''UnaryOperator: {}
Expression: {}'''.format(self.operator, repr(self.expression))

class Expression:
    def __init__(self, terms, operations):
        self.terms = terms
        self.operations = operations

    def __repr__(self):
        s = "Expression:\n"

        for term, operation in zip(self.terms, self.operations):
            s += repr(term)
            if operation:
                s += "Operation: {}".format(operation)

        return s

class Term:
    def __init__(self, factors, operations):
        self.factors = factors
        self.operations = operations

    def __repr__(self):
        s = "Term:\n"

        for factor, operation in zip(self.factors, self.operations):
            s += repr(factor)
            if operation:
                s += "Operation: {}".format(operation)

        return s
