from lexer import Lexer
from tag import Tag

if __name__ == "__main__":
    lexer = Lexer()
    tokens = []
    token = lexer.scan()
    while token.tag != Tag.EOF:
        tokens.append(token)
        token = lexer.scan()
    tokens.append(token) # Adiciona o token de EOF

    for token in tokens:
        print(token)
