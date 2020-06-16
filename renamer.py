from pathlib import Path
from delete_duplicate import delete_duplicate
from os import rename, walk


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
    delete_duplicate()

    attributes = get_attribute(directory)
    for name in attributes:
        actual_file_name = name[0]
        if actual_file_name.suffix == ".ini" or actual_file_name.is_dir():
            continue
        pic_name = f"{cute_name}_{str(serial)}"
        file_name = f"{directory}\\{pic_name}{str(actual_file_name.suffix)}"
        if actual_file_name.stem != pic_name and Path(file_name).exists():
            update(file_name, directory, attributes, serial, actual_file_name)
        rename(actual_file_name, file_name)
        serial += 1

working_dir = input("Enter a directory: ")
print("Now, wait a bit...")
for itered_dir in walk(working_dir):
    rename_dir(itered_dir[0])

print("Done!")