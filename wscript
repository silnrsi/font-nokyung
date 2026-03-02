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

variable = package(
    appname = APPNAME + '-variable',
    version = VERSION,
    docdir = {'documentation': 'documentation', 'variable/web': 'web'}
)

stem = FAMILY
font(target = process(f'variable/{stem}.ttf',
    cmd('gftools fix-font --include-source-fixes -o ${TGT} ${DEP}'),
    cmd('../tools/genstat.sh ${DEP} ${TGT}')
    ),
    source = f'source/{stem}-VF.designspace',
    params = '--feature-writer None --filter DecomposeTransformedComponentsFilter',
    version = VERSION,
    woff = woff(f'variable/web/{stem}.woff2', type='woff2',
        metadata = f'../source/{FAMILY}-WOFF-metadata.xml',
        dontship = True),
    package = variable,
    no_test = True
)
