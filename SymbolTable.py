class Symbol:
    def __init__(self, name, type_, value=None):
        self.name = name
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.type}, value={self.value})"

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, name, type_, value=None):
        if name in self.symbols:
            raise Exception(f"Identificador '{name}' já declarado.")
        self.symbols[name] = Symbol(name, type_, value)

    def get(self, name):
        return self.symbols.get(name, None)

    def __contains__(self, name):
        return name in self.symbols

    def __repr__(self):
        return str(self.symbols)