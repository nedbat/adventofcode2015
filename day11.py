#!/usr/bin/env python3
# http://adventofcode.com/day/11

import re

def is_straight(s):
    """Does s consist of increasing consecutive letters?"""
    for a, b in zip(s, s[1:]):
        if ord(b) - ord(a) != 1:
            return False
    return True

assert is_straight("abc")
assert not is_straight("abd")
assert not is_straight("acd")

def is_good(password):
    """Is this a good password?"""

    # Passwords may not contain the letters i, o, or l, as these letters can be
    # mistaken for other characters and are therefore confusing.
    if any(c in password for c in "iol"):
        return False

    # Passwords must include one increasing straight of at least three letters,
    # like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd
    # doesn't count.
    for i in range(len(password)-3):
        if is_straight(password[i:i+3]):
            break
    else:
        return False

    # Passwords must contain at least two different, non-overlapping pairs of
    # letters, like aa, bb, or zz.
    if len(re.findall(r"(.)\1", password)) < 2:
        return False

    return True

assert not is_good("hijklmmn")
assert not is_good("abbceffg")
assert not is_good("abbcegjk")
assert is_good("abcdffaa")
assert is_good("ghjaabcc")

def next_string(s):
    """Increment a string"""
    if s[-1] == "z":
        return next_string(s[:-1]) + "a"
    else:
        return s[:-1] + chr(ord(s[-1])+1)

assert next_string("abc") == "abd"
assert next_string("azz") == "baa"

def next_password(password):
    """Find the next valid password."""
    while True:
        password = next_string(password)
        if is_good(password):
            return password

print("Finding next password after abcdefgh")
assert next_password("abcdefgh") == "abcdffaa"
print("Finding next password after ghijklmn")
assert next_password("ghijklmn") == "ghjaabcc"

nextp = next_password("cqjxjnds")
print("Answer: next password after cqjxjnds is {}".format(nextp))
print("Answer: and then the next is {}".format(next_password(nextp)))
