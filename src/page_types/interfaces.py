"""
Interface classes to export to other programs.
"""

from src.page_types.character import Character
from dataclasses import dataclass


@dataclass
class TpystRpgCardListItem:
    """
    A list item for use in rpg-cards-typst-templates.
    """

    value: str
    name: str = ""


@dataclass
class TypstRpgCardList:
    """
    A list for use in rpg-cards-typst-templates.
    """

    items: list[TpystRpgCardListItem]
    title: str = ""


@dataclass
class TypstCharacter:
    """
    For exporting characters to rpg-cards-typst-templates.
    The schema is defined in `schemas/rpg-cards-typst-templates/schemas/character.schema.json`.
    """

    name: str
    bodyText: str
    image: str
    nameSubtext: str = ""
    imageSubtext: str = ""
    lists: list[TypstRpgCardList] = []

    # Initialize an instance of the class given a Character object.
    def __init__(self, character: Character):
        # Required fields
        self.name = character.name
        self.bodyText = character.description.overview
        self.image = character.image

        # Optional fields
        if character.physicalInfo:
            self.nameSubtext = character.physicalInfo.job
            self.imageSubtext = (
                f"{character.physicalInfo.gender} {character.physicalInfo.race}"
            )

        # Add lists
        # First list: Quirk, Likes, Dislikes
        if character.personality:
            self.lists.append(
                TypstRpgCardList(
                    items=[
                        TpystRpgCardListItem(
                            value=character.personality.quirk, name="Quirk"
                        ),
                        TpystRpgCardListItem(
                            value=character.personality.likes, name="Likes"
                        ),
                        TpystRpgCardListItem(
                            value=character.personality.dislikes, name="Dislikes"
                        ),
                    ],
                    title="Personality",
                )
            )
        # Second list: Location
        if character.location:
            self.lists.append(
                TypstRpgCardList(
                    items=[TpystRpgCardListItem(value=character.location)],
                    title="Location",
                )
            )
