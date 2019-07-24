from c_compiler import ast_data_structures

def generate_factor(factor, f):
    if isinstance(factor, ast_data_structures.UnaryOperator):
        generate_expression(factor.expression, f)

        if factor.operator == 'negation':
            f.write("neg     %eax\n")
        elif factor.operator == 'bitwise_complement':
            f.write("not     %eax\n")
        elif factor.operator == 'logical_negation':
            f.write("cmpl    $0, %eax\n")
            f.write("movl    $0, %eax\n")
            f.write("sete    %al\n")
    elif isinstance(factor, ast_data_structures.Expression):
        generate_expression(factor, f)
    elif isinstance(factor, ast_data_structures.Constant):
        f.write("movl    ${}, %eax\n".format(factor.integer))

def generate_term(term, f):
    operations = iter(term.operations)

    for factor in term.factors:
        generate_factor(factor, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in term.operations:
        f.write("pop     %rcx\n")
        if operation == 'negation':
            # TODO: Tighten up subtraction
            f.write("neg     %eax\n")
        f.write("addl    %ecx, %eax\n")

def generate_expression(expression, f):
    operations = iter(expression.operations)

    for term in expression.terms:
        generate_term(term, f)

        try:
            op = next(operations)
            f.write("push    %rax\n")
        except StopIteration:
            pass

    for operation in term.operations:
        if operation == 'multiplication_operator':
            f.write("pop     %rcx\n")
            f.write("imul    %ecx, %eax\n")
        elif operation == 'division_operator':
            # TODO: Tighten up
            f.write("pop     %rdx\n") # e1 to EDX
            f.write("movl    %eax, %ecx\n") # e2 to ECX
            f.write("movl    %edx, %eax\n") # e1 to EAX
            f.write("movl    $0, %edx\n") # Zero EDX
            f.write("idivl   %ecx\n")

def generate_statement(statement, f):
    # TODO: Currently assuming return statement

    generate_expression(statement.expression, f)

    f.write("ret\n")

def generate_function(function, f):
    label = function.name

    f.write(".globl _{}\n".format(label))
    f.write("_{}:\n".format(label))

    # TODO: Generate all body statements
    generate_statement(function.statement, f)

def generate_program(program, f):
    # TODO: Generate all functions
    generate_function(program.function_declaration, f)

    # TODO: Goto main?

def generate(ast, output_file):
    with open(output_file, 'w') as f:
        generate_program(ast, f)
