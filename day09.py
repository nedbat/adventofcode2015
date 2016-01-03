#!/usr/bin/env python3
# http://adventofcode.com/day/9

import collections
import re

INPUT = """\
Faerun to Norrath = 129
Faerun to Tristram = 58
Faerun to AlphaCentauri = 13
Faerun to Arbre = 24
Faerun to Snowdin = 60
Faerun to Tambi = 71
Faerun to Straylight = 67
Norrath to Tristram = 142
Norrath to AlphaCentauri = 15
Norrath to Arbre = 135
Norrath to Snowdin = 75
Norrath to Tambi = 82
Norrath to Straylight = 54
Tristram to AlphaCentauri = 118
Tristram to Arbre = 122
Tristram to Snowdin = 103
Tristram to Tambi = 49
Tristram to Straylight = 97
AlphaCentauri to Arbre = 116
AlphaCentauri to Snowdin = 12
AlphaCentauri to Tambi = 18
AlphaCentauri to Straylight = 91
Arbre to Snowdin = 129
Arbre to Tambi = 53
Arbre to Straylight = 40
Snowdin to Tambi = 15
Snowdin to Straylight = 99
Tambi to Straylight = 70
"""

TEST = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

def segments(distances):
    for line in distances.splitlines():
        match = re.match(r"(\w+) to (\w+) = (\d+)", line)
        if not match:
            raise Exception("I don't understand: {!r}".format(line))
        yield match.group(1), match.group(2), int(match.group(3))

def distance_dict(segments):
    distances = collections.defaultdict(dict)
    for start, finish, distance in segments:
        distances[start][finish] = distance
        distances[finish][start] = distance
    return distances

def routes(distance_dict, visited=None, total=0):
    if visited is None:
        for start in distance_dict:
            yield from routes(distance_dict, [start], 0)
    elif len(visited) == len(distance_dict):
        yield visited, total
    else:
        for end, leg in distance_dict[visited[-1]].items():
            if end in visited:
                continue
            yield from routes(distance_dict, visited + [end], total + leg)

def find_a_route(input, criterion):
    return criterion(routes(distance_dict(segments(input))), key=lambda stops_total: stops_total[1])

def shortest_route(input):
    return find_a_route(input, min)

def longest_route(input):
    return find_a_route(input, max)

print("Shortest:")
print(shortest_route(TEST))
print(shortest_route(INPUT))

print("Longest:")
print(longest_route(TEST))
print(longest_route(INPUT))
