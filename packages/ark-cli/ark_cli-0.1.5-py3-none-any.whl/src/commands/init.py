# coding: utf-8

import os
import shutil
import click
from functools import partial
from binaryornot.check import is_binary
from src.definitions.ark_definitions import ArkDefinitions
from src.definitions.platform import Platform
from src.models.project import Project
from src.models.ios_config import IOSConfig
from src.utils.git import git_clone, git_cleanup
from src.utils.file import find_files_recursively, find_dirs_recursively, read_text_file, write_text_file, update_dir_tree


def __on_walk_project_file_android(file: str, package: str):
    if not is_binary(file):
        text = read_text_file(file)
        text = text.replace(ArkDefinitions.PACKAGE_ANDROID, package)
        text = text.replace(ArkDefinitions.PATH_ANDROID, package.replace('.', '/'))
        write_text_file(file, text)

        return True


def __on_walk_project_file_ios(file: str, ios_config: IOSConfig):
    if not is_binary(file):
        text = read_text_file(file)
        text = text.replace(ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
        text = text.replace(ArkDefinitions.PATH_IOS, ios_config.app_identifier.replace('.', '/'))
        if not file.endswith('.podspec'):
            text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)

        write_text_file(file, text)

        return True


def __on_walk_project_dir(dir: str, package: str, platform: str):
    platform_package_path = ArkDefinitions.PACKAGE_ANDROID if platform == Platform.ANDROID else ArkDefinitions.PACKAGE_IOS

    package_path = platform_package_path.replace('.', Platform.PATH_SEP)
    dst_package_path = package.replace('.', Platform.PATH_SEP)

    if dir.endswith(package_path):
        update_dir_tree(dir, package_path, dst_package_path)

        return True


def __process_android_project(project_dir: str, package: str, platform: str):
    # walk all text file and replace package
    find_files_recursively(project_dir, partial(__on_walk_project_file_android, package = package))

    # walk all dirs end with ark package
    find_dirs_recursively(project_dir, partial(__on_walk_project_dir, package = package, platform = platform))

    click.echo('Project generated at: {0}'.format(project_dir))
    click.echo('\nDone!')


def __process_ios_project(ios_config: IOSConfig):
    def process_sources(file: str):
        if file.endswith('.swift'):
            text = read_text_file(file)
            text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
            text = text.replace(ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
            write_text_file(file, text)

    def process_tests(file: str):
        if file.endswith('.swift'):
            text = read_text_file(file)
            text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
            text = text.replace(ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
            text = text.replace('import ARK', 'import {0}'.format(ios_config.project_name))
            write_text_file(file, text)

    def process_configs(file: str):
        if file.endswith('.xcconfig'):
            text = read_text_file(file)
            text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
            text = text.replace(ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
            write_text_file(file, text)

    # walk all text file and replace package
    find_files_recursively(ios_config.project_dir, partial(__on_walk_project_file_ios, ios_config = ios_config))

    env_file = '{0}{1}.env'.format(ios_config.project_dir, Platform.PATH_SEP)
    text = read_text_file(env_file)
    text = text.replace('tao.tang@thoughtworks.com', ios_config.apple_id)
    # text = text.replace(ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
    text = text.replace('25EZUPR5QA', ios_config.team_id)
    text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
    write_text_file(env_file, text)

    pod_file = '{0}{1}Podfile'.format(ios_config.project_dir, Platform.PATH_SEP)
    text = read_text_file(pod_file)
    text = text.replace(ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
    write_text_file(pod_file, text)

    sources_path = '{0}{1}Sources'.format(ios_config.project_dir, Platform.PATH_SEP)
    find_dirs_recursively(sources_path, process_sources)

    tests_path = '{0}{1}Tests'.format(ios_config.project_dir, Platform.PATH_SEP)
    find_dirs_recursively(tests_path, process_tests)

    configs_path = '{0}{1}Configs'.format(ios_config.project_dir, Platform.PATH_SEP)
    find_dirs_recursively(configs_path, process_configs)

    shutil.rmtree('{0}{1}{2}.xcworkspace'.format(ios_config.project_dir, Platform.PATH_SEP, ArkDefinitions.PROJECT_NAME_IOS), True)

    click.echo('Project generated at: {0}'.format(ios_config.project_dir))
    click.echo('There are some steps you need to do manually:')
    click.echo('1. Open ARK-iOS.xcodeproj with XCode')
    click.echo('2. Rename project to "{0}" and select "Rename" when "Rename project content items?" alert show'.format(ios_config.project_name))
    click.echo('3. Delete the existing "{0}" scheme'.format(ArkDefinitions.PROJECT_NAME_IOS))
    click.echo('4. Add a new scheme named "{0}" and make it shared'.format(ios_config.project_name))
    click.echo('5. Land at "General" of {0}Tests target and select "{0}" as "Host Application"'.format(ios_config.project_name))
    click.echo('6. Run "bundle exec pod install"')
    click.echo('\nDone')


def __extract_ios_config(project_dir: str, name: str, platform: str, package: str) -> IOSConfig:
    if platform != Platform.IOS:
        return None

    ios_config = IOSConfig()
    ios_config.app_identifier = package
    ios_config.project_name = name
    ios_config.project_dir = project_dir
    ios_config.apple_id = click.prompt('Please enter apple id')
    ios_config.team_id = click.prompt('Please enter team id')

    return ios_config


def init(name: str, platform: str, package: str):
    current_directory = os.getcwd()

    # list folders of current_directory
    dirs = list(filter(lambda x: os.path.isdir(x), os.listdir(current_directory)))

    # check folder exists
    if name in dirs:
       click.echo('Error: Directory name "{0}" already exists!'.format(name))
       exit(-1)

    project_dir = '{0}{1}{2}'.format(current_directory, Platform.PATH_SEP, name)

    ios_config = __extract_ios_config(project_dir, name, platform, package)

    # download latest ark project from branch 'main'
    git_clone(ArkDefinitions.REPO_ANDROID if platform == Platform.ANDROID else ArkDefinitions.REPO_IOS, project_dir, 'main')

    # clear .git, .github
    git_cleanup(project_dir)

    # different process on each platform
    if platform == Platform.ANDROID:
        __process_android_project(project_dir, package, platform)
    else:
        __process_ios_project(ios_config)

