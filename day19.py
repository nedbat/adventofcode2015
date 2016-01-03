#!/usr/bin/env python3
# http://adventofcode.com/day/19

import itertools
import re
import time

def read_input(inp):
    """Returns a list of pairs (replacements) and the medicine string."""
    replacements = []
    for line in inp:
        line = line.strip()
        if not line:
            continue
        if "=>" in line:
            before, _, after = line.partition(" => ")
            replacements.append((before, after))
        else:
            medicine = line

    return replacements, medicine

with open("day19_input2.txt") as inp:
    replacements, medicine = read_input(inp)

def molecules(molecule, replacements):
    for before, after in replacements:
        for match in re.finditer(before, molecule):
            start, end = match.span()
            new_molecule = molecule[:start] + after + molecule[end:]
            yield new_molecule

TEST_INPUT = """\
H => HO
H => OH
O => HH

HOH
"""

test_replacements, test_medicine = read_input(TEST_INPUT.splitlines())

print("Part 1:")
all_molecules = set(molecules(test_medicine, test_replacements))
print("Test: {} distinct molecules".format(len(all_molecules)))

all_molecules = set(molecules(medicine, replacements))
print("Answer: {} distinct molecules".format(len(all_molecules)))

def find_target(molecule, replacements, target):
    steps = 0
    soup = set([molecule])
    for step in itertools.count():
        soup = set(itertools.chain.from_iterable(molecules(mol, replacements) for mol in soup))
        print("  step {:3d}: {} molecules, avg len {:.1f}".format(step, len(soup), sum(len(m) for m in soup) / len(soup)))
        if target in soup:
            return step

BACKTRACKS = 0

def find_target2(molecule, replacements, target, steps=0):
    if molecule == target:
        #print("FOUND: {} steps".format(len(steps)))
        yield steps
        return
    for new_molecule in molecules(molecule, replacements):
        for steps2 in find_target2(new_molecule, replacements, target, steps+1):
            yield steps2

backward_replacements = [(after, before) for before, after in replacements]
print("Part 2:")
if 0:   # too slow
    print("time: {}".format(time.time()))
    print("{} steps (backward)".format(find_target(medicine, backward_replacements, "e")))
    print("time: {}".format(time.time()))
    print("{} steps (forward)".format(find_target("e", replacements, medicine)))
    print("time: {}".format(time.time()))

descending = sorted(replacements, key=lambda bef_aft: len(bef_aft[1]), reverse=True)
backwards_descending = [(after, before) for before, after in descending]
print("{} steps".format(next(find_target2(medicine, backwards_descending, "e"))))
