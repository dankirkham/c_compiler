def generate_expression(expression, f):
    f.write("movl    ${}, %eax\n".format(expression.integer))

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
