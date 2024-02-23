"""
Convert an Obsidian page object to an object that will conform with the schema for rpg-cards-typst-templates.
"""

from dataclasses import dataclass, field
from typing import List
from src.obsidian_page_types import ObsidianCharacter as ObsidianCharacter
from src.typst_card_abc import rpgCardInterface


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
    template: str = "character"

    def __init__(self, character: ObsidianCharacter):
        self.name = character.name
        self.bodyText = character.description.overview if character.description else ""
        self.image = character.image
        self.nameSubtext = character.physicalInfo.job
        self.imageSubtext = (
            f"{character.physicalInfo.gender} {character.physicalInfo.race}"
        )
        self.lists = TypstCharacter.__get_lists(character)

    @staticmethod
    def __get_lists(character: ObsidianCharacter) -> List[CardList]:
        lists = [
            TypstCharacter.__get_personality_list(character),
            TypstCharacter.__get_secondary_list(character),
        ]
        return lists

    @staticmethod
    def __get_personality_list(character: ObsidianCharacter) -> CardList:
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
    def __get_secondary_list(character: ObsidianCharacter) -> CardList:
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
