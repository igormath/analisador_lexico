def identify_token(char, linha, tokenList):
    if (char == '('):
        token = ('LEFT_PAR', linha)
        tokenList.append(token)

    elif (char == ')'):
        token = ('RIGHT_PAR', linha)
        tokenList.append(token)

    elif (char == '{'):
        token = ('LEFT_CHAV', linha)
        tokenList.append(token)

    elif (char == '}'):
        token = ('RIGHT_CHAV', linha)
        tokenList.append(token)

    elif (char == ';'):
        token = ('PONTO_VIRGULA', linha)
        tokenList.append(token)

    elif (char == 'int'):
        token = ('KEYWORD_INT', linha)
        tokenList.append(token)

    elif (char == 'main'):
        token = ('KEYWORD_MAIN', linha)
        tokenList.append(token)

    elif (char == 'bool'):
        token = ('KEYWORD_BOOL', linha)
        tokenList.append(token)

    elif (char == 'float'):
        token = ('KEYWORD_FLOAT', linha)
        tokenList.append(token)
    
    elif (char == 'char'):
        token = ('KEYWORD_CHAR', linha)
        tokenList.append(token)
    
    elif (char == 'if'):
        token = ('KEYWORD_IF', linha)
        tokenList.append(token)

    elif (char == 'else'):
        token = ('KEYWORD_ELSE', linha)
        tokenList.append(token)

    elif (char == 'while'):
        token = ('KEYWORD_WHILE', linha)
        tokenList.append(token)
    
    elif (char == 'true'):
        token = ('KEYWORD_TRUE', linha)
        tokenList.append(token)

    elif (char == 'false'):
        token = ('KEYWORD_FALSE', linha)
        tokenList.append(token)
    
    elif (char == '+'):
        token = ('OPERATOR_SOMA', linha)
        tokenList.append(token)

    elif (char == '-'):
        token = ('OPERATOR_SUBT', linha)
        tokenList.append(token)

    elif (char == '!='):
        token = ('OPERATOR_DIFF', linha)
        tokenList.append(token)

    elif (char == '>='):
        token = ('OPERATOR_MAIOR_OU_IGUAL_Q', linha)
        tokenList.append(token)

    elif (char == '>'):
        token = ('OPERATOR_MAIOR_Q', linha)
        tokenList.append(token)

    elif (char == '<='):
        token = ('OPERATOR_MENOR_OU_IGUAL_Q', linha)
        tokenList.append(token)

    elif (char == '<'):
        token = ('OPERATOR_MENOR_Q', linha)
        tokenList.append(token)

    elif (char == '*'):
        token = ('OPERATOR_MULT', linha)
        tokenList.append(token)
    
    elif (char == '/'):
        token = ('OPERATOR_DIV', linha)
        tokenList.append(token)

    elif (char == '%'):
        token = ('OPERATOR_MODULO', linha)
        tokenList.append(token)

    elif (char == '='):
        token = ('OPERATOR_ATRIBUI', linha)
        tokenList.append(token)
    
    elif (char == '=='):
        token = ('OPERATOR_IGUAL', linha)
        tokenList.append(token)

    elif (char == '!'):
        token = ('OPERATOR_NEGACAO', linha)
        tokenList.append(token)

    elif (char == '&&'):
        token = ('OPERATOR_E_LOGICO', linha)
        tokenList.append(token)

    elif (char == '||'):
        token = ('OPERATOR_OU_LOGICO', linha)
        tokenList.append(token)
