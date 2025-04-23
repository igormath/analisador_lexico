def read_external_code():
    byte_list = []
    try:
        with open('test.clite', "rb") as f:
            byte = f.read(1)
            while byte:
                byte_list.append(byte[0])
                byte = f.read(1)
        return byte_list
    except FileNotFoundError:
        print('Erro. Arquivo não encontrado.')
        return None
