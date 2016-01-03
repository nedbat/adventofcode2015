#!/usr/bin/env python3
# http://adventofcode.com/day/24

from functools import reduce
from itertools import combinations

TEST_PACKAGES = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]

PACKAGES = [
    1, 2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
]


def choice_rest(items):
    for i in range(len(items)):
        yield items[i], items[i+1:]

class SummedCombos:
    def __init__(self, seq, target_sum, max_len, shortest=False):
        self.seq = seq
        self.target_sum = target_sum
        self.max_len = max_len
        self.shortest = shortest

    def __iter__(self):
        return self._work(self.seq, [])

    def _work(self, remaining, so_far):
        if len(so_far) > self.max_len:
            return

        total = sum(so_far)
        if total == self.target_sum:
            if self.shortest:
                self.max_len = len(so_far)
            yield so_far
            return
        elif total > self.target_sum:
            return

        for choice, rest in choice_rest(remaining):
            for answer in self._work(rest, so_far + [choice]):
                yield answer


def equal_thirds(packages):
    # Work from largest to smallest.  Since we clip off searching when g1 is
    # larger than a previous g1, it helps to find the smallest g1 first, and
    # we do that by using the biggest packages in g1.
    packages = sorted(packages, reverse=True)
    min_g1_size = len(packages)
    min_qe = product(packages)

    third = sum(packages) // 3
    max_g1_size = len(packages) // 3
    for g1 in SummedCombos(packages, third, max_g1_size, shortest=True):
        qe = product(g1)
        if qe > min_qe:
            continue
        min_qe = min(min_qe, qe)

        rest = [p for p in packages if p not in g1]
        for g2 in SummedCombos(rest, third, max_g1_size):
            answer = g1, g2, [p for p in rest if p not in g2]
            print(answer)
            yield answer
            # We don't need all the different combinations of g2 and g3, one
            # will do.
            break

def equal_fourths(packages):
    # Work from largest to smallest.  Since we clip off searching when g1 is
    # larger than a previous g1, it helps to find the smallest g1 first, and
    # we do that by using the biggest packages in g1.
    packages = sorted(packages, reverse=True)
    min_g1_size = len(packages)
    min_qe = product(packages)

    fourth = sum(packages) // 4
    max_g1_size = len(packages)
    for g1 in SummedCombos(packages, fourth, max_g1_size, shortest=True):
        qe = product(g1)
        if qe > min_qe:
            continue
        min_qe = min(min_qe, qe)

        yielded = False
        rest = [p for p in packages if p not in g1]
        for g2 in SummedCombos(rest, fourth, max_g1_size):
            rest2 = [p for p in rest if p not in g2]
            for g3 in SummedCombos(rest2, fourth, max_g1_size):
                answer = g1, g2, g3, [p for p in rest2 if p not in g3]
                print(answer)
                yield answer
                yielded = True
                # We don't need all the different combinations of g2 and g3, one
                # will do.
                break
            if yielded:
                break

def product(seq):
    return reduce(lambda a, b: a * b, seq, 1)

def rating(groups):
    return len(groups[0]), product(groups[0])

def best_packing(packages):
    best = min(equal_thirds(packages), key=rating)
    g1_size, qe = rating(best)
    return best, qe

print("Test:")
best, qe = best_packing(TEST_PACKAGES)
print("Best packing is {}, QE={}".format(best, qe))

print("Part 1:")
best, qe = best_packing(PACKAGES)
print("Best packing is {}, QE={}".format(best, qe))

def best_packing4(packages):
    best = min(equal_fourths(packages), key=rating)
    g1_size, qe = rating(best)
    return best, qe

print("Part 2:")
best, qe = best_packing4(PACKAGES)
print("Best packing is {}, QE={}".format(best, qe))
