# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:16:56 2022

@author: chris.kerklaan

We store a global cache, so we can just import this instead of typing everything.
We use pickle here to ensure it is not humanly readable.
"""


# First party imports
import pathlib
import pickle

# GLOBALS
OUR_PATH = pathlib.Path(__file__)
TRE_PATH = OUR_PATH.parent.parent


class GlobalCache:
    def __init__(self, name="cache"):
        self.file = TRE_PATH / (name + ".pickle")
        self.path = str(self.file)

        self.data = {}
        if not self.file.exists():
            self.write()

        self.load()
        for key, value in self.data.items():
            setattr(self, key, value)

    def __contains__(self, name):
        return name in self.data

    def __setitem__(self, name, data):
        self.data[name] = data
        self.write()
        setattr(self, name, data)

    def __getitem__(self, name):
        return self.data[name]

    def write(self):
        with open(self.path, "wb") as handle:
            pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(self.path, "rb") as handle:
            b = pickle.load(handle)
        self.data = b
