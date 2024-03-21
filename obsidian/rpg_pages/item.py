from dataclasses import dataclass

import typst

from .rpg_data_abc import RpgData


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
