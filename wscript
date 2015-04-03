#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='tests'
TESTRESULTSDIR = 'test-results'
STANDARDS = 'standards'

# set the font name, version, licensing and description
APPNAME="Nokyung"
FILENAMEBASE="Nokyung"
VERSION="1.200"
TTF_VERSION="1.200"
COPYRIGHT="Copyright (c) 2008-2015, SIL International (http://www.sil.org)"
LICENSE='OFL.txt'

DESC_SHORT = "Unicode font for Dai Banna"
DESC_LONG = """
Nokyung is a Unicode font for the Dai Banna script.
Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
DESC_NAME = "Nokyung"
DEBPKG = 'fonts-sil-nokyung'

# set the build and test parameters
mytest = fonttest(targets = {
        'pdfs' : tex(),
    })

for style in ('-R','-B') :
    font(target = FILENAMEBASE + style + '.ttf',
#        source = 'source/' + FILENAMEBASE + style + '.ufo',
        source = create(FILENAMEBASE + style + '-not.sfd', cmd("../tools/FFRemoveOverlapAll.py ${SRC} ${TGT}", ['source/' + FILENAMEBASE + style + '.ufo']),
                                          cmd("../tools/FFRemoveOverlapAll.py ${DEP} ${TGT}")),
        version = VERSION,
        license = ofl('Nokyung','SIL'),
        script = 'talu',
        fret = fret(params = '-r'),
        woff = woff(),
        tests = mytest
    )
