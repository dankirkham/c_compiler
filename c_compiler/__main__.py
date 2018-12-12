import argparse
import re
from c_compiler.lexer import lex
from c_compiler.parser import parse
from c_compiler.generator import generate

def determine_filename(args):
    """Determine default file name for assembly output."""
    if args.o:
        return args.o

    # Swap .c with .S
    m = re.search("(.*)\.[cC]", args.source_file)
    if m:
        return m.group(1) + '.S'

    # Last resort, append .S
    return args.source_file + '.S'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', help='C file to compile')
    parser.add_argument('-o', help='output assembly file', metavar='output_file')

    args = parser.parse_args()

    with open(args.source_file, 'r') as f:
        tokens = lex(f.read())

    print(tokens)
    ast = parse(tokens)
    generate(ast, determine_filename(args))

if __name__ == "__main__":
    main()
