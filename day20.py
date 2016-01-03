#!/usr/bin/env python3
# http://adventofcode.com/day/20

import itertools

def presents(house):
    total = 0
    for elf in range(1, house+1):
        if house % elf == 0:
            total += 10 * elf
    return total

print("Test:")
for house in range(1, 10):
    print("House {} got {} presents".format(house, presents(house)))

def run_elves(step, p_function, limit, guess_step):
    max_p = 1
    for house in itertools.count(step, step=step):
        p = p_function(house)
        if p > limit:
            print("Answer: House {} got {} presents".format(house, p))
            break
        if p > max_p:
            print("House {} got new max {} presents (/ {} == {:.3f}".format(house, p, guess_step, house/guess_step))
            max_p = p

print("Part 1:")
#run_elves(720, presents, 36000000)

def presents2(house):
    total = 0
    for elf in range(1, house+1):
        if house % elf == 0 and house // elf <= 50:
            total += 11 * elf
    return total

print("Part 2:")
run_elves(120, presents2, 36000000, guess_step=720)
