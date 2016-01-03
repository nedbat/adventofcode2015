#!/usr/bin/env python3
# http://adventofcode.com/day/14

INPUT = """\
Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
"""

import collections
import re

Reindeer = collections.namedtuple("Reindeer", "name, speed, fly, rest")

def parse_input(inp):
    reindeer = []
    for line in inp.splitlines():
        match = re.search(r"^(\w+) .* (\d+) .* (\d+) .* (\d+) ", line)
        if not match:
            raise Exception("Buh!? {!r}".format(line))
        name, speed, fly, rest = match.groups()
        reindeer.append(Reindeer(name, int(speed), int(fly), int(rest)))
    return reindeer


def distance(reindeer, seconds):
    """Closed-form calculation, good for part 1."""
    cycle = (reindeer.fly + reindeer.rest)
    full_cycles = seconds // cycle
    remainder = seconds % cycle
    remainder_flying_time = min(remainder, reindeer.fly)
    full_cycle_distance = full_cycles * reindeer.fly * reindeer.speed
    remainder_distance = remainder_flying_time * reindeer.speed
    return full_cycle_distance + remainder_distance


print("Test: Comet goes {}".format(distance(Reindeer("Comet", 14, 10, 127), 1000)))
print("Test: Dancer goes {}".format(distance(Reindeer("Dancer", 16, 11, 162), 1000)))

reindeer = parse_input(INPUT)
farthest = max(distance(r, 2503) for r in reindeer)
print("Part 1: {} km".format(farthest))

class FlyingReindeer:
    def __init__(self, reindeer):
        self.reindeer = reindeer
        self.flying = False
        self.remaining = 0
        self.distance = 0
        self.points = 0

    def __str__(self):
        return self.reindeer.name

    def start(self):
        self.flying = True
        self.remaining = self.reindeer.fly

    def scooch(self):
        """Adjust the deer by one second."""
        if self.flying:
            self.distance += self.reindeer.speed

        # One second gone, maybe we transition state?
        self.remaining -= 1
        if self.remaining == 0:
            self.flying = not self.flying
            self.remaining = self.reindeer.fly if self.flying else self.reindeer.rest


def race(reindeer, seconds):
    flying_deer = [FlyingReindeer(r) for r in reindeer]

    # Init them.
    for fd in flying_deer:
        fd.start()

    for sec in range(seconds):
        # Move the deer forward.
        for fd in flying_deer:
            fd.scooch()

        # Who is in the lead?
        farthest = max(fd.distance for fd in flying_deer)
        for fd in filter(lambda fd: fd.distance == farthest, flying_deer):
            fd.points += 1

    winner = max(flying_deer, key=lambda fd: fd.points)
    return winner

winner = race(reindeer, 2503)
print("{0} wins with {0.points} points".format(winner))
