import os
import time
import json


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)


def temp_name():
    solt = time.time_ns() % (10**6)
    return 'temp-{0:06d}'.format(solt)


def save_safely(content, path):
    # save content to file with temp random name and then rename it
    temp = temp_name()
    with open(temp, "w") as f:
        json.dump(content, f)
    if os.path.exists(path):
        os.remove(path)
    os.rename(temp, path)


def rename_safely(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(src, dst)


def clear_garbage(directory, rx):
    for item in os.scandir(directory):
        if not item.is_file():
            continue
        if not rx.match(item.name):
            os.remove(item.path)
