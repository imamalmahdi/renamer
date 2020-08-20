from imagehash import phash
from itertools import combinations
from pathlib import Path
from send2trash import send2trash
from PIL import Image
import json


def get_hash(image):
    cache_file = Path(f"{Path(__file__).parent.absolute()}//cached_hash.txt")
    if not cache_file.exists():
        with open(cache_file, "w"): pass
        cached_data = []
    else:
        try: 
            cached_data = json.loads(cache_file.read_text())
        except:
            cached_data = []
    
    image_date = image.stat().st_ctime
    image_size = image.stat().st_size
    for data in cached_data:
        if image_date == data[0][0] and image_size == data[0][1]:
            return data[1]
    else:
        the_image = Image.open(image)
        the_hash = phash(the_image)
        print("Hashing", image)
        image_info = ((image_date, image_size), str(the_hash), image.name)
        cached_data.append(image_info)
        cache_file.write_text(json.dumps(cached_data, indent=4))
        return the_hash


def delete_duplicate(path):
    directory = Path(path)
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
            print(a[0], "matched", b[0])

    if duplicates != []:
        for duplicate in duplicates:
            send2trash(str(duplicate).encode())
    else:
        pass
