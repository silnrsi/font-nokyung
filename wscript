#!/usr/bin/python3
# -*- coding: utf-8 -*-

APPNAME = "Nokyung"
DESC_SHORT = "Unicode font for the New Tai Lue script"

getufoinfo('source/masters/Nokyung-Regular.ufo')

fontfamily=APPNAME

generated = 'generated/'
designspace('source/' + fontfamily + '.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = 'source/main.feax',
                ),
            pdf = fret(params="-r -oi"),
            woff = woff()
)
