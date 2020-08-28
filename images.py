from config import CURRENT_DIR, CACHE_FILE, LOG_FILENAME
from PIL import Image
from imagehash import phash
import json
import logging

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

class ImageFile:
    def __init__(self, image_path):
        self.path = image_path
        self.hash = str(self.__get_hash())
    def __get_hash(self):
        if not CACHE_FILE.exists():
            with open(CACHE_FILE, "w"): pass
            cached_data = []
        else:
            try: 
                cached_data = json.loads(CACHE_FILE.read_text())
            except:
                cached_data = []
        
        image_date = self.path.stat().st_ctime
        image_size = self.path.stat().st_size
        for data in cached_data:
            if image_date == data[0][0] and image_size == data[0][1]:
                return data[1]
        else:
            the_image = Image.open(self.path)
            the_hash = phash(the_image)
            image_info = ((image_date, image_size), str(the_hash), self.path.name)
            cached_data.append(image_info)
            CACHE_FILE.write_text(json.dumps(cached_data, indent=4))
            logging.info(f"Hashed {self.path}")
            return the_hash