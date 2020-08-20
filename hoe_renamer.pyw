from pathlib import Path
from delete_duplicate import delete_duplicate
from os import rename, walk
from plyer import notification


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
        serial += 1

try:
    working_dirs = ["D:\\Pics\\UwU", "D:\\Pics\\Wallpapers", "D:\\Pics\\Pro"]
    for working_dir in working_dirs:
        for itered_dir in walk(working_dir):
            rename_dir(itered_dir[0])
    
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
