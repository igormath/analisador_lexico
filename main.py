import sys

class Token:
    def __init__(self, tag, value=None):
        self.tag = tag
        self.value = value

    def __str__(self):
        return f"<{self.tag}, {self.value if self.value is not None else ''}>"

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
        super().__init__(Tag.CHAR, value)

class Bool(Token):
    def __init__(self, value):
        super().__init__(Tag.BOOL, value)

class Tag:
    # Palavras-chave (mantendo como strings para clareza, mas podemos usar ASCII se necessário para comparações internas)
    INT = 'INT'
    BOOL = 'BOOL'
    FLOAT = 'FLOAT'
    CHAR = 'CHAR'
    MAIN = 'MAIN'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    TRUE = 'TRUE'
    FALSE = 'FALSE'

    # Símbolos (usando valores ASCII)
    LBRACE = ord('{')  # 123
    RBRACE = ord('}')  # 125
    LPAREN = ord('(')  # 40
    RPAREN = ord(')')  # 41
    LBRACKET = ord('[') # 91
    RBRACKET = ord(']') # 93
    SEMICOLON = ord(';') # 59
    COMMA = ord(',')    # 44
    ASSIGN = ord('=')   # 61
    OP_EQ = '=='
    OP_NE = '!='
    OP_LT = ord('<')    # 60
    OP_LE = '<='
    OP_GT = ord('>')    # 62
    OP_GE = '>='
    OP_ADD = ord('+')   # 43
    OP_SUB = ord('-')   # 45
    OP_MUL = ord('*')   # 42
    OP_DIV = ord('/')   # 47
    OP_MOD = ord('%')   # 37
    OP_OR = '||'
    OP_AND = '&&'
    OP_NOT = ord('!')   # 33

    # Outros (mantendo como strings para identificação de tipo)
    ID = 'ID'
    NUM = 'NUM'
    REAL = 'REAL'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    EOF = 'EOF'

def read_external_code():
    byte_list = []
    try:
        with open('test.clite', "rb") as f:
            byte = f.read(1)
            while byte:
                byte_list.append(byte[0])
                byte = f.read(1)
        return byte_list
    except FileNotFoundError:
        print('Erro. Arquivo não encontrado.')
        return None

