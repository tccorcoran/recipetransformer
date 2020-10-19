import re
from dataclasses import dataclass
from typing import Union

from measurement.base import MeasureBase
from measurement.measures import Distance as Length
from measurement.measures import Temperature, Time, Volume, Weight


class Count(MeasureBase):
    STANDARD_UNIT = "total"
    UNITS = {"large": 1.5, "small": 0.5, "medium": 1}
    ALIAS = {"large": "lg", "small": "sm", "medium": "med"}

    SI_UNITS = {""}


unit_aliases = dict(
    us_tbsp={"tbsp", "tb", "tablespoon", "tablespoons", "T"},
    us_tsp={"tsp", "ts", "teaspoon", "teaspoons"},
    us_cup={"c", "cup", "cups"},
    us_qt={"quart", "qt", "quarts"},
    pinch={"pn", "pinch", "pinches"},
    us_pint={"pint", "pt", "pints"},
    us_oz={"oz", "ounce", "ounces"},
    count={"lg", "med", "can", "cans", "packet", "packets", "sm"},
    lb={"lb", "lbs", "pound", "pounds"},
    kg={"kg", "kilograms", "kilogram", "kgs"},
)
unit_map = {}
for unit, aliases in unit_aliases.items():
    for alias in aliases:
        unit_map[alias] = unit

unit_pats = "|".join(f"({unit})" for unit in unit_map.keys())
measurement_pat = re.compile(f"((\d+\/\d+)|(\d+?( \d+\/\d+)?)) ({unit_pats})?")


class Ingredient(object):
    def __init__(
        self,
        text: str,
        measurement: Union[Count, Weight, Volume, Temperature, Length],
        ingredient: str,
        style: str = None,
    ):
        self.text = text
        self.measurement = measurement
        self.ingredient = ingredient
        self.style = style

    @classmethod
    def from_text(cls, text):
        text = text.strip()
        measurement_match = measurement_pat.search(text)
        measurement = ""
        ingredient = text

        if measurement_match:
            measurement = text[
                measurement_match.span()[0] : measurement_match.span()[1]
            ]
            ingredient = (
                text[: measurement_match.span()[0]]
                + text[measurement_match.span()[1] :]
            )
        return cls(text, measurement, ingredient.strip())
