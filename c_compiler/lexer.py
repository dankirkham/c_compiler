import re
import argparse
from pprint import pprint

class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __eq__(self, other):
        return (
            self.type == other.type and
            self.value == other.value and
            self.line == other.line and
            self.col == other.col
        )

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return "Token {}: value '{}'; pos: line {}, column {}".format(self.type, self.value, self.line, self.col)

TOKENS = [
    {
        'type': 'open_brace',
        'regex': re.compile('{')
    },
    {
        'type': 'close_brace',
        'regex': re.compile('}')
    },
    {
        'type': 'open_parenthesis',
        'regex': re.compile('\(')
    },
    {
        'type': 'close_parenthesis',
        'regex': re.compile('\)')
    },
    {
        'type': 'semicolon',
        'regex': re.compile(';')
    },
    {
        'type': 'int_keyword',
        'regex': re.compile('int')
    },
    {
        'type': 'return_keyword',
        'regex': re.compile('return')
    },
    {
        'type': 'identifer',
        'regex': re.compile('[a-zA-Z]\w*')
    },
    {
        'type': 'integer_literal',
        'regex': re.compile('[0-9]+')
    },
    {
        'type': 'negation',
        'regex': re.compile('\-')
    },
    {
        'type': 'bitwise_complement',
        'regex': re.compile('~')
    },
    {
        'type': 'logical_negation',
        'regex': re.compile('!')
    },
    {
        'type': 'addition_operator',
        'regex': re.compile('\+')
    },
    {
        'type': 'multiplication_operator',
        'regex': re.compile('\*')
    },
    {
        'type': 'division_operator',
        'regex': re.compile('\/')
    },
]

def lex(string):
    tokens = []
    line_number = 1

    for line in string.splitlines():
        col = 1

        while True:
            leftmost_token = None
            for TOKEN in TOKENS:
                m = TOKEN['regex'].search(line)

                if not m:
                    continue

                token = Token(type=TOKEN['type'], value=m.group(0), line=line_number, col=m.span()[0] + col)

                if not leftmost_token or leftmost_token.col > token.col:
                    leftmost_token = token

            if not leftmost_token:
                line_number += 1
                break

            tokens.append(leftmost_token)
            line = line[leftmost_token.col - col + len(leftmost_token):]
            col += leftmost_token.col - col + len(leftmost_token)

    return tokens

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to be lexed')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        data = f.read()

    pprint(lex(data))

if __name__ == "__main__":
    main()
