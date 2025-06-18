from Tag import Tag

class Token:
    def __init__(self, tag, value=None, line=None):
        self.tag = tag
        self.value = value
        self.line = line

    def __str__(self):
        return f"<{self.tag}, {self.value if self.value is not None else ''}, {self.line}>"

class Word(Token):
    def __init__(self, lexeme, tag):
        super().__init__(tag, lexeme)

class Num(Token):
    def __init__(self, value):
        super().__init__(Tag.NUM, value)

class Real(Token):
    def __init__(self, value):
        super().__init__(Tag.REAL, value)

class Char(Token):
    def __init__(self, value):
        super().__init__(Tag.CHAR_LITERAL, value)

class Bool(Token):
    def __init__(self, value):
        super().__init__(Tag.BOOL, value)
