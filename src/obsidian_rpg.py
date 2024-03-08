import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import List

from dacite import from_dict
from jsonschema import Draft7Validator

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
class TypstCard:
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

    def to_typst_card(self) -> TypstCard:
        """
        Converts the data to a TypstCard.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")


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

    def to_typst_card(self) -> TypstCard:
        """
        Converts the ObsidianCharacter to a TypstCard.
        """
        return TypstCard(
            name=self.name,
            body_text=self.description.overview if self.description else "",
            image=self.image,
            name_subtext=self.physical_info.job,
            image_subtext=f"{self.physical_info.gender} {self.physical_info.race}",
            lists=self.__get_lists(),
            banner_color="#800000",  # maroon
            template="landscape-content-left",
        )

    def __get_lists(self) -> list[CardList]:
        lists = [
            self.__get_personality_list(),
            self.__get_secondary_list(),
        ]
        return lists

    def __get_personality_list(self) -> CardList:
        return CardList(
            items=[
                CardList.ListItem(value=self.personality.quirk, name="Quirk"),
                CardList.ListItem(value=self.personality.likes, name="Likes"),
                CardList.ListItem(value=self.personality.dislikes, name="Dislikes"),
            ],
            title="",
        )

    def __get_secondary_list(self) -> CardList:
        """
        Second list is an unordered and untitled list of location and group membership.
        """
        second_list = CardList(items=[], title="")
        if self.location:
            location_item = CardList.ListItem(value=self.location, name="Location")
            second_list.items.append(location_item)
        if self.group_name != "":
            group_name_item = CardList.ListItem(value=self.group_name, name="Member of")
            second_list.items.append(group_name_item)
        return second_list


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

    def to_typst_card(self) -> TypstCard:
        """
        Converts the ObsidianItem to a TypstCard.
        """
        return TypstCard(
            name=self.name,
            body_text=self.description,
            image=self.image,
            name_subtext=self.__get_subtext(),
            image_subtext="",
            lists=self.__get_lists(),
            banner_color="#195905",  # Lincoln Green
            template="landscape-content-right",
        )

    def __get_lists(self) -> list[CardList]:
        lists = [
            CardList(
                items=[
                    CardList.ListItem(value=self.cost, name="Cost"),
                    CardList.ListItem(value=self.weight, name="Weight"),
                    CardList.ListItem(value=self.properties, name="Properties"),
                ],
                title="",
            )
        ]
        return lists

    def __get_subtext(self) -> str:
        subtext = f"{self.rarity} {self.item_type}"
        return subtext


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

        self.description = self.content["Description"]
        self.occupants = self.content["Occupants"]
        self.story_hook = self.content["Story Hook"]

    def to_typst_card(self) -> TypstCard:
        """
        Converts the ObsidianLocation to a TypstCard.
        """
        return TypstCard(
            name=self.name,
            body_text=self.description,
            image=self.image,
            name_subtext=self.location,
            image_subtext="",
            lists=[
                CardList(
                    items=[
                        CardList.ListItem(value=self.occupants, name="Occupants"),
                        CardList.ListItem(value=self.story_hook, name="Story Hook"),
                    ],
                    title="",
                )
            ],
            banner_color="#191970",  # midnight blue
            template="landscape-content-right",
        )


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
    if len(page.tags) == 0:
        return ObsidianPageTypes.UNKNOWN
    if "character" in page.tags:
        return ObsidianPageTypes.CHARACTER
    elif "item" in page.tags:
        return ObsidianPageTypes.ITEM
    elif "location" in page.tags:
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
