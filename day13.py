#!/usr/bin/env python3
# http://adventofcode.com/day/13

import collections
import itertools
import re

INPUT = """\
Alice would lose 2 happiness units by sitting next to Bob.
Alice would lose 62 happiness units by sitting next to Carol.
Alice would gain 65 happiness units by sitting next to David.
Alice would gain 21 happiness units by sitting next to Eric.
Alice would lose 81 happiness units by sitting next to Frank.
Alice would lose 4 happiness units by sitting next to George.
Alice would lose 80 happiness units by sitting next to Mallory.
Bob would gain 93 happiness units by sitting next to Alice.
Bob would gain 19 happiness units by sitting next to Carol.
Bob would gain 5 happiness units by sitting next to David.
Bob would gain 49 happiness units by sitting next to Eric.
Bob would gain 68 happiness units by sitting next to Frank.
Bob would gain 23 happiness units by sitting next to George.
Bob would gain 29 happiness units by sitting next to Mallory.
Carol would lose 54 happiness units by sitting next to Alice.
Carol would lose 70 happiness units by sitting next to Bob.
Carol would lose 37 happiness units by sitting next to David.
Carol would lose 46 happiness units by sitting next to Eric.
Carol would gain 33 happiness units by sitting next to Frank.
Carol would lose 35 happiness units by sitting next to George.
Carol would gain 10 happiness units by sitting next to Mallory.
David would gain 43 happiness units by sitting next to Alice.
David would lose 96 happiness units by sitting next to Bob.
David would lose 53 happiness units by sitting next to Carol.
David would lose 30 happiness units by sitting next to Eric.
David would lose 12 happiness units by sitting next to Frank.
David would gain 75 happiness units by sitting next to George.
David would lose 20 happiness units by sitting next to Mallory.
Eric would gain 8 happiness units by sitting next to Alice.
Eric would lose 89 happiness units by sitting next to Bob.
Eric would lose 69 happiness units by sitting next to Carol.
Eric would lose 34 happiness units by sitting next to David.
Eric would gain 95 happiness units by sitting next to Frank.
Eric would gain 34 happiness units by sitting next to George.
Eric would lose 99 happiness units by sitting next to Mallory.
Frank would lose 97 happiness units by sitting next to Alice.
Frank would gain 6 happiness units by sitting next to Bob.
Frank would lose 9 happiness units by sitting next to Carol.
Frank would gain 56 happiness units by sitting next to David.
Frank would lose 17 happiness units by sitting next to Eric.
Frank would gain 18 happiness units by sitting next to George.
Frank would lose 56 happiness units by sitting next to Mallory.
George would gain 45 happiness units by sitting next to Alice.
George would gain 76 happiness units by sitting next to Bob.
George would gain 63 happiness units by sitting next to Carol.
George would gain 54 happiness units by sitting next to David.
George would gain 54 happiness units by sitting next to Eric.
George would gain 30 happiness units by sitting next to Frank.
George would gain 7 happiness units by sitting next to Mallory.
Mallory would gain 31 happiness units by sitting next to Alice.
Mallory would lose 32 happiness units by sitting next to Bob.
Mallory would gain 95 happiness units by sitting next to Carol.
Mallory would gain 91 happiness units by sitting next to David.
Mallory would lose 66 happiness units by sitting next to Eric.
Mallory would lose 75 happiness units by sitting next to Frank.
Mallory would lose 99 happiness units by sitting next to George.
"""

def parse_input(inp):
    """Return a dict mapping pairs of strings to an int."""
    people = set()
    prefs = collections.defaultdict(int)
    for line in inp.splitlines():
        match = re.search(r"^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).$", line)
        if not match:
            raise Exception("Huh? {!r}".format(line))
        left, gain_lose, delta, right = match.groups()
        people.add(left)
        people.add(right)

        happiness_delta = int(delta)
        if gain_lose == "lose":
            happiness_delta *= -1
        prefs[left, right] = happiness_delta
    return people, prefs


def circular_pairs(seq):
    """Generate all the adjacent pairs, including wrapping around end to beginning."""
    for left, right in zip(seq, seq[1:]):
        yield left, right
    yield seq[-1], seq[0]


def total_happiness(seating, prefs):
    """Calculate the total happiness for a particular seating."""
    happiness = 0
    for left, right in circular_pairs(seating):
        happiness += prefs[left, right] + prefs[right, left]
    return happiness


def circular_permutations(seq):
    """Permute seq, but don't include permutations that are the same circularly."""
    seq = list(seq)
    for perm_rest in itertools.permutations(seq[1:]):
        yield seq[:1] + list(perm_rest)


def seatings(people, prefs):
    """Generate all the possible seatings as pairs (happiness, seating)."""
    for seating in circular_permutations(people):
        yield total_happiness(seating, prefs), seating

def best_seating(people, prefs):
    """Find the best seating, returns (happiness, seating)."""
    return max(seatings(people, prefs))


people, prefs = parse_input(INPUT)
print("Part one: {}".format(best_seating(people, prefs)))
people.add("Me")
print("Part two: {}".format(best_seating(people, prefs)))
