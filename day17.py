#!/usr/bin/env python3
# http://adventofcode.com/day/17

INPUT = """
33
14
18
20
45
35
16
35
1
13
18
13
50
44
48
6
24
41
30
42
"""

containers = list(map(int, INPUT.split()))

def combos_summing_to(containers, total, so_far=[]):
    if total == 0:
        yield so_far
        return
    if sum(containers) < total:
        return
    if not containers:
        return
    yield from combos_summing_to(containers[1:], total - containers[0], so_far + [containers[0]])
    yield from combos_summing_to(containers[1:], total, so_far)

print("Test:")
print(list(combos_summing_to([20, 15, 10, 5, 5], 25)))
print("Part 1:")
print("Answer: {}".format(len(list(combos_summing_to(containers, 150)))))

import collections

by_num_containers = collections.defaultdict(list)
for combos in combos_summing_to(containers, 150):
    by_num_containers[len(combos)].append(combos)

min_required = min(by_num_containers)
print("Part 2:")
print("Answer: {} containers are needed, and there are {} ways".format(min_required, len(by_num_containers[min_required])))
