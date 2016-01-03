#!/usr/bin/env python3
# http://adventofcode.com/day/25

def sequence_number(row, col):
    """Compute the zero-based sequence number from the zero-based row and col."""
    tri_row = row + col
    row_start_value = (tri_row * tri_row + tri_row) // 2
    delta_in_row = col if tri_row % 2 else row
    return row_start_value + delta_in_row

for row in range(10):
    for col in range(10):
        print("{:4d}".format(sequence_number(row, col)), end="")
    print()

CODE0 = 20151125
CODE_MULT = 252533
CODE_MOD = 33554393

def code_value(n):
    return (CODE0 * pow(CODE_MULT, n, CODE_MOD)) % CODE_MOD

for row in range(6):
    for col in range(6):
        print("{:10d}".format(code_value(sequence_number(row, col))), end="")
    print()

# To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019.

print("Part 1: {}".format(code_value(sequence_number(3009, 3018))))
