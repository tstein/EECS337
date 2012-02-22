#!/usr/bin/env python
""" Contains the Recipe data structure and functions for creating and
manipulating them. """

import re
from random import randint

import nltk

from vocab import adjectives, nouns, units


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
        self.categories = dict()
        self.ethnicities = dict()

    def prettify(self):
        """ Stringify a recipe for human consumption. """
        prettified = "\n" + self.title + ":\n"
        relevant_ethnicities = [k for k, v in self.ethnicities.iteritems()]
        if len(relevant_ethnicities) > 0:
            prettified += "`-> This recipe seems kinda "
            prettified += " and ".join(relevant_ethnicities)
            prettified += ", but what do I know?\n"
        if self.preptime is not None:
            prettified += "    Prep: %s    Cook: %s    Total: %s\n" % \
                (self.preptime, self.cooktime, self.totaltime)
        prettified += "\nIngredients:\n"
        for category in _sortCategories(self.categories.keys()):
            prettified += "  " + category + ":\n"
            for ingredient in self.categories[category]:
                prettified += "    " + _prettifyIngredient(ingredient,
                        self.ingredients[ingredient]) + "\n"
        prettified += "\nDirections:\n"
        for direction in self.directions:
            prettified += "    " + direction + "\n"
        prettified += "\n"
        return prettified

    def makeCategories(self):
        """ Make reverse category mappings. """
        self.categories.clear()
        for ingredient in self.ingredients:
            known_ingredient = fuzzyfind(ingredient, nouns.keys())
            if known_ingredient is not None:
                category = nouns[known_ingredient][0]
                if not category:
                    category = "misc"
            else:
                category = "misc"
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(ingredient)

    def makeEthnicities(self):
        """ Make reverse ethnicity mappings. """
        self.ethnicities.clear()
        for ingredient in self.ingredients:
            known_ingredient = fuzzyfind(ingredient, nouns.keys())
            if known_ingredient is not None:
                ethnicity = nouns[known_ingredient][1]
                if ethnicity:
                    if ethnicity not in self.ethnicities:
                        self.ethnicities[ethnicity] = []
                    self.ethnicities[ethnicity].append(ingredient)

    def changeIngredient(self, old, new):
        """ Swap out an ingredient for a new one.
            Args:
                old: A string. The name of the ingredient to remove.
                new: A tuple to replace the ingredient referred to by old with.
        """
        if old is not None:
            del self.ingredients[old]
        if new is not None:
            self.ingredients[new[0]] = (new[1], new[2], new[3])
        for i, direction in enumerate(self.directions):
            self.directions[i] = substituteText(direction, old, new[0])
        lower_title = substituteText(self.title.lower(), old, new[0])
        lower_tokens = lower_title.split(" ")
        tokens = []
        for t in lower_tokens:
            t = t[0].upper() + t[1:]
            tokens.append(t)
        # Deal with stupid Roman numerals explicitly.
        if re.match('[IVX]+', tokens[-1]):
            tokens[-1] = tokens[-1].upper()
        self.title = " ".join(tokens)
        self.makeCategories()
        self.makeEthnicities()

    def changeEthnicity(self, new):
        """ Swap out any ethnicity for a new one. """
        ethnic_foods = {k: c for k, (c, e) in nouns.items() if e == new}
        for (efood, cat) in ethnic_foods.items():
            if cat in self.categories:
                old_name = pickRandom(self.categories[cat])
                old_tuple = self.ingredients[old_name]
                new_tuple = (efood, old_tuple[0], old_tuple[1], None)
                self.changeIngredient(old_name, new_tuple)
        self.makeCategories()
        self.makeEthnicities()


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
    modifiers = [i.lstrip(' ,-(').rstrip(' ,-)') for i in modifiers if i]
    return (name, quantity, unit, modifiers)


def _isIngredientWord(text, kind):
    """ Test all the ways something can be an ingredient. """
    if text in nouns:
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


def understandDirections(directions, ingredients):
    """ Take a list of strings representing individual instructions and return
    a list of (action, object, parameters) tuples. """
    directions = splitDirections(directions)
    return [_understandDirection(d, ingredients) for d in directions]


def _understandDirection(direction, ingredients):
    """ Take a string describing one instruction and return an (action, object,
    parameters) tuple. """
    tokens = nltk.pos_tag(nltk.word_tokenize(direction))
    # Directions generally begin with a verb or a subordinate clause followed
    # by a verb.
    firstparam = ""
    if tokens[0][1] == 'IN':
        for text, kind in tokens:
            tokens = tokens[1:]
            if not re.match('[\w\d]+', text):
                break
            firstparam += " " + text
        firstparam = firstparam.lstrip()

    # NLTK reliably misidentifies verbs as nouns here. Build an action until we
    # see a part of speech that doesn't belong or an ingredient. e.g.,
    # [slowly stir] the...
    # [mash] potatoes...
    action = ""
    for text, kind in tokens:
        # These types don't belong to actions:
        #   DT: determiner
        #   IN: preposition or conjunction, subordinating
        #   TO: to, dummy
        if re.match('^(?:DT|IN|TO)$', kind) or text in nouns:
            break
        action += " " + text
        tokens = tokens[1:]
    action = action.lstrip()
    return direction


def fuzzyfind(query, values):
    """ Find... fuzzily. """
    query = query.lower()
    values = [v.lower() for v in values]
    # Try to match the entirety of query against an entire value.
    if query in values:
        return query
    # Try to match the entirety of query in a value.
    for v in values:
        if query in subphrases(v):
            return query
    # Try to match the token as best as possible.
    for token in reversed(query.split(" ")):
        if token in values:
            return token
        for v in values:
            if abs(len(v) - len(token)) <= 2 and \
                    v.startswith(token) or token.startswith(v):
                return v
    return None


def subphrases(sentence):
    """ Generate all subphrases, right-to-left, longest-to-shortest. """
    tokens = sentence.split(" ")
    for i in reversed(range(0, len(tokens))):
        for j in reversed(range(0, len(tokens) - i)):
            yield " ".join(tokens[j:j + i + 1])


def substituteText(string, old, new):
    """ Substitute old for new in string, using fuzzy logic when possible. """
    found = fuzzyfind(old, nltk.word_tokenize(string))
    if found is not None:
        if found[0].isupper():
            new[0] = new[0].upper()
        return string.replace(found, new)
    return string


def _sortCategories(categories):
    """ Force some sort of order on the categories. """
    prependees = ['meat', 'starch', 'dairy', 'fruit', 'vegetable']
    appendees = ['seasonings', 'misc']
    for p in reversed(prependees):
        if p in categories:
            categories.remove(p)
            categories.insert(0, p)
    for p in appendees:
        if p in categories:
            categories.remove(p)
            categories.append(p)
    return categories


def pickRandom(objects):
    """ Pick a random item from a list. """
    return objects[randint(0, len(objects) - 1)]

