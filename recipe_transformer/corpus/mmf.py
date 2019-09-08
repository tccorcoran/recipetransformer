import re
from typing import Generator, List, Union
import pathlib
from enum import Enum

MMF = Enum("MMF", "START END")


def mmf_reader(filename: pathlib.Path) -> Union[str, Enum]:
    with open(filename, encoding="latin-1") as fo:
        for line in fo:
            if line.startswith("MMMMM-----"):
                yield MMF.START
            elif line == "MMMMM\n":
                yield MMF.END
            else:
                yield line


def split_recipes(filename: pathlib.Path) -> Generator[List[str], None, None]:
    recipe = []
    for line in mmf_reader(filename):
        if line == MMF.END:
            yield recipe
        elif line == MMF.START:
            recipe = []
        else:
            recipe.append(line.strip())
