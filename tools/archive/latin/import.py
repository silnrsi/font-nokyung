#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
one = font['NULL']
two = font['CR']

one.name = '.null'
two.name = 'nonmarkingreturn'

one.unicode = None
two.unicode = None

# Save UFO
font.changed()
font.save()
font.close()
