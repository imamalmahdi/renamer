from pathlib import Path
from datetime import datetime
import json

CURRENT_DIR = Path(__file__).parent.absolute()
LOG_FILENAME = f"{CURRENT_DIR}/logs/" + datetime.now().strftime('%H_%M_%S_%d_%m_%Y.log')
CACHE_FILE = Path(f"{CURRENT_DIR}/cached_hash.txt")

def load_setting():
    settings_file = Path(f"{CURRENT_DIR}/settings.json")
    return json.loads(settings_file.read_text())