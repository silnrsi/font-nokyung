#!/usr/bin/python3
# -*- coding: utf-8 -*-

APPNAME = "Nokyung"
DESC_SHORT = "Unicode font for the New Tai Lue script"

getufoinfo('source/masters/Nokyung-Regular.ufo')

fontfamily=APPNAME

designspace('source/' + fontfamily + '.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            pdf = fret(params="-r -oi"),
            woff = woff()
)
