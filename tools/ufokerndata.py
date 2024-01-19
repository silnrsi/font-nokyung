#!/usr/bin/python3

import argparse
import pickle

from ufoLib2.objects import Font

# Command line arguments
parser = argparse.ArgumentParser(description='Dump kerning data to JSON')
parser.add_argument('-k', '--kerning', help='File to dump kerning.plist data to', default='kerning.pickle')
parser.add_argument('-g', '--groups', help='File to dump groups.plist data to', default='groups.pickle')
parser.add_argument('ufo', help='UFO to read')
args = parser.parse_args()

font = Font.open(args.ufo)
with open(args.kerning, 'wb') as kerning_file:
    pickle.dump(font.kerning, kerning_file)
with open(args.groups, 'wb') as groups_file:
    pickle.dump(font.groups, groups_file)
