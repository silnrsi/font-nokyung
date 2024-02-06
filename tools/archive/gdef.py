#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
vs = range(0xFE00, 0xFE0F+1)

for glyph in font:
    if glyph.unicode in vs:
        glyph.appendAnchor('_none', (0, 0))

# Save UFO
font.changed()
font.save()
font.close()
