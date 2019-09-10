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


def parse(recipe):
    metadata = dict()
    ingredient_end = False
    ingredients = []
    instructions = ""
    for i, line in enumerate(recipe[1:]):
        if ":" in line and i < 4:
            metadata[line.split(":")[0].strip()] = line.split(":")[1].strip()
        elif re.match(r"\d", line.strip()) and not ingredient_end:
            ingredients.append(line.strip())
        elif not blankline.match(line):
            ingredients.append(line)
        elif blankline.match(line) and i > 4:
            ingredient_end = True
            instructions = " ".join(recipe[i:])
            break
    return {
        "metadata": metadata,
        "instructions": instructions,
        "ingredients": ingredients,
    }


mpa = dict.fromkeys(range(32))


def remove_ascii_control_chars(input_str: str) -> str:
    return input_str.translate(mpa)


def split_recipes(
    filename: pathlib.Path, remove_blanklines=False, keep_variations=False
) -> Generator[List[str], dict, None]:
    stats = {"recipes": 0, "lines": 0}
    recipe = []
    for line in mmf_reader(filename):
        if line == MMF.END:
            if not keep_variations:
                if len([x for x in recipe if x.startswith("MMMMM")]) > 2:
                    recipe = []
                    continue
            if remove_blanklines:
                stats["recipes"] += 1
                recipe = list(filter(lambda x: blankline.match(x) is None, recipe))
                stats["lines"] += len(recipe)
                yield recipe
            else:
                stats["recipes"] += 1
                stats["lines"] += len(recipe)
                yield recipe
            recipe = []

        elif line == MMF.START:
            continue  # TODO: do something here
        else:
            recipe.append(remove_ascii_control_chars(line.strip()))
    return stats
