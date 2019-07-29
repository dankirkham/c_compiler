from c_compiler.parser_error import ParserError

class SymbolMap:
    WORD_SIZE = 8

    def __init__(self):
        self.symbols = {}
        self.next_offset = -SymbolMap.WORD_SIZE

    def declare(self, identifier):
        if identifier in self.symbols:
            raise ParserError('"{}" already defined in this scope.'.format(identifier))

        self.next_offset += SymbolMap.WORD_SIZE
        self.symbols[identifier] = self.next_offset

    def resolve(self, identifier):
        if identifier not in self.symbols:
            raise ParserError('"{}" is an undefined identifier.'.format(identifier))

        return -self.symbols[identifier]

    def size(self):
        return self.next_offset + SymbolMap.WORD_SIZE
