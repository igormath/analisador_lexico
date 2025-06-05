from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer)
    try:
        parser.program()
        print(parser.symbol_table)
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")
