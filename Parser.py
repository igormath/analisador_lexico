from Tag import Tag
from SymbolTable import SymbolTable
from Symbol import Symbol
from IntermediateCodeGenerator import IntermediateCodeGenerator


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.scan()
        self.symbol_table = SymbolTable()
        self.gen = IntermediateCodeGenerator()
        self.current_break_target = None

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
        while self.lookahead.tag in [Tag.INT, Tag.BOOL, Tag.FLOAT, Tag.CHAR_TYPE]:
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
        
        self.symbol_table.add(name=var_name, type_=var_type, is_array=is_array_declaration, size=array_size)
        
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
            expr_addr = self.expression()
            self.gen.emit('assign', expr_addr, var_name)
        self.match(Tag.SEMICOLON)

    def type(self):
        if self.lookahead.tag == Tag.INT:
            self.match(Tag.INT)
        elif self.lookahead.tag == Tag.BOOL:
            self.match(Tag.BOOL)
        elif self.lookahead.tag == Tag.FLOAT:
            self.match(Tag.FLOAT)
        elif self.lookahead.tag == Tag.CHAR_TYPE:
            self.match(Tag.CHAR_TYPE)
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
        var_token = self.lookahead
        self.match(Tag.ID)
        var_name = var_token.value
        symbol = self.symbol_table.get(var_name)
        if not symbol:
            raise SyntaxError(f"Variável '{var_name}' não declarada na linha {self.lexer.line}.")
        if self.lookahead.tag == Tag.LBRACKET:
            if not symbol.is_array:
                raise SyntaxError(f"Variável '{var_name}' não é um array na linha {self.lexer.line}.")
            self.match(Tag.LBRACKET)
            index_addr =  self.expression()
            self.match(Tag.RBRACKET)
            self.match(Tag.ASSIGN)
            source_addr = self.expression()
            self.gen.emit('indexed_assign_to', source_addr, var_name, index_addr) # a[index_addr] = source_addr
            self.match(Tag.SEMICOLON)
        else: # atribuiçõa simples, ñ array
            self.match(Tag.ASSIGN)
            expr_addr = self.expression()
            self.gen.emit('assign', expr_addr, var_name)
            self.match(Tag.SEMICOLON)


    def if_command(self):
        self.match(Tag.IF)
        self.match(Tag.LPAREN)
        condition_addr = self.expression()
        self.match(Tag.RPAREN)
        
        label_after_if_body = self.gen.new_label()
        self.gen.emit('if_false_goto', condition_addr, label_after_if_body)
        
        self.command()
        if self.lookahead.tag == Tag.ELSE:
            label_after_else_body = self.gen.new_label()
            self.gen.emit('goto', label_after_else_body) # se entrar no if, pula o else
            self.gen.emit(label_after_if_body) # se for falso, onde está o else
            self.match(Tag.ELSE)
            self.command()
            self.gen.emit(label_after_else_body) # para onde segue o fluxo pós else
        else:
            self.gen.emit(label_after_if_body)

    def while_command(self):
        label_test = self.gen.new_label()
        label_after = self.gen.new_label()

        previous_break_target = self.current_break_target
        self.current_break_target = label_after

        self.match(Tag.WHILE)
        self.gen.emit(label_test)

        self.match(Tag.LPAREN)
        condition_addr = self.expression()
        self.match(Tag.RPAREN)

        self.gen.emit('if_false_goto', condition_addr, label_after)

        self.command()

        self.gen.emit('goto', label_test)
        self.gen.emit(label_after)
        
        self.current_break_target = previous_break_target
        
    def do_while_command(self):
        label_start_loop = self.gen.new_label()
        label_after_loop = self.gen.new_label() # Para o break

        previous_break_target = self.current_break_target
        self.current_break_target = label_after_loop

        self.match(Tag.DO)
        self.gen.emit(label_start_loop)

        self.command() # Corpo do do-while

        self.match(Tag.WHILE)
        self.match(Tag.LPAREN)
        condition_addr = self.expression()
        self.match(Tag.RPAREN)
        self.match(Tag.SEMICOLON)

        self.gen.emit('if_true_goto', condition_addr, label_start_loop)
        self.gen.emit(label_after_loop)

        self.current_break_target = previous_break_target
        
    def break_command(self):
        self.match(Tag.BREAK)
        self.match(Tag.SEMICOLON)
        if self.current_break_target:
            self.gen.emit('goto', self.current_break_target)
        else:
            raise SyntaxError(f"'break' fora de um loop na linha {self.lexer.line}")

    def expression(self):
        left_addr = self.conjunction()
        while self.lookahead.tag == Tag.OP_OR:
            op_token_value = self.lookahead.value # '||'
            self.match(Tag.OP_OR)
            right_addr = self.conjunction()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            left_addr = result_addr
        return left_addr

    def conjunction(self):
        left_addr = self.equality()
        while self.lookahead.tag == Tag.OP_AND:
            op_token_value = self.lookahead.value # '&&'
            self.match(Tag.OP_AND)
            right_addr = self.equality()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            left_addr = result_addr
        return left_addr
    
    def equality(self):
        left_addr = self.relation()
        if self.lookahead.tag in [Tag.OP_EQ, Tag.OP_NE]:
            op_token_value = self.lookahead.value # '==' ou '!='
            self.match(self.lookahead.tag)
            right_addr = self.relation()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            return result_addr
        return left_addr
    
    def relation(self):
        left_addr = self.addition()
        if self.lookahead.tag in [Tag.OP_LT, Tag.OP_LE, Tag.OP_GT, Tag.OP_GE]:
            op_token_value = self.lookahead.value # '<', '<=', '>', '>='
            self.match(self.lookahead.tag)
            right_addr = self.addition()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            return result_addr
        return left_addr

    def addition(self):
        left_addr = self.term()
        while self.lookahead.tag in [Tag.OP_ADD, Tag.OP_SUB]:
            op_token_value = self.lookahead.value # '+' ou '-'
            self.match(self.lookahead.tag)
            right_addr = self.term()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            left_addr = result_addr
        return left_addr

    def term(self):
        left_addr = self.factor()
        while self.lookahead.tag in [Tag.OP_MUL, Tag.OP_DIV, Tag.OP_MOD]:
            op_token_value = self.lookahead.value # '*', '/', '%'
            self.match(self.lookahead.tag)
            right_addr = self.factor()
            result_addr = self.gen.new_temp()
            self.gen.emit(op_token_value, left_addr, right_addr, result_addr)
            left_addr = result_addr
        return left_addr
    
    def factor(self):
        if self.lookahead.tag in [Tag.OP_SUB, Tag.OP_NOT]: # Operadores unários
            op_token_value = self.lookahead.value # '-' ou '!'
            self.match(self.lookahead.tag)
            operand_addr = self.primary() # factor -> primary na sua gramática original para unários
            result_addr = self.gen.new_temp()
            # Usar um prefixo para distinguir unário, ex: 'unary_-'
            self.gen.emit(f"unary_{op_token_value}", operand_addr, result_addr)
            return result_addr
        return self.primary()
    
    def primary(self):
        if self.lookahead.tag == Tag.ID:
            id_token = self.lookahead
            var_name = id_token.value
            self.match(Tag.ID)
            symbol = self.symbol_table.get(var_name)
            if not symbol:
                raise SyntaxError(f"Variável '{var_name}' não declarada na linha {self.lexer.line}.")

            if self.lookahead.tag == Tag.LBRACKET: # Acesso a array: a[i]
                if not symbol.is_array:
                        raise SyntaxError(f"Variável '{var_name}' não é um array mas está sendo acessada como um, linha {self.lexer.line}.")
                self.match(Tag.LBRACKET)
                index_addr = self.expression()
                self.match(Tag.RBRACKET)
                dest_temp = self.gen.new_temp()
                self.gen.emit('indexed_assign_from', var_name, index_addr, dest_temp) # dest_temp = var_name[index_addr]
                return dest_temp
            return var_name # Retorna o nome do ID

        elif self.lookahead.tag in [Tag.NUM, Tag.REAL, Tag.CHAR_LITERAL, Tag.TRUE, Tag.FALSE]:
            return self.literal() # literal() faz o match e retorna o valor/representação

        elif self.lookahead.tag == Tag.LPAREN:
            self.match(Tag.LPAREN)
            expr_addr = self.expression()
            self.match(Tag.RPAREN)
            return expr_addr

        # Remoção da regra de type casting (INT LPAREN expression RPAREN) que estava no seu código
        # Se precisar, adicione de volta com geração de código apropriada.
        else:
            raise SyntaxError(f"Primário inválido encontrado: {self.lookahead} na linha {self.lexer.line}")
    
    def literal(self):
        tag = self.lookahead.tag
        val = self.lookahead.value
        if tag == Tag.NUM:
            self.match(Tag.NUM)
            return val # Retorna o número diretamente
        elif tag == Tag.REAL:
            self.match(Tag.REAL)
            return val # Retorna o float diretamente
        elif tag == Tag.TRUE:
            self.match(Tag.TRUE)
            return True # Ou 1 para consistência em algumas representações de CTE
        elif tag == Tag.FALSE:
            self.match(Tag.FALSE)
            return False # Ou 0
        elif tag == Tag.CHAR_LITERAL:
            self.match(Tag.CHAR_LITERAL)
            return f"'{val}'" # Representação para distinguir de IDs
        else:
            # Este else não deveria ser alcançado se primary() filtrou corretamente
            raise SyntaxError(f"Literal inválido esperado, encontrado: {self.lookahead} na linha {self.lexer.line}")
