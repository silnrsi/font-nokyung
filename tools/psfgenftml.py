#!/usr/bin/python3
__doc__ = '''generate ftml tests from glyph_data.csv and UFO'''
__url__ = 'https://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018-2024 SIL International  (https://www.sil.org)'
__license__ = 'Released under the MIT License (https://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from fontParts.world import *
from silfont.core import execute
import silfont.ftml_builder as FB
from palaso.unicode.ucd import get_ucd

argspec = [
    ('ifont', {'help': 'Input UFO'}, {'type': 'infont'}),
    ('output', {'help': 'Output file ftml in XML format', 'nargs': '?'}, {'type': 'outfile', 'def': '_out.ftml'}),
    ('-i','--input', {'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-f','--fontcode', {'help': 'letter to filter for glyph_data'},{}),
    ('--prevfont', {'help': 'font file of previous version'}, {'type': 'filename', 'def': None}),
    ('-l','--log', {'help': 'Set log file name'}, {'type': 'outfile', 'def': '_ftml.log'}),
    ('--langs', {'help':'List of bcp47 language tags', 'default': None}, {}),
    ('--rtl', {'help': 'enable right-to-left features', 'action': 'store_true'}, {}),
    ('--norendercheck', {'help': 'do not include the RenderingUnknown check', 'action': 'store_true'}, {}),
    ('-t', '--test', {'help': 'name of the test to generate', 'default': None}, {}),
    ('-s','--fontsrc', {'help': 'font source: "url()" or "local()" optionally followed by "=label"', 'action': 'append'}, {}),
    ('--scale', {'help': 'percentage to scale rendered text (default 100)'}, {}),
    ('--ap', {'help': 'regular expression describing APs to examine', 'default': '.'}, {}),
    ('-w', '--width', {'help': 'total width of all <string> column (default automatic)'}, {}),
    ('--xsl', {'help': 'XSL stylesheet to use'}, {}),
]

ageToFlag = 14.0
ageColor = '#FFC8A0'      # light orange -- marks if there is a char from above Unicode version or later
missingColor = '#FFE0E0'  # light red -- mark if a char is missing from UFO
newColor = '#F0FFF0'      # light green -- mark if char is not in previous version (if --prevFont supplied)
backgroundLegend = f'Background colors: light orange: includes a character from Unicode version {ageToFlag} or later; ' + \
                   'light red: a character is missing from UFO; ' \
                   'light green: a character is new in this version of the font'

def doit(args):
    logger = args.logger

    # Read input csv
    builder = FB.FTMLBuilder(logger, incsv=args.input, fontcode=args.fontcode, font=args.ifont, ap=args.ap,
                             rtlenable=args.rtl, langs=args.langs)

    # Override default base (25CC) for displaying combining marks:
    builder.diacBase = 0x1980   # high qa

    # Specify block of primary script
    block = range(0x1980, 0x19DF+1)

    # Useful ranges of codepoints
    uids = sorted(builder.uids())
    consonants = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Consonant']
    matras = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Vowel_Dependent']
    left_matras = [uid for uid in matras if get_ucd(uid, 'InPC') == 'Visual_Order_Left']
    final_consonants = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Consonant_Final']
    tone = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Tone_Mark']
    digits = [uid for uid in uids if builder.char(uid).general == 'Nd' and uid in block]
    punct = [uid for uid in uids if get_ucd(uid, 'gc').startswith('P')]

    # Read pair kerning data that was in the Regular UFO.
    # Group and glyphs names only, not the amount of kerning.
    ifont = OpenFont(args.ifont.ufodir)
    kerning = ifont.kerning
    groups = ifont.groups

    # Initialize FTML document:
    # Default name for test: AllChars or something based on the csvdata file:
    test = args.test or 'AllChars (NG)'
    widths = None
    if args.width:
        try:
            width, units = re.match(r'(\d+)(.*)$', args.width).groups()
            if len(args.fontsrc):
                width = int(round(int(width)/len(args.fontsrc)))
            widths = {'string': f'{width}{units}'}
            logger.log(f'width: {args.width} --> {widths["string"]}', 'I')
        except:
            logger.log(f'Unable to parse width argument "{args.width}"', 'W')
    # split labels from fontsource parameter
    fontsrc = []
    labels = []
    for sl in args.fontsrc:
        try:
            s, l = sl.split('=',1)
            fontsrc.append(s)
            labels.append(l)
        except ValueError:
            fontsrc.append(sl)
            labels.append(None)
    ftml = FB.FTML(test, logger, comment=backgroundLegend, rendercheck=not args.norendercheck, fontscale=args.scale,
                   widths=widths, xslfn=args.xsl, fontsrc=fontsrc, fontlabel=labels, defaultrtl=args.rtl)

    if args.prevfont is not None:
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(args.prevfont)
            prevCmap = font.getBestCmap()
        except:
            logger.log(f'Unable to open previous font {args.prevfont}', 'S')


    def setBackgroundColor(uids):
        # if any uid in uids is missing from the UFO, set test background color to missingColor
        if any(uid in builder.uidsMissingFromUFO for uid in uids):
            ftml.setBackground(missingColor)
        # else if any uid in uids has Unicode age >= ageToFlag, then set the test background color to ageColor
        elif max(map(lambda x: float(get_ucd(x, 'age')), uids)) >= ageToFlag:
            ftml.setBackground(ageColor)
        elif args.prevfont and any(uid not in prevCmap for uid in uids):
            ftml.setBackground(newColor)

    if test.lower().startswith("allchars"):
        # all chars that should be in the font:
        ftml.startTestGroup('Encoded characters')
        for uid in uids:
            if uid < 32: continue
            c = builder.char(uid)
            setBackgroundColor((uid,))
            for featlist in builder.permuteFeatures(uids=(uid,)):
                ftml.setFeatures(featlist)
                builder.render((uid,), ftml)
                # Don't close test -- collect consecutive encoded chars in a single row
            ftml.clearFeatures()
            if len(c.langs):
                for langID in builder.allLangs:
                    ftml.setLang(langID)
                    builder.render((uid,), ftml)
                ftml.clearLang()
            ftml.clearBackground()

        # Characters used to create SILE test data
        ftml.startTestGroup('Proof')
        for section_name in ('consonants', 'matras', 'final_consonants', 'tone', 'digits', 'punct'):
            section = eval(section_name)
            builder.render(section, ftml, label=section_name, comment=f'{section[0]:04X}')
            ftml.closeTest()
        for group_name in groups:
            pattern_group = list()
            for glyph_name in groups[group_name]:
                char = builder.char(glyph_name).uid
                pattern_group.append(char)
            builder.render(pattern_group, ftml, label=group_name, comment=f'{pattern_group[0]:04X}')
            ftml.closeTest()

    if test.lower().startswith("kern"):
        for group_pair in kerning:
            one = group_pair[0]
            two = group_pair[1]

            ftml.startTestGroup(f'{one}-{two}')
            for glyph_name_one in groups[one]:
                char_one = builder.char(glyph_name_one).uid
                for glyph_name_two in groups[two]:
                    char_two = builder.char(glyph_name_two).uid
                    char_pair = (char_one, char_two)
                    builder.render(char_pair, ftml, label=f'{char_one:04X}', comment=glyph_name_one)
                ftml.closeTest()

    if test.lower().startswith("matras"):
        ftml.startTestGroup('Consonants with matras')
        for c in consonants:
            for m in matras:
                if m in left_matras:
                    cluster = (m,c)
                else:
                    cluster = (c,m)
                builder.render(cluster, ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

    # Write the output ftml file
    ftml.writeFile(args.output)


def cmd() : execute("UFO",doit,argspec)
if __name__ == "__main__": cmd()
