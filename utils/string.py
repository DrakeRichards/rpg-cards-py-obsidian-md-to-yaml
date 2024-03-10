import re as __re


def simplify_text(text: str) -> str:
    """All letters to lowercase. Replace spaces with hyphens."""
    return text.lower().replace(" ", "-")


def remove_wikilinks(text: str) -> str:
    """
    Extracts the string contents of all wikilinks from a string.
    If there is alt text, use that instead of the name of the file.
    Leaves embeds (`![[link]]`) alone.
    """
    pattern = __re.compile(
        r"(?<![!])\[\[(?P<link>.+?)(?:\|)?(?P<altText>(?<=\|).+?)?\]\]"
    )
    matches = pattern.finditer(text)
    for match in matches:
        if match.group("altText"):
            text = text.replace(match.group(0), match.group("altText"))
        else:
            text = text.replace(match.group(0), match.group("link"))
    return text


def replace_uncommon_characters(text: str) -> str:
    """Replace uncommon characters with their common counterparts."""
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text
