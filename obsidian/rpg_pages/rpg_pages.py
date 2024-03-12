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

    name: str = ""
    description: str = ""
    image: str = ""
    content: dict[str, str] = field(default_factory=dict)
    frontmatter: dict[str, str] = field(default_factory=dict)
    dataview_fields: dict[str, list[str]] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    def __init__(self, markdown_text: str):
        # Parse string to object
        page = MarkdownData(markdown_text)

        # The name of the character should be H1, which is the key of the top-level element.
        self.name = list(page.content.keys())[0]

        # Check whether H1 has any subheaders.
        # If H1 has subheaders, then the name will be a key in the content dict.
        # If it's a string, then it's just the description.
        if isinstance(page.content[self.name], str):
            raise KeyError("H1 has no subheadings.")

        # Put the page's contents into a separate dict for ease of reference.
        self.content: dict[str, str] = page.content[self.name]  # type: ignore

        # Optional checks
        if page.images:
            self.image = page.images[0]
        if page.dataview_fields:
            self.dataview_fields = page.dataview_fields
        if page.frontmatter:
            self.frontmatter = page.frontmatter
        if page.tags:
            self.tags = page.tags

    @abstractmethod
    def to_typst_card(self) -> typst.Card:
        """
        Converts the data to a TypstCard.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")


@dataclass
class Item(RpgData):
    """This is the format that my Obsidian item template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs."""

    item_type: str = ""
    rarity: str = ""
    cost: str = ""
    weight: str = ""
    properties: str = ""
    damage: str = ""
    range: str = ""
    armor_class: str = ""
    stealth: str = ""
    traits: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # All items should have these fields.
        self.description = self.content["Description"]
        self.cost = self.dataview_fields["cost"][0]
        self.weight = self.dataview_fields["weight"][0]

        # Optional fields
        if "damage" in self.dataview_fields:
            self.damage = self.dataview_fields["damage"][0]
        if "range" in self.dataview_fields:
            self.range = self.dataview_fields["range"][0]
        if "armor-class" in self.dataview_fields:
            self.armor_class = self.dataview_fields["armor-class"][0]
        if "stealth" in self.dataview_fields:
            self.stealth = self.dataview_fields["stealth"][0]

        # Compendium items vs homebrew items
        if "traits" in self.dataview_fields:
            self.traits = self.dataview_fields["traits"][0]
            self.properties = ""
        else:
            self.traits = f"{self.item_type}, {self.rarity}"
            self.properties = self.dataview_fields["properties"][0]

    def to_typst_card(self) -> typst.Card:
        """
        Converts the ObsidianItem to a TypstCard.
        """
        return typst.Card(
            name=self.name,
            body_text=self.description,
            image=self.image,
            name_subtext=self.traits,
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
                    typst.CardList.Item(value=self.cost, name="Cost"),
                    typst.CardList.Item(value=self.weight, name="Weight"),
                    typst.CardList.Item(value=self.properties, name="Properties"),
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
                        typst.CardList.Item(value=self.damage, name="Damage"),
                        typst.CardList.Item(value=self.range, name="Range"),
                    ],
                    title="",
                )
            )
        if self.armor_class or self.stealth:
            lists.append(
                typst.CardList(
                    items=[
                        typst.CardList.Item(value=self.armor_class, name="Armor Class"),
                        typst.CardList.Item(value=self.stealth, name="Stealth"),
                    ],
                    title="",
                )
            )
        return lists


@dataclass
class Location(RpgData):
    """
    This is the format that my Obsidian location template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs.
    """

    occupants: str = ""
    story_hook: str = ""
    location: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = self.content["Description"]
        self.occupants = self.content["Occupants"]
        self.story_hook = self.content["Story Hook"]

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
            lists=[
                typst.CardList(
                    items=[
                        typst.CardList.Item(value=self.occupants, name="Occupants"),
                        typst.CardList.Item(value=self.story_hook, name="Story Hook"),
                    ],
                    title="",
                )
            ],
            banner_color="#191970",  # midnight blue
            template="landscape-content-right",
        )


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

    name: str = ""
    physical_info: PhysicalInfo = field(default_factory=PhysicalInfo)
    description: Description = field(default_factory=Description)
    personality: Personality = field(default_factory=Personality)
    hooks: Hooks = field(default_factory=Hooks)
    image: str = ""
    location: str = ""
    group_name: str = ""
    group_title: str = ""
    group_rank: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.physical_info = Character.PhysicalInfo(
            gender=self.dataview_fields["gender"][0],
            race=self.dataview_fields["race"][0],
            job=self.dataview_fields["class"][0],
        )
        # If the Description, Personality, or Hooks fields are strings, then fill in the overview/quirk/goals fields.
        if isinstance(self.content["Description"], str):
            self.description = Character.Description(
                overview=self.content["Description"]
            )
        else:
            self.description = from_dict(
                data_class=Character.Description,
                data=get_lower_keys(self.content["Description"]),
            )
        if isinstance(self.content["Personality"], str):
            self.personality = Character.Personality(quirk=self.content["Personality"])
        else:
            self.personality = from_dict(
                data_class=Character.Personality,
                data=get_lower_keys(self.content["Personality"]),
            )
        if isinstance(self.content["Hooks"], str):
            self.hooks = Character.Hooks(goals=self.content["Hooks"])
        else:
            self.hooks = from_dict(
                data_class=Character.Hooks,
                data=get_lower_keys(self.content["Hooks"]),
            )
        # Fill in the rest of the fields
        self.location = self.frontmatter["location"]
        self.group_name = self.dataview_fields["group-name"][0]
        self.group_title = self.dataview_fields["group-title"][0]
        self.group_rank = self.dataview_fields["group-rank"][0]

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
        return typst.CardList(
            items=[
                typst.CardList.Item(value=self.personality.quirk, name="Quirk"),
                typst.CardList.Item(value=self.personality.likes, name="Likes"),
                typst.CardList.Item(value=self.personality.dislikes, name="Dislikes"),
            ],
            title="",
        )

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
    match page_type:
        case PageTypes.CHARACTER:
            return Character(text)
        case PageTypes.ITEM:
            return Item(text)
        case PageTypes.LOCATION:
            return Location(text)
        case _:
            raise ValueError(f"Page type {page_type} not recognized.")
