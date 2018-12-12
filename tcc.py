#!/usr/bin/env python3

import argparse
import re
import os
from c_compiler.lexer import lex
from c_compiler.parser import parse
from c_compiler.generator import generate

def determine_assembly_filename(args):
    """Determine default file name for assembly output."""
    # Swap .c with .S
    m = re.search("(.*)\.[cC]", args.source_file)
    if m:
        return m.group(1) + '.S'

    # Last resort, append .S
    return args.source_file + '.S'

def determine_executable_filename(args):
    """Determine default file name for ELF output."""
    if args.o:
        return args.o

    # Swap .c with .S
    m = re.search("(.*)\.[cC]", args.source_file)
    if m:
        return m.group(1)

    # Last resort, append .S
    return 'a.out'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', help='C file to compile')
    parser.add_argument('-o', help='output assembly file', metavar='output_file')

    args = parser.parse_args()

    with open(args.source_file, 'r') as f:
        tokens = lex(f.read())

    ast = parse(tokens)

    asm_file = determine_assembly_filename(args)
    generate(ast, asm_file)

    os.system('gcc -m32 {} -o {}'.format(asm_file, determine_executable_filename(args)))
    os.system('rm {}'.format(asm_file))

if __name__ == "__main__":
    main()
