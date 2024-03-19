from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from dacite import from_dict

import typst
from obsidian.parser import MarkdownData
from utils.dict import get_lower_keys


@dataclass
class RpgData(ABC):
    """
    Base class for each of the types of Obsidian pages.
    """

    input_data: MarkdownData | str

    @property
    def markdown_data(self) -> MarkdownData:
        if isinstance(self.input_data, str):
            return MarkdownData(self.input_data)
        return self.input_data

    @property
    def name(self) -> str:
        # The name of the character should be H1, which is the key of the top-level element.
        return list(self.markdown_data.headers.keys())[0]

    @property
    def description(self) -> str:
        # There is a description header, and it's a string.
        if "Description" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Description"], str
        ):
            return self.markdown_data.headers["Description"]
        # There is no description header, but the top-level header's content is a string.
        if self.name in self.markdown_data.headers.keys() and isinstance(
            self.markdown_data.headers[self.name], str
        ):
            return self.markdown_data.headers[self.name]  # type: ignore
        return ""

    @property
    def image(self) -> str:
        if self.markdown_data.images:
            return self.markdown_data.images[0]
        return ""

    @abstractmethod
    def to_typst_card(self) -> typst.Card:
        """
        Converts the data to a TypstCard.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")


@dataclass
class Item(RpgData):
    """This is the format that my Obsidian item template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs."""

    @property
    def cost(self) -> str:
        if "cost" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["cost"][0]
        return ""

    @property
    def weight(self) -> str:
        if "weight" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["weight"][0]
        return ""

    @property
    def damage(self) -> str:
        if "damage" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["damage"][0]
        return ""

    @property
    def range(self) -> str:
        if "range" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["range"][0]
        return ""

    @property
    def armor_class(self) -> str:
        if "armor-class" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["armor-class"][0]
        return ""

    @property
    def stealth(self) -> str:
        if "stealth" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["stealth"][0]
        return ""

    @property
    def magic_level(self) -> str:
        if "magic-level" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["magic-level"][0]
        return ""

    @property
    def traits(self) -> str:
        if "traits" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["traits"][0]
        return ""

    @property
    def properties(self) -> str:
        if "properties" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["properties"][0]
        return ""

    @property
    def rarity(self) -> str:
        if "rarity" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["rarity"][0]
        return ""

    @property
    def item_type(self) -> str:
        if "type" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["type"][0]
        return ""

    def to_typst_card(self) -> typst.Card:
        """
        Converts the ObsidianItem to a TypstCard.
        """
        return typst.Card(
            name=self.name,
            body_text=self.description,
            image=self.image,
            name_subtext=self.__get_name_subtext(),
            image_subtext="",
            lists=self.__get_lists(),
            banner_color="#195905",  # Lincoln Green
            template="landscape-content-right",
        )

    def __get_lists(self) -> list[typst.CardList]:
        lists = [
            # Basic properties
            typst.CardList(
                items=[
                    (
                        typst.CardList.Item(value=self.cost, name="Cost")
                        if self.cost
                        else typst.CardList.Item(value="", name="Cost")
                    ),
                    (
                        typst.CardList.Item(value=self.weight, name="Weight")
                        if self.weight
                        else typst.CardList.Item(value="", name="Weight")
                    ),
                    (
                        typst.CardList.Item(value=self.properties, name="Properties")
                        if self.properties
                        else typst.CardList.Item(value="", name="Properties")
                    ),
                ],
                title="",
            )
        ]
        # Optional properties for weapons and armor.
        # Some items might have these mixed in, so check for each of them individually.
        if self.damage or self.range:
            lists.append(
                typst.CardList(
                    items=[
                        (
                            typst.CardList.Item(value=self.damage, name="Damage")
                            if self.damage
                            else typst.CardList.Item(value="", name="Damage")
                        ),
                        (
                            typst.CardList.Item(value=self.range, name="Range")
                            if self.range
                            else typst.CardList.Item(value="", name="Range")
                        ),
                    ],
                    title="",
                )
            )
        if self.armor_class or self.stealth:
            lists.append(
                typst.CardList(
                    items=[
                        (
                            typst.CardList.Item(
                                value=self.armor_class, name="Armor Class"
                            )
                            if self.armor_class
                            else typst.CardList.Item(value="", name="Armor Class")
                        ),
                        (
                            typst.CardList.Item(value=self.stealth, name="Stealth")
                            if self.stealth
                            else typst.CardList.Item(value="", name="Stealth")
                        ),
                    ],
                    title="",
                )
            )
        return lists

    def __get_name_subtext(self) -> str:
        """
        Returns the name subtext for the item.
        """
        if self.traits:
            return self.traits
        name_subtext = ""
        if not self.item_type:
            # If the item has no type, then the other fields are probably mangled, so just return an empty string.
            return ""
        name_subtext += self.item_type
        if self.rarity:
            name_subtext += f", {self.rarity}"
        if self.magic_level:
            name_subtext += f", {self.magic_level}"
        if self.rarity:
            name_subtext += f", {self.rarity}"
        return name_subtext


@dataclass
class Location(RpgData):
    """
    This is the format that my Obsidian location template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs.
    """

    @property
    def occupants(self) -> str:
        if "Occupants" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Occupants"], str
        ):
            return self.markdown_data.headers["Occupants"]
        return ""

    @property
    def story_hook(self) -> str:
        if "Story Hook" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Story Hook"], str
        ):
            return self.markdown_data.headers["Story Hook"]
        return ""

    @property
    def location(self) -> str:
        if "location" in self.markdown_data.frontmatter:
            return self.markdown_data.frontmatter["location"]
        return ""

    def to_typst_card(self) -> typst.Card:
        """
        Converts the ObsidianLocation to a TypstCard.
        """
        return typst.Card(
            name=self.name,
            body_text=self.description,
            image=self.image,
            name_subtext=self.location,
            image_subtext="",
            lists=self.__get_lists(),
            banner_color="#191970",  # midnight blue
            template="landscape-content-right",
        )

    def __get_lists(self) -> list[typst.CardList]:
        list_items = []
        if "Occupants" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Occupants"], str
        ):
            list_items.append(
                typst.CardList.Item(
                    value=self.markdown_data.headers["Occupants"], name="Occupants"
                )
            )
        if "Story Hook" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Story Hook"], str
        ):
            list_items.append(
                typst.CardList.Item(
                    value=self.markdown_data.headers["Story Hook"], name="Rumor"
                )
            )
        return [typst.CardList(items=list_items, title="")]


@dataclass
class Character(RpgData):
    """This is the format that my Obsidian character template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs."""

    @dataclass
    class PhysicalInfo:
        gender: str = ""
        race: str = ""
        job: str = ""

    @dataclass
    class Description:
        overview: str = ""
        looks: str = ""
        voice: str = ""

    @dataclass
    class Personality:
        quirk: str = ""
        likes: str = ""
        dislikes: str = ""

    @dataclass
    class Hooks:
        goals: str = ""
        frustration: str = ""

    @property
    def physical_info(self) -> PhysicalInfo:
        return Character.PhysicalInfo(
            gender=(
                self.markdown_data.dataview_fields["gender"][0]
                if "gender" in self.markdown_data.dataview_fields
                else ""
            ),
            race=(
                self.markdown_data.dataview_fields["race"][0]
                if "race" in self.markdown_data.dataview_fields
                else ""
            ),
            job=(
                self.markdown_data.dataview_fields["class"][0]
                if "class" in self.markdown_data.dataview_fields
                else ""
            ),
        )

    @property
    def description(self) -> Description:
        """
        Returns the description of the character.
        """
        # If there is a header for "Description" in the content...
        if "Description" in self.markdown_data.headers:
            # If the content of that header is a string, then it's the overview.
            if isinstance(self.markdown_data.headers["Description"], str):
                return Character.Description(
                    overview=self.markdown_data.headers["Description"]
                )
            # If it's a dict, then it's the full description.
            return from_dict(
                data_class=Character.Description,
                data=get_lower_keys(self.markdown_data.headers["Description"]),
            )
        # If there is no header for "Description" in the content, then just return an empty description.
        return Character.Description()

    @property
    def personality(self) -> Personality:
        """
        Returns the personality of the character.
        """
        # If there is a header for "Personality" in the content...
        if "Personality" in self.markdown_data.headers:
            # If the content of that header is a string, then it's the quirk.
            if isinstance(self.markdown_data.headers["Personality"], str):
                return Character.Personality(
                    quirk=self.markdown_data.headers["Personality"]
                )
            # If it's a dict, then it's the full personality.
            return from_dict(
                data_class=Character.Personality,
                data=get_lower_keys(self.markdown_data.headers["Personality"]),
            )
        # If there is no header for "Personality" in the content, then just return an empty personality.
        return Character.Personality()

    @property
    def hooks(self) -> Hooks:
        """
        Returns the hooks of the character.
        """
        # If there is a header for "Hooks" in the content...
        if "Hooks" in self.markdown_data.headers:
            # If the content of that header is a string, then it's the goals.
            if isinstance(self.markdown_data.headers["Hooks"], str):
                return Character.Hooks(goals=self.markdown_data.headers["Hooks"])
            # If it's a dict, then it's the full hooks.
            return from_dict(
                data_class=Character.Hooks,
                data=get_lower_keys(self.markdown_data.headers["Hooks"]),
            )
        # If there is no header for "Hooks" in the content, then just return an empty hooks.
        return Character.Hooks()

    @property
    def location(self) -> str:
        if "location" in self.markdown_data.frontmatter:
            return self.markdown_data.frontmatter["location"]
        return ""

    @property
    def group_name(self) -> str:
        if "group-name" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["group-name"][0]
        return ""

    @property
    def group_title(self) -> str:
        if "group-title" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["group-title"][0]
        return ""

    @property
    def group_rank(self) -> str:
        if "group-rank" in self.markdown_data.dataview_fields:
            return self.markdown_data.dataview_fields["group-rank"][0]
        return ""

    def to_typst_card(self) -> typst.Card:
        """
        Converts the ObsidianCharacter to a TypstCard.
        """
        return typst.Card(
            name=self.name,
            body_text=self.description.overview if self.description else "",
            image=self.image,
            name_subtext=self.physical_info.job,
            image_subtext=f"{self.physical_info.gender} {self.physical_info.race}",
            lists=self.__get_lists(),
            banner_color="#800000",  # maroon
            template="landscape-content-left",
        )

    def __get_lists(self) -> list[typst.CardList]:
        lists = [
            self.__get_personality_list(),
            self.__get_secondary_list(),
        ]
        return lists

    def __get_personality_list(self) -> typst.CardList:
        list_items = []
        if self.personality.quirk:
            list_items.append(
                typst.CardList.Item(value=self.personality.quirk, name="Quirk")
            )
        if self.personality.likes:
            list_items.append(
                typst.CardList.Item(value=self.personality.likes, name="Likes")
            )
        if self.personality.dislikes:
            list_items.append(
                typst.CardList.Item(value=self.personality.dislikes, name="Dislikes")
            )
        return typst.CardList(items=list_items, title="")

    def __get_secondary_list(self) -> typst.CardList:
        """
        Second list is an unordered and untitled list of location and group membership.
        """
        second_list = typst.CardList(items=[], title="")
        if self.location:
            location_item = typst.CardList.Item(value=self.location, name="Location")
            second_list.items.append(location_item)
        if self.group_name != "":
            group_name_item = typst.CardList.Item(
                value=self.group_name, name="Member of"
            )
            second_list.items.append(group_name_item)
        return second_list


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
