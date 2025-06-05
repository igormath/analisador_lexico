class Tag:
    # KEYWORDS
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
    DO = 'DO'
    BREAK = 'BREAK'

    # TABELA ASCII
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

    # Outros
    ID = 'ID'
    NUM = 'NUM'
    REAL = 'REAL'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    EOF = 'EOF'
