from __future__ import annotations
from typing import *

from datetime import datetime

import json 

import tempfile

from tqdm import tqdm

class Checkpoint:
    def __init__(self, it: int, output: Any, *kwargs) -> None:
        self.timestamp = datetime.now()
        self.it = it
        self.output = output
        self.variables = kwargs

class CheckpointSaver:
    def __init__(self, function: function, save_per: int) -> None:
        self.function = function
        self.it = 0
        self.save_per = save_per
        self.file = tempfile.NamedTemporaryFile("w+")

    def call_function(self, *args):
        self.function(*args)

    def set_tqdm(self, desc: str = None, total: int = None, miniters: int = None, disable: bool = None, unit: str = None):
        self.tqdm = {
            "desc": desc,
            "total": total,
            "miniters": miniters,
            "disable": disable,
            "unit": unit,
        }

    def iterate(self, *args):
        obj = self.call_function(*args)

        self.it += 1
    
    def iterate_for(self, args_list: Iterator):
        for _ in tqdm(args_list):
            self.call_function(args_list)

# c = CheckpointSaver(lambda x: print(x * 2), 2)
# c.call_function(3)