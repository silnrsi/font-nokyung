#!/usr/bin/python
# this is a smith configuration file 

# set the default output folders
out="results"
DOCDIR="documentation"
OUTDIR="installers"
ZIPDIR="releases"
TESTDIR='test-suite'

APPNAME="NokyungTestCA"
VERSION="1.200"
COPYRIGHT="Copyright (c) 2008-2014 SIL International"

font(target = process('NokyungTestCA.ttf', name(APPNAME)),
     source = create("Nokyung-R-not.sfd", cmd("../bin/FFRemoveOverlapAll.py ${SRC} ${TGT}", ["font-source/Nokyung-R.sfd"]), cmd("../bin/FFRemoveOverlapAll.py ${DEP} ${TGT}")),
     version = VERSION,
     license = ofl('Nokyung'),
     script='talu',
     graphite=gdl(master='font-source/tlue.gdl', no_make=1),
     opentype=internal()
)

