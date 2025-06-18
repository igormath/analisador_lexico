class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, *args):
        self.code.append(args)

    def __str__(self):
        output = []
        for instruction in self.code:
            if instruction[0].startswith('L') and len(instruction) == 1:
                 output.append(f"{instruction[0]}:")
            else:
                 output.append(f"    {instruction}")
        return "\n".join(output)
