#!/usr/bin/python
# this is a smith configuration file 

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='test-suite'
TESTRESULTSDIR = 'test-results'
STANDARDS = 'standards'

# set the font name, version, licensing and description
APPNAME="NokyungTestCA"
VERSION="1.200"
TTF_VERSION="1.200"
COPYRIGHT="Copyright (c) 2008-2014, SIL International (http://www.sil.org)"
LICENSE='OFL.txt'

DESC_SHORT = "Smart Unicode font for Tai Lue"
DESC_LONG = """
Nokyung is a smart Unicode font for Tai Lue.
It uses the Graphite rendering for positioning. Font sources are published in the repository and a smith workflow is used for building, testing and releasing.
"""
DESC_NAME = "Nokyung"
SRCDIST = 'fonts-nokyung-developer'
DEBPKG = 'fonts-sil-nokyung'

# set the build and test parameters
mytest = fonttest(targets = {
        'pdfs' : tex(),
    })
font(target = process('NokyungTestCA.ttf', name(APPNAME)),
     source = create("Nokyung-R-not.sfd", cmd("../bin/FFRemoveOverlapAll.py ${SRC} ${TGT}", ["font-source/Nokyung-R.sfd"]), cmd("../bin/FFRemoveOverlapAll.py ${DEP} ${TGT}")),
     version = VERSION,
     license = ofl('Nokyung','SIL'),
     script='talu',
     graphite=gdl(master='font-source/tlue.gdl', no_make=1),
     opentype=internal(),
     fret = fret(params = '-r'),
     woff = woff(),
     tests = mytest
)