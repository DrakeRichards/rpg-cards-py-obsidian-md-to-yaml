from dataclasses import dataclass
import src.obsidian_tools as obsidian_tools


@dataclass
class Character:
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
    physicalInfo: PhysicalInfo | None = None
    description: Description | None = None
    personality: Personality | None = None
    hooks: Hooks | None = None
    image: str = ""
    location: str = ""
    groupName: str = ""
    groupTitle: str = ""
    groupRank: str = ""

    @classmethod
    def from_markdown(cls, text: str):
        """
        Convert a markdown-formatted string into either a Character object or a plain dict. Used to export to other programs.

        Args:
            text (str): The markdown text to parse.
            mode (str): The mode to return the data in. Options are "dict" (default) and "object".

        Raises:
            KeyError: _description_

        Returns:
            str: _description_
        """
        # Parse string to object
        page = obsidian_tools.ObsidianPageData(text)

        # The name of the character should be H1, which is the key of the top-level element.
        name: str = list(page.content.keys())[0]

        # Check whether H1 has any subheaders.
        if isinstance(page.content[name], str):
            raise KeyError("H1 has no subheadings.")

        # Put the page's contents into a separate dict for ease of reference.
        content: dict[str, dict] = page.content[name]  # type: ignore

        # I want the resulting object's keys to be lowercase.
        description_lower_keys = {
            k.lower(): v for k, v in content["Description"].items()
        }
        personality_lower_keys = {
            k.lower(): v for k, v in content["Personality"].items()
        }
        hooks_lower_keys = {k.lower(): v for k, v in content["Hooks"].items()}

        # Make it a Character class
        char = cls(
            name=name,
            physicalInfo=Character.PhysicalInfo(
                gender=page.dataview_fields["gender"][0],
                race=page.dataview_fields["race"][0],
                job=page.dataview_fields["class"][0],
            ),
            description=Character.Description(**description_lower_keys),
            personality=Character.Personality(**personality_lower_keys),
            hooks=Character.Hooks(**hooks_lower_keys),
            image=page.images[0],
            location=page.frontmatter["location"],
            groupName=page.dataview_fields["group-name"][0],
            groupTitle=page.dataview_fields["group-title"][0],
            groupRank=page.dataview_fields["group-rank"][0],
        )

        return char
