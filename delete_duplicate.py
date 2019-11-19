from imagehash import average_hash
from itertools import combinations
from pathlib import Path
from send2trash import send2trash
from PIL import Image


def get_hash(image):
    the_image = Image.open(image)
    the_hash = average_hash(the_image)

    return the_hash


def delete_duplicate():
    directory = Path(r"D:\Pics\UwU")
    images = directory.iterdir()

    image_and_hashes = []

    for image in images:
        temp_tupol = [image, str(get_hash(image))]
        image_and_hashes.append(temp_tupol)

    duplicates = []
    for a, b in combinations(image_and_hashes, 2):
        if a[1] == b[1]:
            duplicates.append(a[0])

    if duplicates != []:
        for duplicate in duplicates:
            send2trash(str(duplicate).encode())
    else:
        pass
