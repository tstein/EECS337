#!/usr/bin/env python
""" Main entry point for the project. """

from random import shuffle
from sys import stdin, stdout

import nltk

from recipe import fuzzyfind
from scrape import scrapeRecipe, scrapeSearch
from vocab import ethnicity_set, nouns


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
    if not options:
        raise Exception("The hell?!")
    choice = -1
    while choice < 0 or choice >= len(options):
        for i, opt in enumerate(options):
            stdout.write("  %2d. %s\n" % (i, opt))
        stdout.write("> ")
        try:
            choice = int(trim(stdin.readline()))
        except ValueError:
            stdout.write("That ain't no number I ever heard of.\n")
    return choice


def main():
    try:
        stdout.write("Reticulating splines...\n")
        loadNltk()
        while (True):
            stdout.write("Enter a search query: ")
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
                next_choices = ['search again', 'substitution', 'culture swap']
                has_culture = bool(recipe.ethnicities.keys())
                if has_culture:
                    choice = getChoice(next_choices)
                else:
                    next_choices[-1] = "culturize!"
                    choice = getChoice(next_choices)
                if choice == 0:
                    continue
                if choice == 1:
                    ingredients = sorted(recipe.ingredients.keys())
                    stdout.write("Take what out?\n")
                    choice = getChoice(ingredients)
                    to_remove = ingredients[choice]
                    try:
                        found = fuzzyfind(to_remove, nouns.keys())
                        category = nouns[found][0]
                    except KeyError:
                        category = 'misc'
                    candidates = [x for x in nouns.keys() if fuzzyfind(to_remove, [x])
                            is None]
                    if category != 'misc':
                        candidates = [x for x in candidates if nouns[x][0] == category]
                    shuffle(candidates)
                    stdout.write("Put what in?\n")
                    choice = getChoice(candidates[0:6])
                    old_tuple = recipe.ingredients[to_remove]
                    to_add = (candidates[choice], old_tuple[0], old_tuple[1],
                            old_tuple[2])
                    recipe.changeIngredient(to_remove, to_add)
                    stdout.write("\nYour new recipe, substituting %s for %s:\n" %
                            (to_add[0], to_remove))
                    stdout.write(recipe.prettify())
                    continue
                if choice == 2:
                    stdout.write("What spin you wanna give this?\n")
                    prefixes = ['vaguely', 'somewhat', 'potentially']
                    shuffle(prefixes)
                    pref = prefixes[0]
                    suffixes = ['ified', 'ated', '-style', 'ized']
                    shuffle(suffixes)
                    suff = suffixes[0]
                    ethnicity_list = [e for e in sorted(list(ethnicity_set)) if e
                            not in recipe.ethnicities]
                    choice = getChoice(ethnicity_list)
                    new_ethn = ethnicity_list[choice]
                    recipe.changeEthnicity(new_ethn)
                    stdout.write("Your new recipe, %s %s%s!\n" % (pref, new_ethn,
                        suff))
                    stdout.write(recipe.prettify())
                    continue
            stdout.write("\n")
    except KeyboardInterrupt:
        stdout.write("\n")


if __name__ == '__main__':
    main()

