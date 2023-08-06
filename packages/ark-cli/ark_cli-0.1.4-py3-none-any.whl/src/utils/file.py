# coding: utf-8

import os
import shutil
from typing import List
from src.definitions.platform import Platform
from src.utils.str import rreplace


def find_files_recursively(path: str, pred = None, ls = None) -> List[str]:
    if ls == None:
        ls = []

    if not os.path.isdir(path):
        return ls

    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isdir(p):
            find_files_recursively(p, pred, ls)
        elif os.path.isfile(p):
            if not pred or pred(p):
                ls.append(p)

    return ls


def find_dirs_recursively(path: str, pred = None, ls = None) -> List[str]:
    if ls == None:
        ls = []

    if not os.path.isdir(path):
        return ls

    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isdir(p):
            if not pred or pred(p):
                ls.append(p)

            find_dirs_recursively(p, pred, ls)

    return ls


def read_text_file(file: str) -> str:
    with open(file, mode = 'r') as f:
       return f.read()


def write_text_file(file: str, content: str) -> str:
    with open(file, mode = 'w') as f:
       return f.write(content)


def update_dir_tree(dir: str, src_part: str, dst_part: str) -> str:
    base_path = rreplace(dir, Platform.PATH_SEP + src_part, '', 1)
    src_part_prefix = src_part.split(Platform.PATH_SEP)[0]

    temp_dir = os.getcwd() + Platform.PATH_SEP + Platform.ARK_TEMP_FOLDER

    shutil.rmtree(temp_dir, True)
    shutil.move(dir, temp_dir)
    shutil.rmtree(base_path + Platform.PATH_SEP + src_part_prefix, True)
    shutil.move(temp_dir, base_path + Platform.PATH_SEP + dst_part)
    shutil.rmtree(temp_dir, True)

