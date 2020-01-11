from pathlib import Path
from delete_duplicate import delete_duplicate
from os import rename
from plyer import notification


def get_attribute(dir):
    current_dir = Path(dir)
    time_modified = []
    for path in current_dir.iterdir():
        info = path.stat()
        info_stat = (path, info.st_ctime)
        time_modified.append(info_stat)

    time_modified.sort(key=lambda time: time[1])
    return time_modified


directory = "D:\\Pics\\UwU"


try:
    attributes = get_attribute(directory)
    serial = 1
    attempt = 1
    delete_duplicate()

    cute_name = "bak"
    while attempt <= 2:
        if attempt == 2:
            serial = 1
            attributes = get_attribute(directory)
            cute_name = "UwU"
        for name, useless in attributes:
            if name.suffix == ".ini":
                continue
            file_name = f"{directory}\\{cute_name}_{str(serial)}{str(name.suffix)}"
            rename(name, file_name)
            serial += 1
        attempt += 1
    notification.notify(
        title="Just took care of your stuff",
        message="Hope you are happy, senpai UwU",
        app_name="UwU Renamer",
        app_icon="ico//icon.ico",
        timeout=5)
except Exception as error:
    notification.notify(
        title="Something went wrong, senpai :(",
        message=f"Exception: {error}",
        app_name="UwU Renamer",
        app_icon="ico//icon.ico",
        timeout=10)
