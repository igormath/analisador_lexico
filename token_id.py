def identify_token(char, linha, tokenList):
    if (char == '('):
        token = ('LEFTPAR', linha)
        tokenList.append(token)
    elif (char == ')'):
        token = ('RIGHTPAR', linha)
        tokenList.append(token)
    elif (char == '{'):
        token = ('LEFTCHAV', linha)
        tokenList.append(token)
    elif (char == '}'):
        token = ('RIGHTCHAV', linha)
        tokenList.append(token)
    elif (char == ';'):
        token = ('PONTOVIRGULA', linha)
        tokenList.append(token)
    elif (char == 'int'):
        token = ('KEYWORD_INT', linha)
        tokenList.append(token)
