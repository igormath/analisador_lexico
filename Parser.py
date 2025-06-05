from Tag import Tag
from SymbolTable import SymbolTable

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.scan()
        self.symbol_table = SymbolTable()

    def match(self, tag):
        print(f"Esperado '{tag}', Lookahead atual: '{self.lookahead}'")
        if self.lookahead.tag == tag:
            self.lookahead = self.lexer.scan()
            print(f"  Próximo lookahead: '{self.lookahead}'")
        else:
            raise SyntaxError(f"Esperado '{tag}', encontrado '{self.lookahead}' na linha {self.lexer.line}")

    def program(self):
        print(f"Lookahead inicial no program(): {self.lookahead}")
        self.match(Tag.INT)
        print(f"Lookahead após match(INT): {self.lookahead}")
        self.match(Tag.MAIN)
        print(f"Lookahead após match(MAIN): {self.lookahead}")
        self.match(Tag.LPAREN)
        print(f"Lookahead após match(LPAREN): {self.lookahead}")
        self.match(Tag.RPAREN)
        print(f"Lookahead após match(RPAREN): {self.lookahead}")
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
        var_type = self.lookahead.tag
        self.type()
        
        is_array_declaration = False
        array_size = None
        
        # var_name = self.lookahead.value
        # self.match(Tag.ID)
        # self.symbol_table.add(var_name, var_type)
        if self.lookahead.tag == Tag.LBRACKET:
            is_array_declaration = True
            self.match(Tag.LBRACKET) # match consome [
            if self.lookahead.tag != Tag.NUM:
                raise SyntaxError(f"Esperando um número para o tamanho do array na linha {self.lexer.line}")
                
            array_size = self.lookahead.value
            self.match(Tag.NUM)
            self.match(Tag.RBRACKET) # match consome ]
        
        if self.lookahead.tag != Tag.ID:
            raise SyntaxError(f"Esperado um nome de identificador, encontrado '{self.lookahead}' na linha {self.lexer.line}")
            
        id_token = self.lookahead
        var_name = id_token.value
        self.match(Tag.ID)
        
        self.symbol_table.add(var_name, var_type)
        
        # while self.lookahead.tag == Tag.COMMA:
        #     self.match(Tag.COMMA)
        #     self.match(Tag.ID)
        #     if self.lookahead.tag == Tag.LBRACKET:
        #         self.match(Tag.LBRACKET)
        #         self.match(Tag.NUM)
        #         self.match(Tag.RBRACKET)
        if self.lookahead.tag == Tag.ASSIGN:
            if is_array_declaration:
                raise SyntaxError(f'Atribuição direta a array na declaração não suportada na linha {self.lexer.line}')
            self.match(Tag.ASSIGN)
            self.expression()
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
        elif self.lookahead.tag == Tag.DO:
            self.do_while_command()
        elif self.lookahead.tag == Tag.BREAK:
            self.break_command()
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
        
    def do_while_command(self):
        self.match(Tag.DO)
        self.command()
        self.match(Tag.WHILE)
        self.match(Tag.LPAREN)
        self.expression()
        self.match(Tag.RPAREN)
        self.match(Tag.SEMICOLON)
        
    def break_command(self):
        self.match(Tag.BREAK)
        self.match(Tag.SEMICOLON)

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
        elif self.lookahead.tag in [Tag.NUM, Tag.REAL, Tag.CHAR, Tag.BOOL, Tag.TRUE, Tag.FALSE]:
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
        elif self.lookahead.tag == Tag.TRUE:
            self.match(Tag.TRUE)
        elif self.lookahead.tag == Tag.FALSE:
            self.match(Tag.FALSE)
        elif self.lookahead.tag == Tag.REAL:
            self.match(Tag.REAL)
        elif self.lookahead.tag == Tag.CHAR:
            self.match(Tag.CHAR)
        else:
            raise SyntaxError(f"Literal inválido encontrado: {self.lookahead} na linha {self.lexer.line}")
