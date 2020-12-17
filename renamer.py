from directories import Directory
from sys import argv
from config import load_setting
from os import walk

if argv[-1] == "--auto":
    settings = load_setting()
    for folder in settings["folders"]:
        for itered_dir in walk(folder):
            Directory(itered_dir[0]).rename_dir()

else:
    working_dir = input("Enter a directory: ")
    print("Now, wait a bit...")
    Directory(working_dir).rename_dir()

    print("Done!")