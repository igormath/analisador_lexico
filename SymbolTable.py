from Symbol import Symbol

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.current_scope = "global" # POr enquanto, só temos o escopo global.

    def add(self, name, type_, value=None, is_array=False, size=None):
        # Por so termos o escopo global, identificadores são únicos globalmente.
        if name in self.symbols:
            raise Exception(f"Identificador '{name}' já declarado no escopo '{self.current_scope}'.")
        self.symbols[name] = Symbol(name, type_, value, self.current_scope, is_array, size)

    def get(self, name):
        return self.symbols.get(name, None)

    def __contains__(self, name):
        return name in self.symbols

    def __repr__(self):
        return str(self.symbols)
