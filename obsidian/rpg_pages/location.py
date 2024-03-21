from dataclasses import dataclass

import typst

from .rpg_data_abc import RpgData


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
