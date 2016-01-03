#!/usr/bin/env python3
# http://adventofcode.com/day/12

import json

def sum_numbers(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum(sum_numbers(x) for x in obj)
    elif isinstance(obj, dict):
        return sum(sum_numbers(v) for v in obj.values())
    else:
        return 0

TESTS = """\
    [1,2,3]
    {"a":2,"b":4}
    [[[3]]]
    {"a":{"b":4},"c":-1}
    {"a":[-1,1]}
    [-1,{"a":1}]
    []
    {}
"""

for test in TESTS.splitlines():
    test = test.strip()
    print("Sum of {} is {}".format(test, sum_numbers(json.loads(test))))

with open("day12_input.txt") as input_txt:
    INPUT = input_txt.read()

print("Answer is {}".format(sum_numbers(json.loads(INPUT.strip()))))

print()
print("Part 2")

def sum_numbers_no_red(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum(sum_numbers_no_red(x) for x in obj)
    elif isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        else:
            return sum(sum_numbers_no_red(v) for v in obj.values())
    else:
        return 0

TESTS = """\
    [1,2,3]
    [1,{"c":"red","b":2},3]
    {"d":"red","e":[1,2,3,4],"f":5}
    [1,"red",5]
"""

for test in TESTS.splitlines():
    test = test.strip()
    print("Sum of {} is {}".format(test, sum_numbers_no_red(json.loads(test))))

print("Answer is {}".format(sum_numbers_no_red(json.loads(INPUT.strip()))))
