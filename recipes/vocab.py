#!/usr/bin/env python

units = [l for l in open("vocab/units.txt").read().split("\n") if l]

ethnicity_set = set()
nouns = dict()
noun_lines = [l for l in open("vocab/nouns.txt").read().split("\n")
        if l]
for line in noun_lines:
    parts = line.split(":")
    noun = parts[0]
    try:
        category = parts[1]
    except IndexError:
        category = ""
    try:
        ethnicity = parts[2]
    except IndexError:
        ethnicity = ""
    nouns[noun] = (category, ethnicity)
    if ethnicity:
        ethnicity_set.add(ethnicity)

adjectives = [l for l in open("vocab/adjectives.txt").read().split("\n") if l]

