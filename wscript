#!/usr/bin/python3
# -*- coding: utf-8 -*-
# this is a smith configuration file

# override the default folders
generated = 'generated/'

# set the font name
APPNAME = 'Nokyung'
FAMILY = APPNAME

# Get version info from Regular UFO;
# must be first function call:
getufoinfo('source/masters/Nokyung-Regular.ufo')

# Set up the FTML tests
ftmlTest('tools/ftml-smith.xsl')

designspace('source/' + FAMILY + '.designspace',
            target = process("${DS:FILENAME_BASE}.ttf",
                cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${source}'])
            ),
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = 'source/main.feax',
                ),
            version = VERSION,  # Needed to ensure dev information on version string
            woff = woff('web/${DS:FILENAME_BASE}',
                metadata = f'../source/{FAMILY}-WOFF-metadata.xml'),
            pdf = fret(params='-oi')
)
