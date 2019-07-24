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

def parse_unary_operator(tokens):
    token = next(tokens)
    operator = token.type

    expression = parse_expression(tokens);

    return ast_data_structures.UnaryOperator(operator, expression)

def parse_factor(tokens):
    if tokens.peek().type == 'open_parenthesis':
        # Parenthesis
        next(tokens)
        expression = parse_expression(tokens)
        _expect(next(tokens), 'close_parenthesis')
        return expression
    elif tokens.peek().type in ['negation', 'bitwise_complement', 'logical_negation']:
        # Unary Operator
        return parse_unary_operator(tokens)
    else:
        # Constant
        token = next(tokens)
        _expect(token, 'integer_literal')

        return ast_data_structures.Constant(int(token.value))

def parse_term(tokens):
    factors = []
    operations = []

    factors.append(parse_factor(tokens))

    while tokens.peek().type in ['multiplication_operator', 'division_operator']:
        operations.append(next(tokens).type)
        factors.append(parse_factor(tokens))

    return ast_data_structures.Term(factors, operations)

def parse_expression(tokens):
    terms = []
    operations = []

    terms.append(parse_term(tokens))

    while tokens.peek().type in ['addition_operator', 'negation']:
        operations.append(next(tokens).type)
        terms.append(parse_term(tokens))

    return ast_data_structures.Expression(terms, operations)

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
