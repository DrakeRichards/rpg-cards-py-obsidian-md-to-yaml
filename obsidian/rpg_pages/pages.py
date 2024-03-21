from enum import Enum

from ..parser import MarkdownData
from .character import Character
from .item import Item
from .location import Location
from .rpg_data_abc import RpgData


class PageTypes(Enum):
    CHARACTER = "character"
    ITEM = "item"
    LOCATION = "location"
    UNKNOWN = "unknown"


def get_page_type(text: str) -> PageTypes:
    """
    Identify the type of an Obsidian page based on its frontmatter tags.
    """
    page = MarkdownData(text)
    if len(page.tags) == 0:
        return PageTypes.UNKNOWN
    if "character" in page.tags:
        return PageTypes.CHARACTER
    elif "item" in page.tags:
        return PageTypes.ITEM
    elif "location" in page.tags:
        return PageTypes.LOCATION
    else:
        return PageTypes.UNKNOWN


def new_page(text: str) -> RpgData:
    """Main function for creating a new Obsidian page object.

    Args:
        text (str): The text of the markdown file.

    Raises:
        ValueError: If the page type is not recognized.

    Returns:
        RpgData: An Obsidian page object.
    """
    page_type = get_page_type(text)
    markdown_data = MarkdownData(text)
    match page_type:
        case PageTypes.CHARACTER:
            return Character(markdown_data)
        case PageTypes.ITEM:
            return Item(markdown_data)
        case PageTypes.LOCATION:
            return Location(markdown_data)
        case _:
            raise ValueError(f"Page type {page_type} not recognized.")
