from dataclasses import dataclass, field
from enum import Enum

from dacite import from_dict

from src.obsidian_tools import ObsidianPageData


class ObsidianPageTypes(Enum):
    CHARACTER = "character"
    ITEM = "item"
    LOCATION = "location"
    UNKNOWN = "unknown"


class ObsidianItemTypes(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ITEM = "item"
    UNKNOWN = "unknown"


@dataclass
class RpgData:
    """
    Base class for each of the types of Obsidian pages.
    """

    name: str = ""
    description: str = ""
    image: str = ""
    content: dict[str, str] = field(default_factory=dict)
    frontmatter: dict[str, str] = field(default_factory=dict)
    dataview_fields: dict[str, list[str]] = field(default_factory=dict)

    def __init__(self, markdown_text: str):
        # Parse string to object
        page = ObsidianPageData(markdown_text)

        # The name of the character should be H1, which is the key of the top-level element.
        self.name = list(page.content.keys())[0]

        # Check whether H1 has any subheaders.
        # If H1 has subheaders, then the name will be a key in the content dict.
        # If it's a string, then it's just the description.
        if isinstance(page.content[self.name], str):
            raise KeyError("H1 has no subheadings.")

        # Put the page's contents into a separate dict for ease of reference.
        self.content: dict[str, str] = page.content[self.name]  # type: ignore

        # Items might not have an image, so I need to check for that.
        if page.images:
            self.image = page.images[0]

        # Dataview fields are optional, so I need to check for that.
        if page.dataview_fields:
            self.dataview_fields = page.dataview_fields

        # Frontmatter is also optional, so I need to check for that.
        if page.frontmatter:
            self.frontmatter = page.frontmatter


@dataclass
class ObsidianCharacter(RpgData):
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

        self.physical_info = ObsidianCharacter.PhysicalInfo(
            gender=self.dataview_fields["gender"][0],
            race=self.dataview_fields["race"][0],
            job=self.dataview_fields["class"][0],
        )
        # If the Description, Personality, or Hooks fields are strings, then fill in the overview/quirk/goals fields.
        if isinstance(self.content["Description"], str):
            self.description = ObsidianCharacter.Description(
                overview=self.content["Description"]
            )
        else:
            self.description = from_dict(
                data_class=ObsidianCharacter.Description,
                data=get_lower_keys(self.content["Description"]),
            )
        if isinstance(self.content["Personality"], str):
            self.personality = ObsidianCharacter.Personality(
                quirk=self.content["Personality"]
            )
        else:
            self.personality = from_dict(
                data_class=ObsidianCharacter.Personality,
                data=get_lower_keys(self.content["Personality"]),
            )
        if isinstance(self.content["Hooks"], str):
            self.hooks = ObsidianCharacter.Hooks(goals=self.content["Hooks"])
        else:
            self.hooks = from_dict(
                data_class=ObsidianCharacter.Hooks,
                data=get_lower_keys(self.content["Hooks"]),
            )
        # Fill in the rest of the fields
        self.location = self.frontmatter["location"]
        self.group_name = self.dataview_fields["group-name"][0]
        self.group_title = self.dataview_fields["group-title"][0]
        self.group_rank = self.dataview_fields["group-rank"][0]


@dataclass
class ObsidianItem(RpgData):
    """This is the format that my Obsidian item template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs."""

    item_type: str = ""
    rarity: str = ""
    cost: str = ""
    weight: str = ""
    properties: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = self.content["Description"]
        self.item_type = self.frontmatter["tags"][0]
        self.rarity = self.dataview_fields["rarity"][0]
        self.cost = self.dataview_fields["cost"][0]
        self.weight = self.dataview_fields["weight"][0]
        self.properties = self.dataview_fields["properties"][0]


@dataclass
class ObsidianItemWeapon(ObsidianItem):
    """
    Additional fields for weapons.
    """

    damage: str = ""
    range: str = ""
    # TODO: Implement the full class for weapons.


@dataclass
class ObsidianItemArmor(ObsidianItem):
    """
    Additional fields for armor.
    """

    armor_class: str = ""
    stealth: str = ""
    # TODO: Implement the full class for armor.


@dataclass
class ObsidianLocation(RpgData):
    """
    This is the format that my Obsidian location template uses. It's a dataclass so that I can easily convert it to a dictionary for exporting to other programs.
    """

    occupants: str = ""
    story_hook: str = ""
    location: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __post_init__(self):
        self.description = self.content["Description"]
        self.occupants = self.content["Occupants"]
        self.story_hook = self.content["Story Hook"]


def get_lower_keys(content: dict[str, str]) -> dict[str, str]:
    """Converts the keys of a dictionary to lowercase.

    Args:
        content (dict[str, str]): A dictionary.

    Returns:
        dict[str, str]: A dictionary with lowercase keys.
    """
    lower_keys = {k.lower(): v for k, v in content.items()}
    return lower_keys


def __get_item_type(text: str) -> ObsidianItemTypes:
    """
    Identify the type of an Obsidian item based on its frontmatter tags.
    """
    page = ObsidianPageData(text)
    if "tags" not in page.frontmatter:
        return ObsidianItemTypes.UNKNOWN
    tags = page.frontmatter["tags"]
    if "weapon" in tags:
        return ObsidianItemTypes.WEAPON
    elif "armor" in tags:
        return ObsidianItemTypes.ARMOR
    else:
        return ObsidianItemTypes.ITEM


def __new_item(text: str) -> ObsidianItem:
    item_type = __get_item_type(text)
    match item_type:
        case ObsidianItemTypes.WEAPON:
            return ObsidianItemWeapon(text)
        case ObsidianItemTypes.ARMOR:
            return ObsidianItemArmor(text)
        case ObsidianItemTypes.ITEM:
            return ObsidianItem(text)
        case _:
            raise ValueError(f"Item type {item_type} not recognized.")


def get_page_type(text: str) -> ObsidianPageTypes:
    """
    Identify the type of an Obsidian page based on its frontmatter tags.
    """
    page = ObsidianPageData(text)
    if "tags" not in page.frontmatter:
        return ObsidianPageTypes.UNKNOWN
    tags = page.frontmatter["tags"]
    if "character" in tags:
        return ObsidianPageTypes.CHARACTER
    elif "item" in tags:
        return ObsidianPageTypes.ITEM
    elif "location" in tags:
        return ObsidianPageTypes.LOCATION
    else:
        return ObsidianPageTypes.UNKNOWN


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
        case ObsidianPageTypes.CHARACTER:
            return ObsidianCharacter(text)
        case ObsidianPageTypes.ITEM:
            return __new_item(text)
        case ObsidianPageTypes.LOCATION:
            return ObsidianLocation(text)
        case _:
            raise ValueError(f"Page type {page_type} not recognized.")
