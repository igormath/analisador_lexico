from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer)
    try:
        parser.program()
        print("\n--- Tabela de Símbolos ---")
        print(parser.symbol_table)
        print("\n--- Código Intermediário ---")
        print(parser.gen)
    except SyntaxError as e:
            print(f"Erro de sintaxe: {e}")
    except Exception as e: # Captura outras exceções como re-declaração de símbolo
        print(f"Erro: {e}")
