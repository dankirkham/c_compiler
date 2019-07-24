from c_compiler.lexer import Token
from c_compiler import ast_data_structures
from c_compiler.parser import parse
import unittest

class TestParser(unittest.TestCase):
    def test_parser(self):
        tokens = [
            Token(type='int_keyword', value='int', line=1, col=1),
            Token(type='identifer', value='main', line=1, col=5),
            Token(type='open_parenthesis', value='(', line=1, col=9),
            Token(type='close_parenthesis', value=')', line=1, col=10),
            Token(type='open_brace', value='{', line=1, col=12),
            Token(type='return_keyword', value='return', line=2, col=5),
            Token(type='integer_literal', value='2', line=2, col=12),
            Token(type='semicolon', value=';', line=2, col=13),
            Token(type='close_brace', value='}', line=3, col=1)
        ]

        ast = parse(tokens)

        # Program
        self.assertTrue(isinstance(ast, ast_data_structures.Program))

        # Function
        function = ast.function_declaration
        self.assertTrue(isinstance(function, ast_data_structures.Function))
        self.assertEqual(function.name, 'main')

        # Statement
        statement = function.statement
        self.assertTrue(isinstance(statement, ast_data_structures.ReturnStatement))

        # Expression
        expression = statement.expression
        self.assertTrue(isinstance(expression, ast_data_structures.Expression))

        # Term
        term = expression.terms[0]
        self.assertTrue(isinstance(term, ast_data_structures.Term))

        # Factor
        factor = term.factors[0]
        self.assertTrue(isinstance(factor, ast_data_structures.Constant))
        self.assertEqual(factor.integer, 2)
