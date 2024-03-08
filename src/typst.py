import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

from jsonschema import Draft7Validator


@dataclass
class CardList:
    """
    A list for use in rpg-cards-typst-templates.
    """

    @dataclass
    class Item:
        """
        A list item for use in rpg-cards-typst-templates.
        """

        value: str
        name: str = ""

    items: List[Item]
    title: str = ""
    style: str = "plain"  # The style of the list as defined in the schema.


@dataclass
class Card:
    """
    Class used to export data to rpg-cards-typst-templates.
    """

    template: str
    name: str
    body_text: str
    banner_color: str = "#800000"  # maroon
    image: str = ""
    name_subtext: str = ""
    image_subtext: str = ""
    lists: List[CardList] = field(default_factory=list)

    def validate_schema(self) -> bool:
        # Get the schema from the repository.
        schema_file: Path = Path("rpg-cards-typst-templates/schemas/data.schema.json")
        with open(schema_file, "r") as file:
            schema: dict[str, str] = json.load(file)
            # The schema assumes that the data is a list of cards.
            # Since this is a single card, we need to wrap it in a list.
            card: dict = {"cards": [asdict(self)]}
            card_validator = Draft7Validator(schema)
            errors = sorted(card_validator.iter_errors(card), key=lambda e: e.path)
            if len(errors) == 0:
                return True
            for error in errors:
                print(error)
            return False
