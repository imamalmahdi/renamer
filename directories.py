from pathlib import Path
from images import ImageFile
from itertools import combinations
from send2trash import send2trash
from os import rename
from config import LOG_FILENAME
import time
import logging

IMAGE_FORMATS = [
    ".jpg", '.jpeg', '.png', '.webp'
]

EXCLUDE_LIST = ['.ini', '.db']
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

class Directory:
    def __init__(self, dir):
        self.path = Path(dir)
        self.path_str = dir
        self.name = "_".join(dir.split("\\")[2:])
        self.attributes = self.__get_attributes()

    def __delete_duplicate(self):
        images = self.path.iterdir()

        image_and_hashes = []

        for image in images:
            if image.suffix not in IMAGE_FORMATS or image.is_dir():
                continue
            else:
                try:
                    temp_tupol = [image, ImageFile(image).hash]
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

    def __get_attributes(self):
        self.__delete_duplicate()
        data = {}
        for file_path in self.path.iterdir():
            if file_path.suffix in EXCLUDE_LIST or file_path.is_dir():
                continue
            info = file_path.stat()
            time_created = info.st_ctime
            if time_created in data.keys():
                time_created += 0.000001
            data[time_created] = file_path
        return dict(sorted(data.items()))
    
    def __update(self, duplicate_file, serial, name):
        while True:
            bak_name = f"{self.path_str}\\bak_{str(serial)}{str(name.suffix)}"
            if Path(bak_name).exists():
                serial -= 1
            else: break
        rename(duplicate_file, bak_name)
        logging.info(f"Renamed {duplicate_file} to {bak_name} as backup")
        for token in self.attributes:
            if self.attributes[token] == Path(duplicate_file):
                self.attributes[token] == Path(bak_name)
                break

    def rename_dir(self):
        serial = 1
        for token in self.attributes:
            actual_file_name = self.attributes[token]
            pic_name = f"{self.name}_{str(serial)}"
            file_name = f"{self.path_str}\\{pic_name}{str(actual_file_name.suffix)}"
            if actual_file_name.stem != pic_name and Path(file_name).exists():
                self.__update(file_name, serial, actual_file_name)
            rename(actual_file_name, file_name)
            logging.info(f"Renamed {actual_file_name} to {file_name}")
            serial += 1
