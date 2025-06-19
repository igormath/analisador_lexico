def write_intermediate_code(intermediate_code_generator_str):
    with open('intermediate_code.txt', 'w', encoding='utf-8') as f:
                f.write(str(intermediate_code_generator_str))
            
    print("Código intermediário salvo em 'intermediate_code.txt'")
