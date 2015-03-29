#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='tests'
TESTRESULTSDIR = 'results'
STANDARDS = 'standards'

# set the font name, version, licensing and description
APPNAME="Nokyung"
VERSION="1.200"
TTF_VERSION="1.200"
COPYRIGHT="Copyright (c) 2008-2015, SIL International (http://www.sil.org)"
LICENSE='OFL.txt'

DESC_SHORT = "Unicode font for Dai Banna"
DESC_LONG = """
Nokyung is a Unicode font for the Dai Banna script.
Font sources are published in the repository and a smith open workflow is used for building, testing and releasing.
"""
DESC_NAME = "Nokyung"
DEBPKG = 'fonts-sil-nokyung'

# set the build and test parameters
mytest = fonttest(targets = {
        'pdfs' : tex(),
    })
f = font(target = process('NokyungTestDA.ttf', name(APPNAME)),
        # why remove overlap twice?
     source = create("Nokyung-R-not.sfd", cmd("../bin/FFRemoveOverlapAll.py ${SRC} ${TGT}", ["font-source/NokyungTest-R.ufo"]),
                                          cmd("../bin/FFRemoveOverlapAll.py ${DEP} ${TGT}")),
     version = VERSION,
     license = ofl('Nokyung','SIL'),
     script='talu',
     fret = fret(params = '-r'),
     woff = woff(),
     tests = mytest
)

#subset(target = 'subsets/NokyungTestCA.ttf',
#    source = f)
