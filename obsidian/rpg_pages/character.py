from dataclasses import dataclass

from dacite import from_dict

import typst
from utils.dict import get_lower_keys

from .rpg_data_abc import RpgData


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
