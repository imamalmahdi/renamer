from pathlib import Path
from delete_duplicate import delete_duplicate
from os import rename
from win10toast import ToastNotifier


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

cute_name = "UwU"
notification = ToastNotifier()

try:
    attributes = get_attribute(directory)
    serial = 1

    delete_duplicate()
    for name, useless in attributes:
        if name.suffix == ".ini":
            continue
        file_name = f"{directory}\\{cute_name}_{str(serial)}{str(name.suffix)}"
        rename(name, file_name)
        serial += 1
    notification.show_toast(
        title="UwU Renamer", msg="Just took care of your stuff, senpai UwU", icon_path="ico//icon.ico", duration=5)
except:
    notification.show_toast(
        title="UwU Renamer", msg="Something went wrong. Save me, senpai :(", icon_path="ico//icon.ico", duration=10)
