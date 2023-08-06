# coding: utf-8

import os
import click
from functools import partial
from binaryornot.check import is_binary
from src.definitions.ark_definitions import ArkDefinitions
from src.definitions.platform import Platform
from src.models.project import Project
from src.utils.git import git_clone, git_cleanup
from src.utils.file import find_files_recursively, find_dirs_recursively, read_text_file, write_text_file, update_dir_tree

def __on_walk_project_file(file: str, package: str, platform: str):
    if not is_binary(file):
        text = read_text_file(file)
        text = text.replace(ArkDefinitions.PACKAGE_ANDROID if platform == Platform.ANDROID else ArkDefinitions.PACKAGE_IOS, package)
        text = text.replace(ArkDefinitions.PATH_ANDROID if platform == Platform.ANDROID else ArkDefinitions.PATH_IOS, package.replace('.', '/'))
        write_text_file(file, text)

        return True


def __on_walk_project_dir(dir: str, package: str, platform: str):
    platform_package_path = ArkDefinitions.PACKAGE_ANDROID if platform == Platform.ANDROID else ArkDefinitions.PACKAGE_IOS

    package_path = platform_package_path.replace('.', Platform.PATH_SEP)
    dst_package_path = package.replace('.', Platform.PATH_SEP)

    if dir.endswith(package_path):
        update_dir_tree(dir, package_path, dst_package_path)

        return True


def init(project: Project, name: str, platform: str, package: str):
    current_directory = os.getcwd()

    # list folders of current_directory
    dirs = list(filter(lambda x: os.path.isdir(x), os.listdir(current_directory)))

    # check folder exists
    if name in dirs:
       click.echo('Error: Directory name "{0}" already exists!'.format(name))
       exit(-1)

    project_dir = '{0}{1}{2}'.format(current_directory, Platform.PATH_SEP, name)

    # download latest ark project from branch 'main'
    git_clone(ArkDefinitions.REPO_ANDROID if platform == 'android' else ArkDefinitions.REPO_IOS, project_dir, 'main')

    # clear .git, .github
    git_cleanup(project_dir)

    # walk all text file and replace package
    find_files_recursively(project_dir, partial(__on_walk_project_file, package = package, platform = platform))

    # walk all dirs end with ark package
    find_dirs_recursively(project_dir, partial(__on_walk_project_dir, package = package, platform = platform))

    click.echo('Project generated at: {0}'.format(project_dir))
    click.echo('Done!')

