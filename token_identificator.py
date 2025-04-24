class Token:
    def __init__(self, tag, value=None, line=None):
        self.tag = tag
        self.value = value
        self.line = line

    def __str__(self):
        return f"<{self.tag}, {self.value if self.value is not None else ''}, {self.line}>"
