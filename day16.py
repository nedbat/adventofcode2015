#!/usr/bin/env python3
# http://adventofcode.com/day/16


def parse_input(inp):
    aunts = {}
    for line in inp:
        name, _, compounds = line.partition(':')
        aunts[name] = {}
        for compound in compounds.split(','):
            compound = compound.strip()
            cname, _, amt = compound.partition(':')
            aunts[name][cname] = int(amt)

    return aunts

def find_matches(criteria, aunts, compares={}):
    for aname, aunt in aunts.items():
        for k, v in criteria.items():
            compare = compares.get(k, lambda a, c: a == c)
            if k in aunt and not compare(aunt[k], v):
                break
        else:
            yield aname, aunt


CRITERIA = dict(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1,
)

with open("day16_input.txt") as f:
    aunts = parse_input(f)

print(list(find_matches(CRITERIA, aunts)))

COMPARES = dict(
    cats=(lambda a, c: a > c),
    trees=(lambda a, c: a > c),
    pomeranians=(lambda a, c: a < c),
    goldfish=(lambda a, c: a < c),
)

print(list(find_matches(CRITERIA, aunts, COMPARES)))
