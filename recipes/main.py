#!/usr/bin/env python
""" Main entry point for the project. """

from sys import stdin, stdout

from scrape import scrapeRecipe, scrapeSearch

def trim(text):
    return text.lstrip(' \t\n').rstrip(' \t\n')


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
    stdout.write("Results:\n")
    for (i, result) in enumerate(results):
        stdout.write(" %d: %s\n" % (i, result[0]))
        if i >= 9: break

    choice = -1
    while choice < 0 or choice > min(len(results) - 1, 9):
        stdout.write("Enter the number of a recipe: ")
        choice = int(trim(stdin.readline()))
    stdout.write("Scraping...")
    stdout.flush()
    recipe = scrapeRecipe(results[choice][1])
    stdout.write(" Done!\n")
    stdout.write("This is what we parsed:\n\n")
    stdout.write(recipe.prettify())
    stdout.write("\n")

