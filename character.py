from dataclasses import dataclass, asdict

import obsidian_tools


@dataclass
class Character:
    @dataclass
    class PhysicalInfo:
        gender: str = ''
        race: str = ''
        job: str = ''

    @dataclass
    class Description:
        overview: str = ''
        looks: str = ''
        voice: str = ''

    @dataclass
    class Personality:
        quirk: str = ''
        likes: str = ''
        dislikes: str = ''

    @dataclass
    class Hooks:
        goals: str = ''
        frustration: str = ''

    name: str = ''
    physicalInfo: PhysicalInfo | None = None
    description: Description | None = None
    personality: Personality | None = None
    hooks: Hooks | None = None
    image: str = ''
    location: str = ''
    groupName: str = ''
    groupTitle: str = ''
    groupRank: str = ''

def parse(text: str) -> dict[str, str]:
    """Convert a markdown-formatted string into a Character object. Used to export to other programs.

    Args:
        text (str): 

    Raises:
        KeyError: _description_

    Returns:
        str: _description_
    """
    # Parse string to object
    page = obsidian_tools.Page(text)

    # The name of the character should be H1, which is the key of the top-level element.
    name: str = list(page.content.keys())[0]

    # Check whether H1 has any subheaders.
    if isinstance(page.content[name], str):
        raise KeyError('H1 has no subheadings.')

    # Put the page's contents into a separate dict for ease of reference.
    content: dict[str, dict] = page.content[name]  # type: ignore

    # I want the resulting object's keys to be lowercase.
    description_lower_keys = {
        k.lower(): v for k, v in content['Description'].items()}
    personality_lower_keys = {
        k.lower(): v for k, v in content['Personality'].items()}
    hooks_lower_keys = {
        k.lower(): v for k, v in content['Hooks'].items()}

    # Make it a Character class
    char = Character(
        name=name,
        physicalInfo=Character.PhysicalInfo(
            gender=page.dataview_fields['gender'][0],
            race=page.dataview_fields['race'][0],
            job=page.dataview_fields['class'][0],
        ),
        description=Character.Description(**description_lower_keys),
        personality=Character.Personality(**personality_lower_keys),
        hooks=Character.Hooks(**hooks_lower_keys),
        image=page.images[0],
        location=page.frontmatter['location'],
        groupName=page.dataview_fields['Group Name'][0],
        groupTitle=page.dataview_fields['Group Title'][0],
        groupRank=page.dataview_fields['Group Rank'][0]
    )

    return asdict(char)


"""
# File contents to string
text = Path(filepath).read_text()

# Export to a YAML file.
outfile: str = f"./data/{char.name}.yaml"
with open(outfile, mode="wt", encoding="utf-8") as file:
    yaml.dump(asdict(char), file)
"""