#!/usr/bin/env python2
""" Contains the Recipe data structure and functions for creating and
manipulating them. """

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
        prettified = self.title + ":\n"
        prettified += "Prep: %s    Cook: %s    Total: %s\n" % (self.preptime,
                self.cooktime, self.totaltime)
        prettified += "Ingredients:\n"
        for ingredient in self.ingredients:
            prettified += "  " + ingredient + "\n"
        prettified += "Directions:\n"
        for direction in self.directions:
            prettified += "  " + direction + "\n"
        return prettified

