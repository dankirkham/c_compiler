#!/usr/bin/env bash

DIR=write_a_c_compiler
EXE_FILE=${1%.*}
ASM_FILE=${EXE_FILE}.S

# Compile
cd ..
python3.5 -m c_compiler $DIR/$1

# Assemble
gcc -m64 $DIR/$ASM_FILE -o $DIR/$EXE_FILE
rm $DIR/$ASM_FILE

# Make Executeable
chmod +x $DIR/$EXE_FILE
