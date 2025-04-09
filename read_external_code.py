def read_external_code(code_string):
    with open('test.clite', 'r') as fh:
        for line in fh:
            code_string += line
    return code_string
