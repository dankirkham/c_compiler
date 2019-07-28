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

    factor = parse_factor(tokens);

    return ast_data_structures.UnaryOperator(operator, factor)

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
    root_expression = parse_factor(tokens)

    while tokens.peek().type in ['multiplication_operator', 'division_operator']:
        operation = next(tokens).type
        e2 = parse_factor(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

def parse_additive_expression(tokens):
    root_expression = parse_term(tokens)

    while tokens.peek().type in ['addition_operator', 'negation']:
        operation = next(tokens).type
        e2 = parse_term(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

def parse_relational_expression(tokens):
    root_expression = parse_additive_expression(tokens)

    while tokens.peek().type in ['less_than', 'less_than_or_equal', 'greater_than', 'greater_than_or_equal']:
        operation = next(tokens).type
        e2 = parse_additive_expression(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

def parse_equality_expression(tokens):
    root_expression = parse_relational_expression(tokens)

    while tokens.peek().type in ['equal_comparison', 'not_equal_comparison']:
        operation = next(tokens).type
        e2 = parse_relational_expression(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

def parse_logical_and_expression(tokens):
    root_expression = parse_equality_expression(tokens)

    while tokens.peek().type in ['logical_and']:
        operation = next(tokens).type
        e2 = parse_equality_expression(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

def parse_expression(tokens):
    root_expression = parse_logical_and_expression(tokens)

    while tokens.peek().type in ['logical_or']:
        operation = next(tokens).type
        e2 = parse_logical_and_expression(tokens)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

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
