#!/usr/bin/env python3
# http://adventofcode.com/day/22

class Player:
    def __init__(self, name, hit, damage=0, armor=0, mana=0):
        self.name = name
        self.hit = hit
        self.damage = damage
        self.armor = armor
        self.mana = mana

    def __str__(self):
        return (
            "{0.name}: "
            "{0.damage} damage, "
            "{0.hit} hit points, "
            "{0.armor} armor, "
            "{0.mana} mana".format(self)
        )

    def defend(self, other):
        self.hit -= max(1, other.damage - self.armor)

    def dead(self):
        return self.hit <= 0


class Spell:
    duration = 0
    cost = 0

    def __init__(self):
        self.timer = 0
        self.active = False

    def cast(self, you, enemy):
        you.mana -= self.cost
        self.timer = self.duration
        self.active = True

    def apply(self, you, enemy):
        pass

class MagicMissile(Spell):
    """Magic Missile costs 53 mana. It instantly does 4 damage."""
    cost = 53

    def cast(self, you, enemy):
        enemy.hit -= 4

class Drain(Spell):
    """Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points."""
    cost = 73

    def cast(self, you, enemy):
        enemy.hit -= 2
        you.hit += 2

class Shield(Spell):
    """
    Shield costs 113 mana. It starts an effect that lasts for 6 turns.
    While it is active, your armor is increased by 7.
    """
    cost = 113
    duration = 6

    def apply(self, you, enemy):
        you.armor = 7

class Poison(Spell):
    """
    Poison costs 173 mana. It starts an effect that lasts for 6 turns.
    At the start of each turn while it is active, it deals the boss 3 damage.
    """
    cost = 173
    duration = 6

    def apply(self, you, enemy):
        enemy.hit -= 3

class Recharge(Spell):
    """
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
    At the start of each turn while it is active, it gives you 101 new mana.
    """
    cost = 229
    duration = 5

    def apply(self, you, enemy):
        you.mana += 101


class Spells:
    def __init__(self):
        self.spells = [
            MagicMissile(),
            Drain(),
            Shield(),
            Poison(),
            Recharge(),
        ]

    def available(self, mana):
        return [sp for sp in self.spells if mana > sp.cost]

    def apply(self, you, enemy):
        for sp in self.spells:
            if sp.active:
                sp.apply(you, enemy)
                sp.timer -= 1
                if sp.timer == 0:
                    sp.active = False

def play(you, boss, spells=None, show=None):
    spell_iter = iter(spells)
    your_spells = Spells()
    if show is None:
        show = lambda s: None
    while True:
        show("\nPlayer turn")
        show(you)
        show(boss)
        you.armor = 0       # I don't understand armor, this makes it work?
        your_spells.apply(you, boss)

        next_spell = your_spells.spells[next(spell_iter)]
        show(next_spell)
        next_spell.cast(you, boss)
        #boss.defend(you)
        if boss.dead():
            return you

        show("\nBoss turn")
        show(you)
        show(boss)
        you.armor = 0       # I don't understand armor, this makes it work?
        your_spells.apply(you, boss)
        if boss.dead():
            return you
        you.defend(boss)
        if you.dead():
            return boss

print("Test 1:")
test_you = Player("you", hit=10, mana=250)
test_boss = Player("boss", hit=13, damage=8)

winner = play(test_you, test_boss, spells=[3, 0], show=print)
print("winner is {}".format(winner))

print("\n-----------------\nTest 2:")
test_you = Player("you", hit=10, mana=250)
test_boss = Player("boss", hit=14, damage=8)

winner = play(test_you, test_boss, spells=[4, 2, 1, 3, 0], show=print)
print("winner is {}".format(winner))



