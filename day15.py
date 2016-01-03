#!/usr/bin/env python3
# http://adventofcode.com/day/15

INPUT = """\
Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
"""

import collections
import itertools
import re

Properties = collections.namedtuple('Properties', 'cap, dur, fla, tex, cal')

def parse_input(inp):
    ingredients = {}
    for line in inp.splitlines():
        name, _, props = line.partition(':')
        prop_vals = re.findall(r'-?\d+', line)
        ingredients[name] = Properties(*map(int, prop_vals))
    return ingredients


def all_recipes(ingredients, total):
    """Produce all recipes of total units of ingredients"""
    ingredients = list(ingredients)
    n_ingred = len(ingredients)

    for amounts in itertools.product(range(total+1), repeat=n_ingred-1):
        so_far = sum(amounts)
        if so_far > total:
            continue
        recipe = list(zip(ingredients, amounts))
        recipe.append((ingredients[-1], total - sum(amounts)))
        yield recipe


def total_score(recipe, ingredients):
    score = 1
    for propi in range(4):
        prop_total = 0
        for item, amount in recipe:
            prop_total += amount * ingredients[item][propi]
        if prop_total < 0:
            prop_total = 0
        score *= prop_total
    return score


def best_recipe(ingredients, total, choose=None):
    recipes = all_recipes(ingredients, total)
    if choose is not None:
        recipes = filter(lambda r: choose(r, ingredients), recipes)
    recipes_with_scores = map(
        lambda r: (total_score(r, ingredients), r),
        recipes
    )
    return max(recipes_with_scores)


TEST = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""

def nice_result(result):
    return "recipe is {0[1]} for a score of {0[0]}".format(result)

print("Part 1:")
print("Test: {}".format(nice_result(best_recipe(parse_input(TEST), 100))))
print("Answer: {}".format(nice_result(best_recipe(parse_input(INPUT), 100))))

def calories(recipe, ingredients):
    total = 0
    for item, amount in recipe:
        total += amount * ingredients[item].cal
    return total

def calories500(recipe, ingredients):
    return calories(recipe, ingredients) == 500

print("Part 2:")
print("Test: {}".format(nice_result(best_recipe(parse_input(TEST), 100, calories500))))
print("Answer: {}".format(nice_result(best_recipe(parse_input(INPUT), 100, calories500))))
