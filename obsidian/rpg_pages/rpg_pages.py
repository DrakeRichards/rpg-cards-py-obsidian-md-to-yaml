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
            self.description = page.content[self.name]  # type: ignore
            # raise KeyError("H1 has no subheadings.")

        # Put the page's contents into a separate dict for ease of reference.
        self.content: dict[str, str] = page.content[self.name]  # type: ignore

        # Optional checks
        if page.images:
            self.image = page.images[0]
        if page.dataview_fields:
            self.dataview_fields = page.dataview_fields
        else:
            self.dataview_fields = {}
        if page.frontmatter:
            self.frontmatter = page.frontmatter
        else:
            self.frontmatter = {}
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

    item_type: str = ""  # Wondrous item, dagger, armor, etc.
    rarity: str = ""  # Common, uncommon, rare, very rare, legendary, artifact
    cost: str = ""  # gp, sp, cp, etc.
    weight: str = ""  # lb, oz, etc.
    properties: str = ""  # finesse, light, heavy, etc.
    damage: str = ""  # 1d4 S, 1d6 P, etc.
    range: str = ""  # 20/60, 30/120, etc.
    armor_class: str = ""  # 12 + Dex modifier, etc.
    stealth: str = ""  # disadvantage, advantage, etc.
    traits: str = ""  # item type, rarity, magic level, attunement requirements
    magic_level: str = ""  # minor, major, artifact

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # All items should have these fields, but we need to check for them anyway since it's a dict.
        if "Description" in self.content:
            self.description = self.content["Description"]
        else:
            self.description = ""
        if "cost" in self.dataview_fields:
            self.cost = self.dataview_fields["cost"][0]
        else:
            self.cost = ""
        if "weight" in self.dataview_fields:
            self.weight = self.dataview_fields["weight"][0]
        else:
            self.weight = ""

        # Optional fields
        if "damage" in self.dataview_fields:
            self.damage = self.dataview_fields["damage"][0]
        if "range" in self.dataview_fields:
            self.range = self.dataview_fields["range"][0]
        if "armor-class" in self.dataview_fields:
            self.armor_class = self.dataview_fields["armor-class"][0]
        if "stealth" in self.dataview_fields:
            self.stealth = self.dataview_fields["stealth"][0]
        if "magic-level" in self.dataview_fields:
            self.magic_level = self.dataview_fields["magic-level"][0]

        # "Traits" is the key that I used on compendium items to store the item type, rarity, magic level, and attunement requirements.
        # On custom items, these are separate fields.
        # Compendium items
        if "traits" in self.dataview_fields:
            self.traits = self.dataview_fields["traits"][0]
        # Custom items
        if "properties" in self.dataview_fields:
            self.properties = self.dataview_fields["properties"][0]

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

    occupants: str = ""
    story_hook: str = ""
    location: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = self.__get_description()
        self.occupants = (
            self.content["Occupants"] if "Occupants" in self.content else ""
        )
        self.story_hook = (
            self.content["Story Hook"] if "Story Hook" in self.content else ""
        )

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

    def __get_description(self) -> str:
        """
        Returns the description of the location.
        """
        if self.description:
            return self.description
        if "Description" in self.content:
            return self.content["Description"]
        if isinstance(self.content["Description"], str):
            return self.content["Description"]
        return ""

    def __get_lists(self) -> list[typst.CardList]:
        list_items = []
        if "Occupants" in self.content:
            list_items.append(
                typst.CardList.Item(value=self.content["Occupants"], name="Occupants")
            )
        if "Story Hook" in self.content:
            list_items.append(
                typst.CardList.Item(value=self.content["Story Hook"], name="Rumor")
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
            gender=(
                self.dataview_fields["gender"][0]
                if "gender" in self.dataview_fields
                else ""
            ),
            race=(
                self.dataview_fields["race"][0]
                if "race" in self.dataview_fields
                else ""
            ),
            job=(
                self.dataview_fields["class"][0]
                if "class" in self.dataview_fields
                else ""
            ),
        )
        # If the Description, Personality, or Hooks fields are strings, then fill in the overview/quirk/goals fields.
        self.description = self.__get_description()
        self.personality = self.__get_personality()
        self.hooks = self.__get_hooks()
        # Fill in the rest of the fields
        self.location = (
            self.frontmatter["location"] if "location" in self.frontmatter else ""
        )
        self.group_name = (
            self.dataview_fields["group-name"][0]
            if "group-name" in self.dataview_fields
            else ""
        )
        self.group_title = (
            self.dataview_fields["group-title"][0]
            if "group-title" in self.dataview_fields
            else ""
        )
        self.group_rank = (
            self.dataview_fields["group-rank"][0]
            if "group-rank" in self.dataview_fields
            else ""
        )

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

    def __get_description(self) -> Description:
        """
        Returns the description of the character.
        """
        # If it already exists for some reason, just return it.
        if self.description and isinstance(self.description, Character.Description):
            return self.description
        # If there is a header for "Description" in the content...
        if "Description" in self.content:
            # If the content of that header is a string, then it's the overview.
            if isinstance(self.content["Description"], str):
                return Character.Description(overview=self.content["Description"])
            # If it's a dict, then it's the full description.
            return from_dict(
                data_class=Character.Description,
                data=get_lower_keys(self.content["Description"]),
            )
        # If there is no header for "Description" in the content, then just return an empty description.
        return Character.Description()

    def __get_personality(self) -> Personality:
        """
        Returns the personality of the character.
        """
        # If there is a header for "Personality" in the content...
        if "Personality" in self.content:
            # If the content of that header is a string, then it's the quirk.
            if isinstance(self.content["Personality"], str):
                return Character.Personality(quirk=self.content["Personality"])
            # If it's a dict, then it's the full personality.
            return from_dict(
                data_class=Character.Personality,
                data=get_lower_keys(self.content["Personality"]),
            )
        # If there is no header for "Personality" in the content, then just return an empty personality.
        return Character.Personality()

    def __get_hooks(self) -> Hooks:
        """
        Returns the hooks of the character.
        """
        # If there is a header for "Hooks" in the content...
        if "Hooks" in self.content:
            # If the content of that header is a string, then it's the goals.
            if isinstance(self.content["Hooks"], str):
                return Character.Hooks(goals=self.content["Hooks"])
            # If it's a dict, then it's the full hooks.
            return from_dict(
                data_class=Character.Hooks,
                data=get_lower_keys(self.content["Hooks"]),
            )
        # If there is no header for "Hooks" in the content, then just return an empty hooks.
        return Character.Hooks()


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