class Lexer:
    def __init__(self):
        self.line = 1
        self.peek = None  # Inicializado com um valor inteiro
        self.keywords = {
            "int": Tag.INT,
            "bool": Tag.BOOL,
            "float": Tag.FLOAT,
            "char": Tag.CHAR,
            "main": Tag.MAIN,
            "if": Tag.IF,
            "else": Tag.ELSE,
            "while": Tag.WHILE,
            "true": Tag.TRUE,
            "false": Tag.FALSE
        }
        self.byte_list = read_external_code()
        self.current_byte_index = 0

    def read_char(self):
        if self.byte_list is not None and self.current_byte_index < len(self.byte_list):
            byte_val = self.byte_list[self.current_byte_index]
            self.current_byte_index += 1
            return byte_val
        else:
            return None

    def peek_char(self):
        if self.byte_list is not None and self.current_byte_index < len(self.byte_list):
            return self.byte_list[self.current_byte_index]
        else:
            return None

    def scan(self):
        if self.peek is None:
            self.peek = self.read_char()
        while True:
            if self.peek is None:
                return Token(Tag.EOF)
            if chr(self.peek).isspace():
                if self.peek == ord('\n'):
                    self.line += 1
                self.peek = self.read_char()
                continue
            elif chr(self.peek).isalpha():
                lexeme_bytes = [self.peek]
                while True:
                    next_byte = self.peek_char()
                    if next_byte is not None and (chr(next_byte).isalpha() or chr(next_byte).isdigit()):
                        lexeme_bytes.append(next_byte)
                        self.peek = self.read_char()
                    else:
                        break
                lexeme = bytes(lexeme_bytes).decode('ascii')
                tag = Tag.ID
                if lexeme in self.keywords:
                    tag = self.keywords[lexeme]
                self.peek = self.read_char() # Adicionado
                return Token(tag, lexeme)
            elif chr(self.peek).isdigit():
                lexeme_bytes = [self.peek]
                while True:
                    next_byte = self.peek_char()
                    if next_byte is not None and chr(next_byte).isdigit():
                        lexeme_bytes.append(next_byte)
                        self.peek = self.read_char()
                    else:
                        break
                lexeme = bytes(lexeme_bytes).decode('ascii')
                if self.peek_char() == ord('.'):
                    lexeme_bytes.append(self.read_char())
                    while True:
                        next_byte = self.peek_char()
                        if next_byte is not None and chr(next_byte).isdigit():
                            lexeme_bytes.append(next_byte)
                            self.peek = self.read_char()
                        else:
                            break
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.REAL, float(bytes(lexeme_bytes).decode('ascii')))
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.NUM, int(lexeme))
            elif self.peek == ord("'"):
                char_val = self.read_char()
                if self.read_char() == ord("'"):
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.CHAR, chr(char_val))
                else:
                    raise SyntaxError(f"Caractere mal formado na linha {self.line}")
            elif self.peek == Tag.LPAREN:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.LPAREN, '(')
            elif self.peek == Tag.RPAREN:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.RPAREN, ')')
            elif self.peek == Tag.LBRACE:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.LBRACE, '{')
            elif self.peek == Tag.RBRACE:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.RBRACE, '}')
            elif self.peek == Tag.LBRACKET:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.LBRACKET, '[')
            elif self.peek == Tag.RBRACKET:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.RBRACKET, ']')
            elif self.peek == Tag.SEMICOLON:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.SEMICOLON, ';')
            elif self.peek == Tag.COMMA:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.COMMA, ',')
            elif self.peek == Tag.ASSIGN:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_EQ, '==')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.ASSIGN, '=')
            elif self.peek == Tag.OP_NOT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_NE, '!=')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_NOT, '!')
            elif self.peek == Tag.OP_LT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_LE, '<=')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_LT, '<')
            elif self.peek == Tag.OP_GT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_GE, '>=')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_GT, '>')
            elif self.peek == ord('|'):
                if self.peek_char() == ord('|'):
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_OR, '||')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(ord('|'))
            elif self.peek == ord('&'):
                if self.peek_char() == ord('&'):
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() # Adicionado
                    return Token(Tag.OP_AND, '&&')
                else:
                    self.peek = self.read_char() # Adicionado
                    return Token(ord('&'))
            elif self.peek == Tag.OP_ADD:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.OP_ADD, '+')
            elif self.peek == Tag.OP_SUB:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.OP_SUB, '-')
            elif self.peek == Tag.OP_MUL:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.OP_MUL, '*')
            elif self.peek == Tag.OP_DIV:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.OP_DIV, '/')
            elif self.peek == Tag.OP_MOD:
                self.peek = self.read_char() # Adicionado
                return Token(Tag.OP_MOD, '%')
            else:
                self.peek = self.read_char() # Adicionado
                return Token(self.peek)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.scan()

    def match(self, tag):
        print(f"Matching: Esperado '{tag}', Lookahead atual: '{self.lookahead}'") # Depuração
        if self.lookahead.tag == tag:
            print(f"  Match bem-sucedido. Lendo próximo token.") # Depuração
            self.lookahead = self.lexer.scan()
            print(f"  Próximo lookahead: '{self.lookahead}'") # Depuração
        else:
            raise SyntaxError(f"Esperado '{tag}', encontrado '{self.lookahead}' na linha {self.lexer.line}")

    def program(self):
        print(f"Lookahead inicial no program(): {self.lookahead}") # Depuração
        self.match(Tag.INT)
        print(f"Lookahead após match(INT): {self.lookahead}") # Depuração
        self.match(Tag.MAIN)
        print(f"Lookahead após match(MAIN): {self.lookahead}") # Depuração
        self.match(Tag.LPAREN)
        print(f"Lookahead após match(LPAREN): {self.lookahead}") # Depuração
        self.match(Tag.RPAREN)
        print(f"Lookahead após match(RPAREN): {self.lookahead}") # Depuração
        self.match(Tag.LBRACE)
        self.declarations()
        self.commands()
        self.match(Tag.RBRACE)
        self.match(Tag.EOF)
        print("Análise sintática bem-sucedida!")

    def declarations(self):
        while self.lookahead.tag in [Tag.INT, Tag.BOOL, Tag.FLOAT, Tag.CHAR]:
            self.declaration()

    def declaration(self):
        self.type()
        self.match(Tag.ID)
        if self.lookahead.tag == Tag.LBRACKET:
            self.match(Tag.LBRACKET)
            self.match(Tag.NUM)
            self.match(Tag.RBRACKET)
        while self.lookahead.tag == Tag.COMMA:
            self.match(Tag.COMMA)
            self.match(Tag.ID)
            if self.lookahead.tag == Tag.LBRACKET:
                self.match(Tag.LBRACKET)
                self.match(Tag.NUM)
                self.match(Tag.RBRACKET)
        if self.lookahead.tag == Tag.ASSIGN:
            self.match(Tag.ASSIGN)
            self.expression() # Ou um método mais específico para o valor inicial
        self.match(Tag.SEMICOLON)

    def type(self):
        if self.lookahead.tag == Tag.INT:
            self.match(Tag.INT)
        elif self.lookahead.tag == Tag.BOOL:
            self.match(Tag.BOOL)
        elif self.lookahead.tag == Tag.FLOAT:
            self.match(Tag.FLOAT)
        elif self.lookahead.tag == Tag.CHAR:
            self.match(Tag.CHAR)
        else:
            raise SyntaxError(f"Tipo inválido encontrado: {self.lookahead} na linha {self.lexer.line}")

    def commands(self):
        while self.lookahead.tag != Tag.RBRACE:
            self.command()

    def command(self):
        if self.lookahead.tag == Tag.SEMICOLON:
            self.match(Tag.SEMICOLON)
        elif self.lookahead.tag == Tag.LBRACE:
            self.block()
        elif self.lookahead.tag == Tag.ID:
            self.assignment()
        elif self.lookahead.tag == Tag.IF:
            self.if_command()
        elif self.lookahead.tag == Tag.WHILE:
            self.while_command()
        else:
            raise SyntaxError(f"Comando inválido encontrado: {self.lookahead} na linha {self.lexer.line}")

    def block(self):
        self.match(Tag.LBRACE)
        self.commands()
        self.match(Tag.RBRACE)

    def assignment(self):
        self.match(Tag.ID)
        if self.lookahead.tag == Tag.LBRACKET:
            self.match(Tag.LBRACKET)
            self.expression()
            self.match(Tag.RBRACKET)
        self.match(Tag.ASSIGN)
        self.expression()
        self.match(Tag.SEMICOLON)

    def if_command(self):
        self.match(Tag.IF)
        self.match(Tag.LPAREN)
        self.expression()
        self.match(Tag.RPAREN)
        self.command()
        if self.lookahead.tag == Tag.ELSE:
            self.match(Tag.ELSE)
            self.command()

    def while_command(self):
        self.match(Tag.WHILE)
        self.match(Tag.LPAREN)
        self.expression()
        self.match(Tag.RPAREN)
        self.command()

    def expression(self):
        self.conjunction()
        while self.lookahead.tag == Tag.OP_OR:
            self.match(Tag.OP_OR)
            self.conjunction()

    def conjunction(self):
        self.equality()
        while self.lookahead.tag == Tag.OP_AND:
            self.match(Tag.OP_AND)
            self.equality()

    def equality(self):
        self.relation()
        if self.lookahead.tag in [Tag.OP_EQ, Tag.OP_NE]:
            op = self.lookahead.tag
            self.match(op)
            self.relation()

    def relation(self):
        self.addition()
        if self.lookahead.tag in [Tag.OP_LT, Tag.OP_LE, Tag.OP_GT, Tag.OP_GE]:
            op = self.lookahead.tag
            self.match(op)
            self.addition()

    def addition(self):
        self.term()
        while self.lookahead.tag in [Tag.OP_ADD, Tag.OP_SUB]:
            op = self.lookahead.tag
            self.match(op)
            self.term()

    def term(self):
        self.factor()
        while self.lookahead.tag in [Tag.OP_MUL, Tag.OP_DIV, Tag.OP_MOD]:
            op = self.lookahead.tag
            self.match(op)
            self.factor()

    def factor(self):
        if self.lookahead.tag in [Tag.OP_SUB, Tag.OP_NOT]:
            op = self.lookahead.tag
            self.match(op)
        self.primary()

    def primary(self):
        if self.lookahead.tag == Tag.ID:
            self.match(Tag.ID)
            if self.lookahead.tag == Tag.LBRACKET:
                self.match(Tag.LBRACKET)
                self.expression()
                self.match(Tag.RBRACKET)
        elif self.lookahead.tag in [Tag.NUM, Tag.REAL, Tag.CHAR, Tag.BOOL]:
            self.literal()
        elif self.lookahead.tag == Tag.LPAREN:
            self.match(Tag.LPAREN)
            self.expression()
            self.match(Tag.RPAREN)
        elif self.lookahead.tag in [Tag.INT, Tag.BOOL, Tag.FLOAT, Tag.CHAR]:
            self.type()
            self.match(Tag.LPAREN)
            self.expression()
            self.match(Tag.RPAREN)
        else:
            raise SyntaxError(f"Primário inválido encontrado: {self.lookahead} na linha {self.lexer.line}")

    def literal(self):
        if self.lookahead.tag == Tag.NUM:
            self.match(Tag.NUM)
        elif self.lookahead.tag == Tag.BOOL:
            self.match(Tag.BOOL)
        elif self.lookahead.tag == Tag.REAL:
            self.match(Tag.REAL)
        elif self.lookahead.tag == Tag.CHAR:
            self.match(Tag.CHAR)
        else:
            raise SyntaxError(f"Literal inválido encontrado: {self.lookahead} na linha {self.lexer.line}")

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer)
    try:
        parser.program()
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")
