from c_compiler import ast_data_structures
from c_compiler.symbol_map import SymbolMap
from c_compiler.parser_error import ParserError

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

    def peek(self, distance=1):
        if self._position == len(self) + distance - 1:
            raise IndexError('Tried to peek an exhausted iterator.')
        else:
            return self.iterable[self._position + distance - 1]

def _expect(token, types):
    if not isinstance(types, list):
        types = [types]

    if token.type not in types:
        raise ParserError("Expected {} at {}".format(types, token))

def parse_unary_operator(tokens, symbol_map):
    token = next(tokens)
    operator = token.type

    factor = parse_factor(tokens, symbol_map);

    return ast_data_structures.UnaryOperator(operator, factor)

def parse_factor(tokens, symbol_map):
    _expect(tokens.peek(), ['open_parenthesis', 'negation', 'bitwise_complement', 'logical_negation', 'identifier', 'integer_literal'])

    if tokens.peek().type == 'open_parenthesis':
        # Parenthesis
        next(tokens)
        expression = parse_expression(tokens, symbol_map)
        _expect(next(tokens), 'close_parenthesis')
        return expression
    elif tokens.peek().type in ['negation', 'bitwise_complement', 'logical_negation']:
        # Unary Operator
        return parse_unary_operator(tokens, symbol_map)
    elif tokens.peek().type == 'identifier':
        # Variable
        identifier = next(tokens).value
        symbol_map.resolve(identifier) # Check for defined
        return ast_data_structures.Variable(identifier)
    elif tokens.peek().type == 'integer_literal':
        # Constant
        token = next(tokens)
        _expect(token, 'integer_literal')

        return ast_data_structures.Constant(int(token.value))

def parse_binary_operation(tokens, symbol_map, child_function, operations):
    root_expression = child_function(tokens, symbol_map)

    while tokens.peek().type in operations:
        operation = next(tokens).type
        e2 = child_function(tokens, symbol_map)
        root_expression = ast_data_structures.BinaryOperator(operation, root_expression, e2)

    return root_expression

# Binary Operation Operator Precedence
parse_term = lambda tokens, symbol_map: parse_binary_operation(tokens, symbol_map, parse_factor, ['multiplication_operator', 'division_operator'])
parse_additive_expression = lambda tokens, symbol_map: parse_binary_operation(tokens, symbol_map, parse_term, ['addition_operator', 'negation'])
parse_relational_expression = lambda tokens, symbol_map: parse_binary_operation(tokens, symbol_map, parse_additive_expression, ['less_than', 'less_than_or_equal', 'greater_than', 'greater_than_or_equal'])
parse_equality_expression = lambda tokens, symbol_map: parse_binary_operation(tokens, symbol_map, parse_relational_expression, ['equal_comparison', 'not_equal_comparison'])
parse_logical_and_expression = lambda tokens, symbol_map: parse_binary_operation(tokens, symbol_map, parse_equality_expression, ['logical_and'])

def parse_expression(tokens, symbol_map):
    if tokens.peek().type == "identifier" and tokens.peek(2).type == "assignment":
        identifier = next(tokens).value
        symbol_map.resolve(identifier) # Check for declared variable

        next(tokens) # Consume equals sign

        e2 = parse_expression(tokens, symbol_map)

        return ast_data_structures.BinaryOperator('assignment', identifier, e2)
    else:
        return parse_binary_operation(tokens, symbol_map, parse_logical_and_expression, ['logical_or'])

def parse_statement(tokens, symbol_map):
    if tokens.peek().type == "return_keyword":
        next(tokens)

        expression = parse_expression(tokens, symbol_map)

        token = next(tokens)
        _expect(token, 'semicolon')

        return ast_data_structures.ReturnStatement(expression)
    elif tokens.peek().type == "int_keyword":
        next(tokens)

        token = next(tokens)
        _expect(token, 'identifier')
        identifier = token.value
        symbol_map.declare(identifier)

        token = next(tokens)
        _expect(token, ['assignment', 'semicolon'])
        if token.type == 'assignment':
            expression = parse_expression(tokens, symbol_map)

            token = next(tokens)
            _expect(token, 'semicolon')

            return ast_data_structures.DeclareStatement(expression, identifier)
        elif token.type == 'semicolon':
            return ast_data_structures.DeclareStatement(None, identifier)
    else: # Expression
        expression = parse_expression(tokens, symbol_map)

        token = next(tokens)
        _expect(token, 'semicolon')

        return expression


def parse_function(tokens):
    symbol_map = SymbolMap()

    token = next(tokens)
    _expect(token, 'int_keyword')

    token = next(tokens)
    _expect(token, 'identifier')
    name = token.value

    token = next(tokens)
    _expect(token, 'open_parenthesis')

    token = next(tokens)
    _expect(token, 'close_parenthesis')

    token = next(tokens)
    _expect(token, 'open_brace')

    statements = []

    while tokens.peek().type != 'close_brace':
        statements.append(parse_statement(tokens, symbol_map))

    token = next(tokens) # close_brace

    return ast_data_structures.Function(name, statements, symbol_map)

def parse_program(tokens):
    function = parse_function(tokens)

    return ast_data_structures.Program(function)

def parse(tokens):
    peekable_tokens = PeekableIterator(tokens)
    return parse_program(peekable_tokens)
