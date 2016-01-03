#!/usr/bin/env python3
# http://adventofcode.com/day/21

import collections
import copy
import itertools


class Player:
    def __init__(self, name, hit, damage, armor):
        self.name = name
        self.hit = hit
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return "{0.name}: {0.damage} damage, {0.armor} armor, {0.hit} hit points".format(self)

    def defend(self, other):
        self.hit -= max(1, other.damage - self.armor)

    def dead(self):
        return self.hit <= 0


def play(you, boss, show=None):
    if show is None:
        show = lambda s: None
    show(you)
    show(boss)
    while True:
        boss.defend(you)
        show(boss)
        if boss.dead():
            return you

        you.defend(boss)
        show(you)
        if you.dead():
            return boss

test_you = Player("you", 8, 5, 5)
test_boss = Player("boss", 12, 7, 2)

winner = play(test_you, test_boss, print)
print("winner is {}".format(winner))


Thing = collections.namedtuple("Thing", "name cost damage armor")

WEAPONS = [
    # Weapons:          Cost  Damage  Armor
    Thing('Dagger',        8,     4,    0),
    Thing('Shortsword',   10,     5,    0),
    Thing('Warhammer',    25,     6,    0),
    Thing('Longsword',    40,     7,    0),
    Thing('Greataxe',     74,     8,    0),
]

ARMOR = [
    # Armor:            Cost  Damage  Armor
    Thing('Leather',      13,     0,       1),
    Thing('Chainmail',    31,     0,       2),
    Thing('Splintmail',   53,     0,       3),
    Thing('Bandedmail',   75,     0,       4),
    Thing('Platemail',   102,     0,       5),
]

RINGS = [
    # Rings:            Cost  Damage  Armor
    Thing('Damage +1',    25,     1,       0),
    Thing('Damage +2',    50,     2,       0),
    Thing('Damage +3',   100,     3,       0),
    Thing('Defense +1',   20,     0,       1),
    Thing('Defense +2',   40,     0,       2),
    Thing('Defense +3',   80,     0,       3),
]

def inventories():
    """Produces possible inventories of stuff."""
    # OK: this turned out really weird....

    # Choose one weapon.
    weapons = itertools.chain.from_iterable(
        itertools.combinations(WEAPONS, n) for n in range(1, 2)
    )
    # Choose one armor, or no armor.
    armor = itertools.chain.from_iterable(
        itertools.combinations(ARMOR, n) for n in range(0, 2)
    )
    # Choose 0-2 rings.
    rings = itertools.chain.from_iterable(
        itertools.combinations(RINGS, n) for n in range(0, 3)
    )

    return map(
        lambda inv: list(inv[0]+inv[1]+inv[2]),
        itertools.product(weapons, armor, rings)
    )


def players(name, hit, inventories):
    """Produces (spent, Player) values from inventories."""
    for inv in inventories:
        spent = sum(i.cost for i in inv)
        player = Player(
            name,
            hit,
            damage=sum(i.damage for i in inv),
            armor=sum(i.armor for i in inv),
        )
        yield spent, player


def outcomes(boss, hit, inventories):
    """Produces (spent, Player) values that win against boss."""
    boss_template = boss
    for spent, you in players("You", hit, inventories):
        boss = copy.copy(boss_template)
        winner = play(you, boss)
        yield spent, you, winner is you


def winning_players(boss, hit, inventories):
    return ((spent, you) for spent, you, outcome in outcomes(boss, hit, inventories) if outcome is True)

def losing_players(boss, hit, inventories):
    return ((spent, you) for spent, you, outcome in outcomes(boss, hit, inventories) if outcome is False)

print("Part 1:")
boss = Player("boss", hit=104, damage=8, armor=1)
spent, best = min(winning_players(boss, 100, inventories()))
print("Minimum gold is {}, for this player: {}".format(spent, best))

print("Part 2:")
spent, worst = max(losing_players(boss, 100, inventories()))
print("Maximum gold is {}, for this player: {}".format(spent, worst))
