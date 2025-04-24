from tag import Tag
from read_external_code import read_external_code
from token_identificator import Token

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
                self.peek = self.read_char()
                return Token(tag, lexeme, self.line)
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
                    self.peek = self.read_char()
                    return Token(Tag.REAL, float(bytes(lexeme_bytes).decode('ascii')), self.line)
                else:
                    self.peek = self.read_char()
                    return Token(Tag.NUM, int(lexeme), self.line)
            elif self.peek == ord("'"):
                char_val = self.read_char()
                if self.read_char() == ord("'"):
                    self.peek = self.read_char()
                    return Token(Tag.CHAR, chr(char_val), self.line)
                else:
                    raise SyntaxError(f"Caractere mal formado na linha {self.line}")
            elif self.peek == Tag.LPAREN:
                self.peek = self.read_char() 
                return Token(Tag.LPAREN, '(', self.line)
            elif self.peek == Tag.RPAREN:
                self.peek = self.read_char() 
                return Token(Tag.RPAREN, ')', self.line)
            elif self.peek == Tag.LBRACE:
                self.peek = self.read_char() 
                return Token(Tag.LBRACE, '{', self.line)
            elif self.peek == Tag.RBRACE:
                self.peek = self.read_char() 
                return Token(Tag.RBRACE, '}', self.line)
            elif self.peek == Tag.LBRACKET:
                self.peek = self.read_char() 
                return Token(Tag.LBRACKET, '[', self.line)
            elif self.peek == Tag.RBRACKET:
                self.peek = self.read_char() 
                return Token(Tag.RBRACKET, ']', self.line)
            elif self.peek == Tag.SEMICOLON:
                self.peek = self.read_char() 
                return Token(Tag.SEMICOLON, ';', self.line)
            elif self.peek == Tag.COMMA:
                self.peek = self.read_char() 
                return Token(Tag.COMMA, ',', self.line)
            elif self.peek == Tag.ASSIGN:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_EQ, '==', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(Tag.ASSIGN, '=', self.line)
            elif self.peek == Tag.OP_NOT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_NE, '!=', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(Tag.OP_NOT, '!', self.line)
            elif self.peek == Tag.OP_LT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_LE, '<=', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(Tag.OP_LT, '<', self.line)
            elif self.peek == Tag.OP_GT:
                if self.peek_char() == Tag.ASSIGN:
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_GE, '>=', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(Tag.OP_GT, '>', self.line)
            elif self.peek == ord('|'):
                if self.peek_char() == ord('|'):
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_OR, '||', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(ord('|'), self.line)
            elif self.peek == ord('&'):
                if self.peek_char() == ord('&'):
                    self.read_char()
                    self.read_char()
                    self.peek = self.read_char() 
                    return Token(Tag.OP_AND, '&&', self.line)
                else:
                    self.peek = self.read_char() 
                    return Token(ord('&'), self.line)
            elif self.peek == Tag.OP_ADD:
                self.peek = self.read_char() 
                return Token(Tag.OP_ADD, '+', self.line)
            elif self.peek == Tag.OP_SUB:
                self.peek = self.read_char() 
                return Token(Tag.OP_SUB, '-', self.line)
            elif self.peek == Tag.OP_MUL:
                self.peek = self.read_char() 
                return Token(Tag.OP_MUL, '*', self.line)
            elif self.peek == Tag.OP_DIV:
                self.peek = self.read_char() 
                return Token(Tag.OP_DIV, '/', self.line)
            elif self.peek == Tag.OP_MOD:
                self.peek = self.read_char() 
                return Token(Tag.OP_MOD, '%', self.line)
            else:
                self.peek = self.read_char() 
                return Token(self.peek)
