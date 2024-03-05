"""
Abstract base class for data to be used in rpg-cards-typst-templates.
"""

import requests
from abc import ABC
from dataclasses import asdict, dataclass
from jsonschema import validate, ValidationError


@dataclass
class rpgCardInterface(ABC):
    """
    Abstract base class for data to be used in rpg-cards-typst-templates.
    """

    SCHEMA_URL = "https://raw.githubusercontent.com/DrakeRichards/rpg-cards-typst-templates/main/schemas/data.schema.json"

    def template(self) -> str:
        return ""

    def name(self) -> str:
        return ""

    def bodyText(self) -> str:
        return ""

    def image(self) -> str:
        return ""

    def nameSubtext(self) -> str:
        return ""

    def imageSubtext(self) -> str:
        return ""

    def lists(self) -> list:
        return []

    def validateSchema(self) -> bool:
        schema = requests.get(self.SCHEMA_URL).json()
        # The schema assumes that the data is a list of cards.
        # Since this is a single card, we need to wrap it in a list.
        card: dict = {"cards": [asdict(self)]}
        try:
            validate(card, schema)
            is_valid = True
        except ValidationError:
            is_valid = False
        if not is_valid:
            raise ValueError(
                f"The character_typst object does not validate against the schema: '{self.SCHEMA_URL}'"
            )
        return is_valid