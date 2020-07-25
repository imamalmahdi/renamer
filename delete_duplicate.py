from imagehash import average_hash
from itertools import combinations
from pathlib import Path
from send2trash import send2trash
from PIL import Image
import json


def get_hash(image):
    cache_file = Path(f"{Path(__file__).parent.absolute()}//cached_hash.txt")
    cached_data = json.loads(cache_file.read_text())
    image_date = image.stat().st_ctime
    for data in cached_data:
        if image_date == data[0]:
            return data[1]
    else:
        the_image = Image.open(image)
        the_hash = average_hash(the_image)
        image_info = (image_date, str(the_hash))
        cached_data.append(image_info)
        cache_file.write_text(json.dumps(cached_data))
        return the_hash


def delete_duplicate():
    directory = Path(r"D:\Pics\UwU")
    images = directory.iterdir()

    image_and_hashes = []

    for image in images:
        if image.suffix in [".mp4", ".ini", ".db"] or image.is_dir():
            continue
        else:
            try:
                temp_tupol = [image, str(get_hash(image))]
                image_and_hashes.append(temp_tupol)
            except OSError:
                pass

    duplicates = []
    for a, b in combinations(image_and_hashes, 2):
        if a[1] == b[1]:
            duplicates.append(a[0])

    if duplicates != []:
        for duplicate in duplicates:
            send2trash(str(duplicate).encode())
    else:
        pass
