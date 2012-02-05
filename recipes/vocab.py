#!/usr/bin/env python2

units = [l for l in open("vocab/units.txt").read().split("\n") if l]

ingredients = dict()
ingredient_lines = [l for l in open("vocab/ingredients.txt").read().split("\n")
        if l]
for line in ingredient_lines[:-1]:
    parts = line.split(":")
    ingredient = parts[0]
    if len(parts) > 1:
        ingredients[ingredient] = parts[1].split(",")
    else:
        ingredients[ingredient] = []

