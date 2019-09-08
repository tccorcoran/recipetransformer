import re
from typing import Generator, List, Union
import pathlib
from enum import Enum

MMF = Enum("MMF", "START END")

blankline = re.compile(r"(^\s+)|^$")


def mmf_reader(filename: pathlib.Path) -> Union[str, Enum]:
    with open(filename, encoding="latin-1") as fo:
        for line in fo:
            if line.startswith("MMMMM-----"):
                yield MMF.START
            elif line == "MMMMM\n":
                yield MMF.END
            else:
                yield line


def split_recipes(
    filename: pathlib.Path, remove_linebreaks=False
) -> Generator[List[str], None, None]:
    recipe = []
    for line in mmf_reader(filename):
        if line == MMF.END:
            if remove_linebreaks:
                yield list(filter(lambda x: blankline.match(x) is None, recipe))
            else:
                yield recipe
        elif line == MMF.START:
            recipe = []
        else:
            recipe.append(line.strip())
