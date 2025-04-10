code_string = ''
tokenList = []
linhaAtual = 1
from token_id import identify_token
from read_external_code import read_external_code

code_string = read_external_code(code_string=code_string)

print(code_string)

i = 0

while i < len(code_string):
    if (code_string[i] == '(' or code_string[i] == ')' or code_string[i] == '{' or code_string[i] == '}' or code_string[i] == ';'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '+'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '-'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '*'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '/'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '%'):
        identify_token(char=code_string[i], linha=linhaAtual, tokenList=tokenList)

    elif (code_string[i] == '!'):
        if (code_string[i + 1] == '='):
            identify_token(char='!=', linha=linhaAtual, tokenList=tokenList)
            i += 1
        else:
            identify_token(char='!', linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '&'):
        if (code_string[i + 1] == '&'):
            identify_token(char='&&', linha=linhaAtual, tokenList=tokenList)
            i += 1

    elif (code_string[i] == '|'):
        if (code_string[i + 1] == '|'):
            identify_token(char='||', linha=linhaAtual, tokenList=tokenList)
            i += 1

    elif (code_string[i] == '='):
        if (code_string[i + 1] == '='):
            identify_token(char='==', linha=linhaAtual, tokenList=tokenList)
            i += 1
        else:
            identify_token(char='=', linha=linhaAtual, tokenList=tokenList)

    
    elif (code_string[i] == '>'):
        if (code_string[i + 1] == '='):
            identify_token(char='>=', linha=linhaAtual, tokenList=tokenList)
            i += 1
        else:
            identify_token(char='>', linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == '<'):
        if (code_string[i + 1] == '='):
            identify_token(char='<=', linha=linhaAtual, tokenList=tokenList)
            i += 1
        else:
            identify_token(char='<', linha=linhaAtual, tokenList=tokenList)
    
    elif (code_string[i] == 'i'):
        if (code_string[i + 1] == 'n'):
            if (code_string[i + 2] == 't'):
                identify_token(char='int', linha=linhaAtual, tokenList=tokenList)
                i += 2
        elif (code_string[i + 1] == 'f'):
            identify_token(char='if', linha=linhaAtual, tokenList=tokenList)
            i += 1

    elif (code_string[i] == 'm'):
        if (code_string[i + 1] == 'a'):
            if (code_string[i + 2] == 'i'):
                if (code_string[i + 3] == 'n'):
                    identify_token(char='main', linha=linhaAtual, tokenList=tokenList)
                    i += 3
    
    elif (code_string[i] == 'b'):
        if (code_string[i + 1] == 'o'):
            if (code_string[i + 2] == 'o'):
                if (code_string[i + 3] == 'l'):
                    identify_token(char='bool', linha=linhaAtual, tokenList=tokenList)
                    i += 3

    elif (code_string[i] == 'f'):
        if (code_string[i + 1] == 'l'):
            if (code_string[i + 2] == 'o'):
                if (code_string[i + 3] == 'a'):
                    if (code_string[i + 4] == 't'):
                        identify_token(char='float', linha=linhaAtual, tokenList=tokenList)
                        i += 4
        elif (code_string[i + 1] == 'a'):
            if (code_string[i + 2] == 'l'):
                if (code_string[i + 3] == 's'):
                    if (code_string[i + 4] == 'e'):
                        identify_token(char='false', linha=linhaAtual, tokenList=tokenList)
                        i += 4

    elif (code_string[i] == 'c'):
        if (code_string[i + 1] == 'h'):
            if (code_string[i + 2] == 'a'):
                if (code_string[i + 3] == 'r'):
                    identify_token(char='char', linha=linhaAtual, tokenList=tokenList)
                    i += 3

    elif (code_string[i] == 'e'):
        if (code_string[i + 1] == 'l'):
            if (code_string[i + 2] == 's'):
                if (code_string[i + 3] == 'e'):
                    identify_token(char='else', linha=linhaAtual, tokenList=tokenList)
                    i += 3

    elif (code_string[i] == 'w'):
        if (code_string[i + 1] == 'h'):
            if (code_string[i + 2] == 'i'):
                if (code_string[i + 3] == 'l'):
                    if (code_string[i + 4] == 'e'):
                        identify_token(char='while', linha=linhaAtual, tokenList=tokenList)
                        i += 4

    elif (code_string[i] == 't'):
        if (code_string[i + 1] == 'r'):
            if (code_string[i + 2] == 'u'):
                if (code_string[i + 3] == 'e'):
                    identify_token(char='true', linha=linhaAtual, tokenList=tokenList)
                    i += 3
        
    elif (code_string[i] == '\n'):
        linhaAtual += 1

    i += 1

print(tokenList)
