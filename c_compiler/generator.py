from c_compiler import ast_data_structures, symbols

def generate_binary_operator(expression, symbol_table, f):
    generate_expression(expression.expression2, symbol_table, f)
    f.write("push    %rax\n")
    generate_expression(expression.expression1, symbol_table, f)

    operation = expression.operation
    if operation == "logical_or":
        symbol = symbol_table.create_symbol("_logical_or_")
        end_symbol = symbol_table.create_symbol("_logical_or_end_")

        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("cmpq    $0, %rcx\n") # Set ZF if RCX == 0
        f.write("je      {}\n".format(symbol)) # If ZF set, go to symbol
        f.write("movq    $1, %rax\n") # Evaluate true
        f.write("jmp     {}\n".format(end_symbol)) # Short circuit
        f.write("{}:\n".format(symbol)) # Evaluate e2
        f.write("cmpq    $0, %rax\n") # Set ZF if RAX == 0
        f.write("movq    $0, %rax\n") # Zero RAX without tampering with MOVQ
        f.write("setne   %al\n") # Set AL register if e2 != 0
        f.write("{}:\n".format(end_symbol)) # Symbol to skip e2
    elif operation == "logical_and":
        symbol = symbol_table.create_symbol("_logical_and_")
        end_symbol = symbol_table.create_symbol("_logical_and_end_")

        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("cmpq    $0, %rcx\n") # Set ZF if RCX == 0
        f.write("jne      {}\n".format(symbol)) # If ZF not set, go to symbol
        f.write("movq    $0, %rax\n") # Evaluate False
        f.write("jmp     {}\n".format(end_symbol)) # Short circuit
        f.write("{}:\n".format(symbol)) # Evaluate e2
        f.write("cmpq    $0, %rax\n") # Set ZF if RAX == 0
        f.write("movq    $0, %rax\n") # Zero RAX without tampering with MOVQ
        f.write("setne   %al\n") # Set AL register if e2 != 0
        f.write("{}:\n".format(end_symbol)) # Symbol to skip e2
    elif operation == 'equal_comparison':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("cmpq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("sete    %al\n")
    elif operation == 'not_equal_comparison':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("cmpq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("setne   %al\n")
    elif operation == 'less_than':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("subq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("setg    %al\n")
    elif operation == 'less_than_or_equal':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("subq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("setge   %al\n")
    elif operation == 'greater_than':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("subq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("setl    %al\n")
    elif operation == 'greater_than_or_equal':
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("subq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX
        f.write("setle   %al\n")
    elif operation == 'negation':
        f.write("pop     %rcx\n")
        f.write("subq    %rcx, %rax\n")
    elif operation == 'addition_operator':
        f.write("pop     %rcx\n")
        f.write("addq    %rcx, %rax\n")
    elif operation == 'multiplication_operator':
        f.write("pop     %rcx\n")
        f.write("imul    %rcx, %rax\n")
    elif operation == 'division_operator':
        f.write("pop     %rcx\n") # e2 to RCX
        f.write("cqto\n")
        f.write("idivq   %rcx\n")

def generate_expression(expression, symbol_table, f):
    if isinstance(expression, ast_data_structures.UnaryOperator):
        generate_expression(expression.expression, symbol_table, f)

        if expression.operator == 'negation':
            f.write("neg     %rax\n")
        elif expression.operator == 'bitwise_complement':
            f.write("not     %rax\n")
        elif expression.operator == 'logical_negation':
            f.write("cmpq    $0, %rax\n")
            f.write("movq    $0, %rax\n")
            f.write("sete    %al\n")
    elif isinstance(expression, ast_data_structures.BinaryOperator):
        generate_binary_operator(expression, symbol_table, f)
    elif isinstance(expression, ast_data_structures.Constant):
        f.write("movq    ${}, %rax\n".format(expression.integer))

def generate_statement(statement, symbol_table, f):
    # TODO: Currently assuming return statement

    generate_expression(statement.expression, symbol_table, f)

    f.write("ret\n")

def generate_function(function, symbol_table, f):
    label = function.name

    # macOS
    f.write(".globl _{}\n".format(label))
    f.write("_{}:\n".format(label))

    # Debian WSL
    f.write(".globl {}\n".format(label))
    f.write("{}:\n".format(label))

    # TODO: Generate all body statements
    generate_statement(function.statement, symbol_table, f)

def generate_program(program, symbol_table, f):
    # TODO: Generate all functions
    generate_function(program.function_declaration, symbol_table, f)

    # TODO: Goto main?

def generate(ast, output_file):
    symbol_table = symbols.Symbols()

    with open(output_file, 'w') as f:
        generate_program(ast, symbol_table, f)
