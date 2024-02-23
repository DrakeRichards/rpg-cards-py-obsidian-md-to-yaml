from dataclasses import dataclass, field
import src.obsidian_tools as obsidian_tools


@dataclass
class ObsidianCharacter:
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
    physicalInfo: PhysicalInfo = field(default_factory=PhysicalInfo)
    description: Description = field(default_factory=Description)
    personality: Personality = field(default_factory=Personality)
    hooks: Hooks = field(default_factory=Hooks)
    image: str = ""
    location: str = ""
    groupName: str = ""
    groupTitle: str = ""
    groupRank: str = ""

    def __init__(self, markdownText: str):
        # Parse string to object
        page = obsidian_tools.ObsidianPageData(markdownText)

        # The name of the character should be H1, which is the key of the top-level element.
        characterName: str = list(page.content.keys())[0]

        # Check whether H1 has any subheaders.
        # If H1 has subheaders, then the name will be a key in the content dict.
        # If it's a string, then it's just the description.
        if isinstance(page.content[characterName], str):
            raise KeyError("H1 has no subheadings.")

        # Put the page's contents into a separate dict for ease of reference.
        content: dict[str, dict] = page.content[characterName]  # type: ignore

        # I want the resulting object's keys to be lowercase.
        description_lower_keys = {
            k.lower(): v for k, v in content["Description"].items()
        }
        personality_lower_keys = {
            k.lower(): v for k, v in content["Personality"].items()
        }
        hooks_lower_keys = {k.lower(): v for k, v in content["Hooks"].items()}

        # Make it a Character class
        self.name = characterName
        self.physicalInfo = ObsidianCharacter.PhysicalInfo(
            gender=page.dataview_fields["gender"][0],
            race=page.dataview_fields["race"][0],
            job=page.dataview_fields["class"][0],
        )
        self.description = ObsidianCharacter.Description(**description_lower_keys)
        self.personality = ObsidianCharacter.Personality(**personality_lower_keys)
        self.hooks = ObsidianCharacter.Hooks(**hooks_lower_keys)
        self.image = page.images[0]
        self.location = page.frontmatter["location"]
        self.groupName = page.dataview_fields["group-name"][0]
        self.groupTitle = page.dataview_fields["group-title"][0]
        self.groupRank = page.dataview_fields["group-rank"][0]
