"""
Abstract base class for data to be used in rpg-cards-typst-templates.
"""

from pathlib import Path
import json
from abc import ABC
from dataclasses import asdict, dataclass
from jsonschema import validate, ValidationError


@dataclass
class rpgCardInterface(ABC):
    """
    Abstract base class for data to be used in rpg-cards-typst-templates.
    """

    def template(self) -> str:
        return ""

    def bannerColor(self) -> str:
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
        # Get the schema from the repository.
        SCHEMA_FILE: Path = Path("rpg-cards-typst-templates/schemas/data.schema.json")
        with open(SCHEMA_FILE, "r") as file:
            schema = json.load(file)
            # The schema assumes that the data is a list of cards.
            # Since this is a single card, we need to wrap it in a list.
            card: dict = {"cards": [asdict(self)]}
            try:
                validate(instance=card, schema=schema)
                is_valid = True
            except ValidationError:
                is_valid = False
            if not is_valid:
                raise ValueError(
                    f"The character_typst object does not validate against the schema: '{SCHEMA_FILE}'"
                )
            return is_valid
