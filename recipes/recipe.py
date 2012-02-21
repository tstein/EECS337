#!/usr/bin/env python
""" Contains the Recipe data structure and functions for creating and
manipulating them. """

import re

import nltk

from vocab import adjectives, ingredients, units


DEBUG = True


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
        pretty_quant = ("%.2f" % quantity).rstrip('0')
        if pretty_quant[-1] == ".":
            pretty_quant = pretty_quant[:-1]
        if unit is not None:
            pretty = "%s: %s %s" % (name, pretty_quant, unit)
        else:
            pretty = "%s: %s" % (name, pretty_quant)
    else:
        pretty = name
    if modifiers:
        pretty += " (" + ", ".join(modifiers) + ")"
    return pretty


def understandIngredients(ingredients):
    """ Take a list of strings and return a dictionary of ingredient names to
    (quantity, unit, modifiers) tuples. """
    ret = dict()
    for i in ingredients:
        if i == i.upper():
            continue
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
    # Find the ingredient name and any modifiers.
    tokens = nltk.pos_tag(nltk.word_tokenize(ingredient))
    print tokens
    name = ""
    modifiers = []
    making_name = False
    for text, kind in tokens:
        if _isIngredientWord(text, kind) or \
                (making_name and kind.startswith('CC')):
            if not name:
                making_name = True
            if making_name:
                name += " " + text
        else:
            making_name = False
        if name and not making_name:
            break
    if not name:
        name = ingredient
        if DEBUG:
            print "%s failed: %s" % (ingredient, str(tokens))
            name = "*%s*" % name
    name = name.lstrip()
    modifiers = ingredient.split(name)
    modifiers = [i.lstrip(' ,-').rstrip(' ,-') for i in modifiers if i]
    return (name, quantity, unit, modifiers)


def _isIngredientWord(text, kind):
    """ Test all the ways something can be an ingredient. """
    if text in ingredients:
        return True
    # Consider all of the following word classes, as returned by nltk, to be
    # part of ingredient names:
    #   IN: preposition or conjunction, subordinating
    #   NN: noun, common, singular or mass
    #   NNP: noun, proper, singular
    #   NNPS: noun, proper, plural
    #   NNS: noun, common, plural
    #   VBG: verb, present participle or gerund
    #   VBZ: verb, present tense, 3rd person singular
    if re.match('^(?:(?:[IN]N)|VB[GZ])', kind) and text not in adjectives:
        return True
    return False


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


def splitDirections(directions):
    """ Split each of the directions parsed from the page into their
    constituent sentences. """
    newdirections = []
    for direction in directions:
        for direc in re.split('(?:\.\s+(?=[A-Z]))|(?:;\s+)', direction):
            if len(direc) > 0:
                direc = direc.lower().rstrip('.')
                newdirections.append(direc.lstrip())
    return newdirections


def understandDirections(directions):
    """ Take a list of strings representing individual instructions and return a
    list of (action, object, parameters) tuples. """
    directions = splitDirections(directions)
    return directions


def _understandDirection(direction):
    """ Take a string describing one instruction and return an (action, object,
    parameters) tuple. """
    pass

