import pathlib
from typing import Generator, List

import click

from recipe_transformer.corpus import mmf


def really_simple_sentence_tokenizer(instructions: str) -> List[str]:
    pass


def sentence_per_line(filenames: List[str]) -> Generator[str, None, None]:
    for filename in filenames:
        for recipe in mmf.split_recipes(filename):
            parsed_recipe = mmf.parse(recipe)
            for ingredient in parsed_recipe["ingredients"]:
                yield ingredient + "\n"
            yield "\n"


def recipe_per_line(filenames: List[str]) -> Generator[str, None, None]:
    for filename in filenames:
        for recipe in mmf.split_recipes(filename):
            parsed_recipes = mmf.parse(recipe)
            ingredients = " ".join(parsed_recipes["ingredients"])
            instructions = parsed_recipes["instructions"]
            line = f"<BOS> {ingredients} {instructions} <EOS>\n"
            yield line


@click.command()
@click.argument("filenames", nargs=-1, type=click.Path(exists=True))
@click.argument("output_path", nargs=1, type=click.Path(exists=False))
def main(filenames: List[str], output_path: pathlib.Path):
    with open(output_path, "w") as fo:
        fo.writelines(list(recipe_per_line(filenames)))


if __name__ == "__main__":
    main()
