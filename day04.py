#!/usr/bin/env python3
# http://adventofcode.com/day/4

import hashlib
import itertools


def find_zeroes(key, nzeros):
    for i in itertools.count():
        md5 = hashlib.md5((key + str(i)).encode("ascii")).hexdigest()
        if md5.startswith("0"*nzeros):
            return i

for key in ["abcdef", "pqrstuv"]:
    print("Test: {!r} --> {}".format(key, find_zeroes(key, 5)))

print("Answer: {!r} --> {}".format("bgvyzdsv", find_zeroes("bgvyzdsv", 5)))
print("Answer: {!r} --> {}".format("bgvyzdsv", find_zeroes("bgvyzdsv", 6)))
