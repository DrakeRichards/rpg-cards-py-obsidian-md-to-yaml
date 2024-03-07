"""
Convert an Obsidian page object to an object that will conform with the schema for rpg-cards-typst-templates.
"""

import json
from abc import ABC
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

from jsonschema import ValidationError, validate

import src.obsidian_rpg as obsidian_rpg


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

    items: List[ListItem]
    title: str = ""


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


@dataclass
class TypstCharacter(rpgCardInterface):
    """
    For exporting characters to rpg-cards-typst-templates.
    This assumes that the input character page uses my standard template.
    Other character page types will have their own classes.
    """

    name: str
    bodyText: str
    image: str
    nameSubtext: str = ""
    imageSubtext: str = ""
    lists: List[CardList] = field(default_factory=list)
    template: str = "landscape-content-left"
    bannerColor: str = "#800000"  # maroon

    def __init__(self, character: obsidian_rpg.ObsidianCharacter):
        self.name = character.name
        self.bodyText = character.description.overview if character.description else ""
        self.image = character.image
        self.nameSubtext = character.physicalInfo.job
        self.imageSubtext = (
            f"{character.physicalInfo.gender} {character.physicalInfo.race}"
        )
        self.lists = TypstCharacter.__get_lists(character)

    @staticmethod
    def __get_lists(character: obsidian_rpg.ObsidianCharacter) -> List[CardList]:
        lists = [
            TypstCharacter.__get_personality_list(character),
            TypstCharacter.__get_secondary_list(character),
        ]
        return lists

    @staticmethod
    def __get_personality_list(character: obsidian_rpg.ObsidianCharacter) -> CardList:
        return CardList(
            items=[
                CardList.ListItem(value=character.personality.quirk, name="Quirk"),
                CardList.ListItem(value=character.personality.likes, name="Likes"),
                CardList.ListItem(
                    value=character.personality.dislikes, name="Dislikes"
                ),
            ],
            title="",
        )

    @staticmethod
    def __get_secondary_list(character: obsidian_rpg.ObsidianCharacter) -> CardList:
        """
        Second list is an unordered and untitled list of location and group membership.
        """
        secondList = CardList(items=[], title="")
        if character.location:
            locationItem = CardList.ListItem(value=character.location, name="Location")
            secondList.items.append(locationItem)
        if character.groupName != "":
            groupNameItem = CardList.ListItem(
                value=character.groupName, name="Member of"
            )
            secondList.items.append(groupNameItem)
        return secondList


def fromPageObject(pageObject: obsidian_rpg.RpgData) -> rpgCardInterface:
    """
    Converts an Obsidian page object to a rpgCardInterface object.
    """
    if isinstance(pageObject, obsidian_rpg.ObsidianCharacter):
        return TypstCharacter(pageObject)
    if isinstance(pageObject, obsidian_rpg.ObsidianItem):
        raise NotImplementedError("ObsidianItem is not yet implemented.")
    if isinstance(pageObject, obsidian_rpg.ObsidianLocation):
        raise NotImplementedError("ObsidianLocation is not yet implemented.")
    else:
        raise ValueError(f"Unknown page type: {type(pageObject)}")
