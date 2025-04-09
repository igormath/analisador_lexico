code_string = ''
palavraAtual = ''
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
    elif (code_string[i] == 'i'):
        if (code_string[i+1] == 'n'):
            if (code_string[i+2] == 't'):
                identify_token(char='int', linha=linhaAtual, tokenList=tokenList)
                i += 2
    elif (code_string[i] == '\n'):
        linhaAtual += 1
    i += 1

print(tokenList)
 