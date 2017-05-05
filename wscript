#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out = "results"
DOCDIR = ["documentation", "web"]
OUTDIR = "installers"
ZIPDIR = "releases"
TESTDIR = "tests"
#TESTRESULTSDIR = "tests"
STANDARDS = "reference"

# set the font name, version, licensing and description
APPNAME = "Nokyung"
VERSION = "1.490"
COPYRIGHT = "Copyright (c) 2008-2017, SIL International (http://www.sil.org) with Reserved Font Name \"Nokyung\"."
LICENSE = 'OFL.txt'

DESC_NAME = "Nokyung"
DESC_SHORT = "Unicode font for the New Tai Lue script"
DESC_LONG = """
Nokyung is a Unicode font for the New Tai Lue script.
Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
DEBPKG = 'fonts-sil-nokyung'

for style in ('-Regular','-Bold') :
    font(target = process(APPNAME + style + '.ttf'),
#        source = 'source/' + FILENAMEBASE + style + '.ufo',
        source = create(APPNAME + style + '-not.sfd', cmd("../tools/FFremoveOverlapAll.py ${SRC} ${TGT}", ['source/' + APPNAME + style + '.ufo']),
                                          cmd("../tools/FFremoveOverlapAll.py ${DEP} ${TGT}")),
#        opentype = internal(),
#        script = 'talu',
#        fret = fret(params = '-r'),
        woff = woff(params = '-v ' + VERSION + ' -m ../source/Nokyung-WOFF-metadata.xml')
    )
