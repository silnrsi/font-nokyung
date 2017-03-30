#! /usr/bin/env python
# FFremoveOverlapAll.py
# FontForge: Remove overlap on all glyphs in font
# VG 22 Feb 2012
# usage: FFremoveOverlapAll.py [sourcefont.sfd] [resultfont.sfd]

import sys, fontforge

source = fontforge.open(sys.argv[1])
result = sys.argv[2]

for glyph in source:
    source[glyph].removeOverlap()
source.save(result)

