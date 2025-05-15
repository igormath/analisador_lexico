class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Inicializa com o escopo global

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Não é possível sair do escopo global")

    def insert(self, name, type, line): # 'value' pode conter mais informações
        self.scopes[-1][name] = {'type': type, 'line': line}

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
