# coding: utf-8

import os

class Project:
    def __init__(self):
        self.__dir = os.getcwd()

    def dir(self) -> str:
        return self.__dir

