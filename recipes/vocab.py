#!/usr/bin/env python

units = [l for l in open("vocab/units.txt").read().split("\n") if l]

nouns = dict()
noun_lines = [l for l in open("vocab/nouns.txt").read().split("\n")
        if l]
for line in noun_lines:
    parts = line.split(":")
    noun = parts[0]
    if len(parts) > 1:
        nouns[noun] = parts[1].split(",")
    else:
        nouns[noun] = []

adjectives = [l for l in open("vocab/adjectives.txt").read().split("\n") if l]

