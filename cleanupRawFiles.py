#!/usr/bin/python3

import re
import os
import argparse

TRASH_DIR = 'Trash'

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to cleanup")
parser.add_argument("-e", "--extension", default="NEF", help="File extension to clean up. Files of this type without"
                                               " a match of reference type are moved.")
parser.add_argument("-r", "--reference", default="JPG", help="reference file extension")
args = parser.parse_args()

# Using the case insensitive flag to match, for example, both .NEF and .nef
regex = re.compile(r"(.*)\." + args.extension + "$", re.I)

files = os.listdir(args.dir)

files_to_move = []

for filename in files:
    match = regex.fullmatch(filename)
    if match:
        if str(match.groups()[0]) + '.' + args.reference not in files:
            files_to_move.append(match.string)

files_to_move.sort()

if len(files_to_move) > 0:
    trash_path = os.path.join(args.dir, TRASH_DIR)
    if not os.path.exists(trash_path):
        try:
            os.mkdir(trash_path)
        except FileExistsError as e:
            print(e)
            exit()
    if os.path.isdir(trash_path):
        for file_to_move in files_to_move:
            print("moving " + file_to_move)
            os.rename(os.path.join(args.dir, file_to_move), os.path.join(trash_path, file_to_move))
