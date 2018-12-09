from c_compiler import ast_data_structures

class PeekableIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self._position = 0

    def __next__(self):
        if self._position == len(self):
            raise StopIteration
        else:
            self._position += 1
            return self.iterable[self._position - 1]

    def __len__(self):
        return len(self.iterable)

    def peek(self):
        if self._position == len(self):
            raise IndexError('Tried to peek an exhausted iterator.')
        else:
            return self.iterable[self._position]

class ParserError(Exception):
    pass

def _expect(token, types):
    if not isinstance(types, list):
        types = [types]

    if token.type not in types:
        raise ParserError("Expected {} at {}".format(types, token))

def parse_expression(tokens):
    token = next(tokens)

    _expect(token, 'integer_literal')

    return ast_data_structures.Constant(int(token.value))

def parse_statement(tokens):
    token = next(tokens)
    _expect(token, 'return_keyword')

    expression = parse_expression(tokens)

    token = next(tokens)
    _expect(token, 'semicolon')

    return ast_data_structures.ReturnStatement(expression)

def parse_function(tokens):
    token = next(tokens)
    _expect(token, 'int_keyword')

    token = next(tokens)
    _expect(token, 'identifer')
    name = token.value

    token = next(tokens)
    _expect(token, 'open_parenthesis')

    token = next(tokens)
    _expect(token, 'close_parenthesis')

    token = next(tokens)
    _expect(token, 'open_brace')

    statement = parse_statement(tokens)

    token = next(tokens)
    _expect(token, 'close_brace')

    return ast_data_structures.Function(name, statement)

def parse_program(tokens):
    function = parse_function(tokens)

    return ast_data_structures.Program(function)

def parse(tokens):
    peekable_tokens = PeekableIterator(tokens)
    return parse_program(peekable_tokens)
