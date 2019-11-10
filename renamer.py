# This program renames all files in a given directory by date and a name given by the user
# UwU
# V1.1Su

from pathlib import Path
import os
import time


def get_attribute(dir):
    current_dir = Path(dir)
    time_modified = []
    for path in current_dir.iterdir():
        info = path.stat()
        info_stat = (path, info.st_ctime)
        time_modified.append(info_stat)

    time_modified.sort(key=lambda time: time[1])
    return time_modified


print("\nHi!")
print("This program will rename all your collection of lewd by date for you!")

print("\nEnter your sauce: ")
directory = input()

print("\nNow a cute name for them UwU: ")
cute_name = input()

print("\nThanks, brozzer!")
print("Please, wait a bit..")


attributes = get_attribute(directory)
serial = 1

for name, useless in attributes:
    file_name = f"{directory}\\{cute_name}_{str(serial)}{str(name.suffix)}"
    os.rename(name, file_name)
    serial += 1


time.sleep(2)
print("\nDone, my dude")
print(f"Renamed {serial} files")
print("Enjoy your lewds!\n")
print("(Isn't really)Copyright 2019 demonicshady\n")
