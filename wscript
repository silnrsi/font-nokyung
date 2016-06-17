#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='tests'
#TESTRESULTSDIR = 'results/tests'
STANDARDS = 'standards'

# set the font name, version, licensing and description
APPNAME="Nokyung"
FILENAMEBASE="Nokyung"
VERSION="1.302"
TTF_VERSION="1.302"
COPYRIGHT="Copyright (c) 2008-2016, SIL International (http://www.sil.org)"
LICENSE='OFL.txt'

DESC_SHORT = "Unicode font for New Tai Lue"
DESC_LONG = """
Nokyung is a Unicode font for the New Tai Lue script.
Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
DESC_NAME = "Nokyung"
DEBPKG = 'fonts-sil-nokyung'

for style in ('-R','-B') :
    font(target = process(FILENAMEBASE + style + '.ttf', cmd("ttftable -d opentype ${DEP} ${TGT}")),
#        source = 'source/' + FILENAMEBASE + style + '.ufo',
        source = create(FILENAMEBASE + style + '-not.sfd', cmd("../tools/FFRemoveOverlapAll.py ${SRC} ${TGT}", ['source/' + FILENAMEBASE + style + '.ufo']),
                                          cmd("../tools/FFRemoveOverlapAll.py ${DEP} ${TGT}")),
        version = VERSION,
        license = ofl('Nokyung','SIL'),
        opentype = internal(),
#        script = 'talu',
        fret = fret(params = '-r'),
        woff = woff()
    )
