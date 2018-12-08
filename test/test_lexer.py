from c_compiler.lexer import lex, Token
import unittest
from itertools import zip_longest

class TestLexer(unittest.TestCase):
    def test_lexer(self):
        source = '''int main() {
    return 2;
}
'''
        tokens = lex(source)

        expected_tokens = [
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

        for actual, expected in zip_longest(tokens, expected_tokens):
            self.assertEqual(actual, expected)
