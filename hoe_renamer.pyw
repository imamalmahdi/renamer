from pathlib import Path
from os import rename, walk
from plyer import notification
from imagehash import phash
from itertools import combinations
from send2trash import send2trash
from PIL import Image
from datetime import datetime
import logging
import json

LOG_FILENAME = f"{Path(__file__).parent.absolute()}\\logs\\" + datetime.now().strftime('%H_%M_%S_%d_%m_%Y.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

def get_hash(image):
    cache_file = Path(f"{Path(__file__).parent.absolute()}\\cached_hash.txt")
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
        logging.info(f"Hashed {image}")
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
            logging.info(f"{a[0]} matched {b[0]}")

    if duplicates != []:
        for duplicate in duplicates:
            send2trash(str(duplicate).encode())
            logging.info(f"Deleted {duplicate}")
    else:
        pass

def get_attribute(dir):
    current_dir = Path(dir)
    time_modified = []
    for path in current_dir.iterdir():
        info = path.stat()
        info_stat = [path, info.st_ctime]
        time_modified.append(info_stat)

    time_modified.sort(key=lambda time: time[1])
    return time_modified


def update(file, directory, attributes, serial, name):
    bak_name = f"{directory}\\bak_{str(serial)}{str(name.suffix)}"
    rename(file, bak_name)
    for index, element in enumerate(attributes):
        if element[0] == Path(file):
            attributes[index][0] = Path(bak_name)

renamed = 0
def rename_dir(directory):
    cute_name = "_".join(directory.split("\\")[2:])
    serial = 1
    delete_duplicate(directory)
    exceptions = ['.ini', '.db']
    attributes = get_attribute(directory)
    for name in attributes:
        actual_file_name = name[0]
        if actual_file_name.suffix in exceptions or actual_file_name.is_dir():
            continue
        pic_name = f"{cute_name}_{str(serial)}"
        file_name = f"{directory}\\{pic_name}{str(actual_file_name.suffix)}"
        if actual_file_name.stem != pic_name and Path(file_name).exists():
            update(file_name, directory, attributes, serial, actual_file_name)
        rename(actual_file_name, file_name)
        global renamed
        renamed += 1
        serial += 1

try:
    working_dirs = ["D:\\Pics\\UwU", "D:\\Pics\\Wallpapers", "D:\\Pics\\Pro"]
    for working_dir in working_dirs:
        for itered_dir in walk(working_dir):
            rename_dir(itered_dir[0])
    logging.info(f"Processed {renamed} file(s)")

    notification.notify(
        title="Just took care of your stuff",
        message=f"Processed {renamed} file(s), senpai UwU",
        app_name="UwU Renamer",
        app_icon="ico//icon.ico",
        timeout=5)

except Exception as error:
    logging.error(error)
    notification.notify(
        title="Something went wrong, senpai :(",
        message=f"Exception: {error}",
        app_name="UwU Renamer",
        app_icon="ico//icon.ico",
        timeout=10)
