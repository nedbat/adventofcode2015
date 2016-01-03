#!/usr/bin/env python3
# http://adventofcode.com/day/10

import itertools

def look_and_say(s):
    result = []
    for digit, seq in itertools.groupby(s):
        result.append(str(len(list(seq))))
        result.append(digit)
    return "".join(result)

CONWAY = 1.303577269034296

def repeat_look_and_say(s, n):
    print("Starting with {}".format(s))
    last_len = len(s)
    for i in range(n):
        s = look_and_say(s)
        print("After {} iterations, length is {}, starting with {:.50}".format(i+1, len(s), s))
        ratio = len(s) / last_len
        print("  ratio is {}, off by {}".format(ratio, CONWAY - ratio))
        last_len = len(s)
    return s

print("Answer is {}".format(len(repeat_look_and_say("3113322113", 50))))
