#!/usr/bin/env python
""" Main entry point for the project. """

from random import shuffle
from sys import stdin, stdout

import nltk

from recipe import fuzzyfind
from scrape import scrapeRecipe, scrapeSearch
from vocab import nouns


def trim(text):
    return text.lstrip(' \t\n').rstrip(' \t\n')


def loadNltk():
    """ Attempt to use the nltk. If it fails, download the corpora. """
    try:
        text = nltk.word_tokenize("There are four types of internal \
            combustion engine.")
        nltk.pos_tag(text)
    except LookupError:
        stdout.write("nltk data not present. Downloading.\n")
        nltk.download("book")


def getChoice(options):
    """ Get a numeric choice from a list of options. """
    choice = -1
    while choice < 0 or choice >= len(options):
        for i, opt in enumerate(options):
            stdout.write("  %2d. %s\n" % (i, opt))
        stdout.write("> ")
        choice = int(trim(stdin.readline()))
    return choice


loadNltk()
while (True):
    stdout.write("\nEnter a search query: ")
    query = trim(stdin.readline())
    if not query:
        stdout.write("Exiting.\n")
        break
    stdout.write("Scraping...")
    stdout.flush()
    results = scrapeSearch(query) 
    stdout.write(" Done!\n")
    if not results:
        stdout.write("You can't eat that!\n")
    else:
        stdout.write("Results:\n")
        stdout.write("Choose a recipe:\n")
        choice = getChoice([x[0] for x in results[0:10]])
        stdout.write("Scraping...")
        stdout.flush()
        recipe = scrapeRecipe(results[choice][1])
        stdout.write(" Done!\n\n")
        stdout.write(recipe.prettify())
        stdout.write("\n")
        stdout.write("Now what?\n")
        choice = getChoice(['substitution', 'culture swap', 'search again'])
        if choice == 2:
            continue
        if choice == 0:
            ingredients = recipe.ingredients.keys()
            stdout.write("Take what out?\n")
            choice = getChoice(ingredients)
            to_remove = ingredients[choice]
            try:
                found = fuzzyfind(to_remove, nouns.keys())
                category = nouns[found][0]
            except KeyError:
                category = 'misc'
            candidates = [x for x in nouns.keys() if x != to_remove]
            if category != 'misc':
                candidates = [x for x in candidates if nouns[x][0] == category]
            candidates = shuffle(candidates)
            stdout.write("Put what in?\n")
            choice = getChoice(candidates[0:10])
            old_tuple = recipe.ingredients[to_remove]
            to_add = (candidates[choice], old_tuple[0], old_tuple[1],
                    old_tuple[2])
            recipe.changeIngredient(to_remove, to_add)
            stdout.write("\nYour new recipe, substituting %s for %s:\n" %
                    (to_add[0], to_remove))
            stdout.write(recipe.prettify())
        if choice == 1:
            # culturize
            pass

