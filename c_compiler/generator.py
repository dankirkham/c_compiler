from c_compiler import ast_data_structures

def generate_factor(factor, f):
    if isinstance(factor, ast_data_structures.UnaryOperator):
        generate_factor(factor.factor, f)

        if factor.operator == 'negation':
            f.write("neg     %rax\n")
        elif factor.operator == 'bitwise_complement':
            f.write("not     %rax\n")
        elif factor.operator == 'logical_negation':
            f.write("cmpq    $0, %rax\n")
            f.write("movq    $0, %rax\n")
            f.write("sete    %al\n")
    elif isinstance(factor, ast_data_structures.Expression):
        generate_expression(factor, f)
    elif isinstance(factor, ast_data_structures.Constant):
        f.write("movq    ${}, %rax\n".format(factor.integer))

def generate_term(term, f):
    operations = reversed(term.operations)

    for factor in reversed(term.factors):
        generate_factor(factor, f)

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
            f.write("movq    $0, %rdx\n") # Zero RDX
            f.write("cqto\n")
            f.write("idivq   %rcx\n")
            f.write("movq    %rcx, %rax\n") # Move answer to RAX

def generate_expression(expression, f):
    operations = reversed(expression.operations)

    for term in reversed(expression.terms):
        generate_term(term, f)

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

def generate_statement(statement, f):
    # TODO: Currently assuming return statement

    generate_expression(statement.expression, f)

    f.write("ret\n")

def generate_function(function, f):
    label = function.name

    # macOS
    f.write(".globl _{}\n".format(label))
    f.write("_{}:\n".format(label))

    # Debian WSL
    f.write(".globl {}\n".format(label))
    f.write("{}:\n".format(label))

    # TODO: Generate all body statements
    generate_statement(function.statement, f)

def generate_program(program, f):
    # TODO: Generate all functions
    generate_function(program.function_declaration, f)

    # TODO: Goto main?

def generate(ast, output_file):
    with open(output_file, 'w') as f:
        generate_program(ast, f)
