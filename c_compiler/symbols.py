from collections import defaultdict

class Symbols:
    def __init__(self):
        self.symbol_counters = defaultdict(int)

    def create_symbol(self, name):
        symbol = name + str(self.symbol_counters[name])

        self.symbol_counters[name] += 1

        return symbol
