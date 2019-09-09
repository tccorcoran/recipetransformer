from typing import List, Generator
from recipe_transformer.corpus import mmf


def really_simple_sentence_tokenizer(instuctions: str) -> List[str]:
    pass


def sentence_per_line(filenames: List[str]) -> Generator[str, None, None]:
    for filename in filenames:
        for recipe in mmf.split_recipes(filename):
            parsed_recipe = mmf.parse(recipe)
            for ingreident in parsed_recipe["ingredients"]:
                yield ingreident + "\n"
            yield "\n"
