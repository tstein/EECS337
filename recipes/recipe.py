#!/usr/bin/env python
""" Contains the Recipe data structure and functions for creating and
manipulating them. """

import re

from vocab import units


class Recipe(object):
    """ Represents a single recipe. """
    def __init__(self):
        self.title = ""
        self.image = None
        self.preptime = 0
        self.cooktime = 0
        self.totaltime = 0
        self.yields = ""
        self.ingredients = []
        self.directions = []

    def prettify(self):
        """ Stringify a recipe for human consumption. """
        prettified = self.title + ":\n"
        if self.preptime is not None:
            prettified += "Prep: %s    Cook: %s    Total: %s\n" % \
                (self.preptime, self.cooktime, self.totaltime)
        prettified += "Ingredients:\n"
        for ingredient in self.ingredients:
            prettified += "  " + _prettifyIngredient(ingredient,
                    self.ingredients[ingredient]) + "\n"
        prettified += "Directions:\n"
        for direction in self.directions:
            prettified += "  " + direction + "\n"
        return prettified


def _prettifyIngredient(name, (quantity, unit, modifiers)):
    """ Stringify an ingredient for human consumption. """
    if quantity is not None:
        if unit is not None:
            return "%s: %.2f %s" % (name, quantity, unit)
        else:
            return "%s: %.2f" % (name, quantity)
    else:
        return name


def understandIngredients(ingredients):
    """ Take a list of strings and return a dictionary of ingredient names to
    (quantity, unit, modifiers) tuples. """
    ret = dict()
    for i in ingredients:
        parsed = _understandIngredient(i)
        ret[parsed[0]] = (parsed[1], parsed[2], parsed[3])
    return ret


def _understandIngredient(ingredient):
    """ Take a string describing one ingredient and return a tuple of (name,
    quantity, unit, modifiers). """
    re_numeric = re.compile("(\d+/\d+|\d+(?:\,\d+)?)")
    if re_numeric.match(ingredient):
        quantity = re_numeric.match(ingredient).group(0)
        ingredient = ingredient[len(quantity):].lstrip()
        if re_numeric.match(ingredient):
            fraction = re_numeric.match(ingredient).group(0)
            quantity += " " + fraction
            ingredient = ingredient[len(fraction):].lstrip()
        quantity = _understandQuantity(quantity)
    else:
        quantity = None
    # Ignore any (10.5 oz) annotations.
    if ingredient[0] == "(":
        index = ingredient.find(")")
        ingredient = ingredient[index + 1:].lstrip()
    # Find the units, if any.
    unit = ingredient.split(" ")[0]
    if unit in units:
        ingredient = ingredient[len(unit):].lstrip()
    else:
        unit = None
    # Find the ingredient name.
    name = ingredient
    # Maybe later.
    modifiers = None

    return (name, quantity, unit, modifiers)


def _understandQuantity(quantity):
    """ Turn quantity strings into numbers. Handles:
        "1"     -> 1
        "1/2"   -> .5
        "1 1/2" -> 1.5
    """
    ret = 0
    parts = quantity.split(" ")
    frac = parts[-1].split("/")
    if len(frac) == 2:
        ret += float(frac[0]) / float(frac[1])
        if len(parts) > 1:
            ret += int(parts[0])
    else:
        ret = int(parts[0])
    return ret


def understandDirections(directions):
    return directions

