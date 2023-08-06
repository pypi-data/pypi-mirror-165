# coding: utf-8

import shutil
from git import Repo, RemoteProgress
from tqdm import tqdm


class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count = None, message = ''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def git_clone(url: str, to_path: str, branch: str):
    Repo.clone_from(url, to_path, progress = CloneProgress(), branch = branch)


def git_cleanup(project_dir):
    # remove 
    shutil.rmtree('{0}/.git'.format(project_dir), True)
    shutil.rmtree('{0}/.github'.format(project_dir), True)
