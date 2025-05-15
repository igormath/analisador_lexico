from lexer import Lexer
from tag import Tag
from symbol_table import SymbolTable

if __name__ == "__main__":
    lexer = Lexer()
    tokens = []
    token = lexer.scan()
    while token.tag != Tag.EOF:
        tokens.append(token)
        token = lexer.scan()
    tokens.append(token) # O útlimo token será EOF (end of file)

    symbol_table = SymbolTable()
    current_type = None

    for token in tokens:
        print(token) # Ainda imprimindo os tokens para debug

        if token.tag in [Tag.INT, Tag.BOOL, Tag.FLOAT, Tag.CHAR]:
            current_type = token.tag
        elif token.tag == Tag.ID:
            if current_type:
                symbol_table.insert(token.value, current_type, token.line)
                current_type = None # Reseta o tipo após a declaração
            elif symbol_table.lookup(token.value) is None:
                print(f"Erro: Variável '{token.value}' não declarada antes do uso na linha {token.line}.")
        elif token.tag == Tag.SCOPE_BEGIN:
            symbol_table.enter_scope()
        elif token.tag == Tag.SCOPE_END:
            symbol_table.exit_scope()

    print(symbol_table.scopes)
