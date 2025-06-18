class Symbol:
    def __init__(self, name, type_, value=None, scope=None, is_array=False, size=None):
        self.name = name
        self.type = type_ 
        self.value = value
        self.scope = scope # Por enquanto, só temos o escopo Global.
        self.is_array = is_array
        self.size = size

    def __repr__(self):
        return (f"Symbol(name={self.name}, type={self.type}, value={self.value}, "
                f"scope={self.scope}, is_array={self.is_array}, size={self.size})")
