from c_compiler import ast_data_structures, symbols

def generate_factor(factor, symbol_table, f):
    if isinstance(factor, ast_data_structures.UnaryOperator):
        generate_factor(factor.factor, symbol_table, f)

        if factor.operator == 'negation':
            f.write("neg     %rax\n")
        elif factor.operator == 'bitwise_complement':
            f.write("not     %rax\n")
        elif factor.operator == 'logical_negation':
            f.write("cmpq    $0, %rax\n")
            f.write("movq    $0, %rax\n")
            f.write("sete    %al\n")
    elif isinstance(factor, ast_data_structures.Expression):
        generate_expression(factor, symbol_table, f)
    elif isinstance(factor, ast_data_structures.Constant):
        f.write("movq    ${}, %rax\n".format(factor.integer))

def generate_term(term, symbol_table, f):
    operations = reversed(term.operations)

    for factor in reversed(term.factors):
        generate_factor(factor, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(term.operations):
        if operation == 'multiplication_operator':
            f.write("pop     %rcx\n")
            f.write("imul    %rcx, %rax\n")
        elif operation == 'division_operator':
            f.write("pop     %rcx\n") # e2 to RCX
            f.write("cqto\n")
            f.write("idivq   %rcx\n")

def generate_additive_expression(expression, symbol_table, f):
    operations = reversed(expression.operations)

    for term in reversed(expression.terms):
        generate_term(term, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(expression.operations):
        f.write("pop     %rcx\n")
        if operation == 'negation':
            f.write("subq    %rcx, %rax\n")
        elif operation == 'addition_operator':
            f.write("addq    %rcx, %rax\n")

def generate_relational_expression(expression, symbol_table, f):
    operations = reversed(expression.operations)

    for additive_expression in reversed(expression.additive_expressions):
        generate_additive_expression(additive_expression, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(expression.operations):
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("subq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX

        if operation == 'less_than':
            f.write("setg    %al\n")
        elif operation == 'less_than_or_equal':
            f.write("setge   %al\n")
        elif operation == 'greater_than':
            f.write("setl    %al\n")
        elif operation == 'greater_than_or_equal':
            f.write("setle   %al\n")

def generate_equality_expression(expression, symbol_table, f):
    operations = reversed(expression.operations)

    for relational_expression in reversed(expression.relational_expressions):
        generate_relational_expression(relational_expression, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(expression.operations):
        f.write("pop     %rcx\n") # Move e1 to RCX
        f.write("cmpq    %rax, %rcx\n") # Subtract operands (e2 - e1)
        f.write("movq    $0, %rax\n") # Zero RAX

        if operation == 'equal_comparison':
            f.write("sete    %al\n")
        elif operation == 'not_equal_comparison':
            f.write("setne   %al\n")

def generate_logical_and_expression(expression, symbol_table, f):
    operations = reversed(expression.operations)

    for equality_expression in reversed(expression.equality_expressions):
        generate_equality_expression(equality_expression, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(expression.operations):
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

def generate_expression(expression, symbol_table, f):
    operations = reversed(expression.operations)

    for logical_and_expression in reversed(expression.logical_and_expressions):
        generate_logical_and_expression(logical_and_expression, symbol_table, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in reversed(expression.operations):
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
