"""
Convert a Character object to an object that will conform with the `rpg-cards-typst-templates/character` schema.
"""

from src.obsidian_page_types import Character as ObsidianCharacter
from jsonschema import validate, ValidationError
from json import load
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CardList:
    """
    A list for use in rpg-cards-typst-templates.
    """

    @dataclass
    class ListItem:
        """
        A list item for use in rpg-cards-typst-templates.
        """

        value: str
        name: str = ""

    items: list[ListItem]
    title: str = ""


@dataclass
class Character:
    """
    For exporting characters to rpg-cards-typst-templates.
    The schema is defined in `schemas/rpg-cards-typst-templates/schemas/character.schema.json`.
    """

    name: str
    bodyText: str
    image: str
    nameSubtext: str = ""
    imageSubtext: str = ""
    lists: list[CardList] | None = None

    # Initialize an instance of the class given a Character object.
    @classmethod
    def from_character(cls, character: ObsidianCharacter):

        # Required fields
        character_typst = cls(
            name=character.name,
            bodyText=(character.description.overview if character.description else ""),
            image=character.image,
        )

        # Optional fields
        if character.physicalInfo:
            character_typst.nameSubtext = character.physicalInfo.job
            character_typst.imageSubtext = (
                f"{character.physicalInfo.gender} {character.physicalInfo.race}"
            )

        # Add lists
        # First list: Quirk, Likes, Dislikes
        if character.personality:
            character_typst.lists = []
            character_typst.lists.append(
                CardList(
                    items=[
                        CardList.ListItem(
                            value=character.personality.quirk, name="Quirk"
                        ),
                        CardList.ListItem(
                            value=character.personality.likes, name="Likes"
                        ),
                        CardList.ListItem(
                            value=character.personality.dislikes, name="Dislikes"
                        ),
                    ],
                    title="Personality",
                )
            )
        # Second list: Location
        if character.location:
            # Initialize the array if it doesn't exist.
            if not character_typst.lists:
                character_typst.lists = []
            character_typst.lists.append(
                CardList(
                    items=[
                        CardList.ListItem(value=character.location, name="Location")
                    ],
                    title="",
                )
            )

        # Validate the character_typst object against the schema.
        schema_location = (
            "schemas/rpg-cards-typst-templates/schemas/character.schema.json"
        )
        # Construct a path based on this file's location.
        project_root = Path(__file__).parent.parent
        schema_path = Path(project_root, schema_location)
        character_dict = asdict(character_typst)
        with open(schema_path) as file:
            schema = load(file)
        try:
            validate(character_dict, schema)
            is_valid = True
        except ValidationError:
            is_valid = False
        if not is_valid:
            raise ValueError(
                f"The character_typst object does not validate against {schema_location}."
            )
        return character_typst
