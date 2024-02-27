#!/usr/bin/python3

import argparse

from palaso.unicode.ucd import find_ucd, get_ucd


def main():
    parser = argparse.ArgumentParser(description='Find visual or logical encoding order')
    parser.add_argument('file', help='file to process', nargs='+')
    args = parser.parse_args()

    # All codepoints in the script
    uids = find_ucd('sc', 'Talu')

    # Useful ranges of codepoints
    consonants = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Consonant']
    matras = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Vowel_Dependent']
    left_matras = [uid for uid in matras if get_ucd(uid, 'InPC') == 'Visual_Order_Left']
    right_matras = [uid for uid in matras if get_ucd(uid, 'InPC') == 'Right']
    final_consonants = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Consonant_Final']
    tone = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Tone_Mark']

    for input_filename in args.file:
        with open(input_filename, 'r') as input_file:
            line_number = 1
            for line in input_file:
                location = f'{input_filename}:{line_number}: '
                usv_prev1 = usv_prev2 = ''
                for char in line:
                    usv = ord(char)
                    if usv in left_matras:
                        if usv_prev1 not in uids:
                            print(f'{location}visual other/left')
                        if usv_prev1 in final_consonants:
                            print(f'{location}visual final/left')
                        if usv_prev2 in final_consonants and usv_prev1 in tone:
                            print(f'{location}visual final/tone/left')
                        if usv_prev1 in right_matras:
                            print(f'{location}visual right/left')
                        if usv_prev2 in right_matras and usv_prev1 in tone:
                            print(f'{location}visual right/tone/left')
                    if usv in tone:
                        if usv_prev1 in left_matras:
                            if usv_prev2 in consonants:
                                print(f'{location}logical consonant/left/tone')
                    usv_prev2 = usv_prev1
                    usv_prev1 = usv
                line_number += 1


if __name__ == "__main__":
    main()
