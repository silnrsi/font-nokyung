#!/usr/bin/python
# this is a smith configuration file

# output folders use smith defaults and don't need to be set here

# set the version control system for srcdist
VCS = 'git'

APPNAME = "Nokyung"

DESC_NAME = "Nokyung"
DESC_SHORT = "Unicode font for the New Tai Lue script"
DESC_LONG = """
Nokyung is a Unicode font for the New Tai Lue script.
Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
DEBPKG = 'fonts-sil-nokyung'

getufoinfo('source/Nokyung-Regular.ufo')

fontfamily=APPNAME
designspace('source/' + fontfamily + '.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            pdf = fret(params="-r -oi"),
            woff = woff()
)

#for style in ('-Regular','-Bold') :
#    font(target = process(APPNAME + style + '.ttf'),
#        source = 'source/' + FILENAMEBASE + style + '.ufo',
#        source = create(APPNAME + style + '-not.sfd', cmd("../tools/FFremoveOverlapAll.py ${SRC} ${TGT}", ['source/' + APPNAME + style + '.ufo']),
#                                          cmd("../tools/FFremoveOverlapAll.py ${DEP} ${TGT}")),
#        opentype = internal(),
#        script = 'talu',
#        fret = fret(params = '-r'),
#        woff = woff('web/' + APPNAME + style + '.woff', params = '-v ' + VERSION + ' -m ../source/Nokyung-WOFF-metadata.xml')
#    )
