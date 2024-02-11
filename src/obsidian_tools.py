"""
Extracts data from Obsidian Markdown files.
"""

import json
import re
import frontmatter as fm
import markdown_to_json
from dataclasses import dataclass, field


@dataclass
class ObsidianPageData:
    """Dumps a Markdown string to a dict.

    Args:

        - `text (str)`: Input markdown text.

    Returns:

        - `frontmatter`: The key-value pairs from the document's frontmatter.
        - `content`: A `dict` with each header as the key and the content under that header as the value.
        - `dataview_fields`: The key-value pairs of each inline Dataview field contained in `content`.
            - Because Dataview doesn't restrict users to one key per page, all values in this field are returned as a `list`.
            - Should detect:
                - `(key:: value)`
                - `[key:: value]`
                - `- key:: value`
        - `images`: A list of all embedded image filenames.
    """

    text: str
    frontmatter: dict[str, str] = field(init=False)
    content: dict[str, str | dict] = field(init=False)
    dataview_fields: dict[str, list[str]] = field(init=False)
    images: list[str] = field(init=False)

    def __init__(self, text):
        text_without_wikilinks = remove_wikilinks(text)
        self.frontmatter = get_frontmatter(text_without_wikilinks)
        self.content = get_content(text_without_wikilinks)
        self.dataview_fields = get_dataview_fields(text_without_wikilinks)
        self.images = get_images(text)


def simplify_text(text: str) -> str:
    """All letters to lowercase. Replace spaces with hyphens."""
    return text.lower().replace(" ", "-")


def get_content(text) -> dict[str, str | dict]:
    # Pull the frontmatter into a dict.
    parsed = fm.parse(text)

    # Pull the rest of the non-frontmatter markdown content.
    text_markdown = parsed[1]

    # Parse the markdown into a dict.
    # I convert the markdown to JSON and then back to a dict because this way I get a plain dict instead of an OrderedDict.
    data_json = markdown_to_json.jsonify(text_markdown)
    data = json.loads(data_json)
    return data


def get_frontmatter(text) -> dict[str, str]:
    parsed = fm.parse(text)
    frontmatter = parsed[0]
    # Some frontmatter values are enclosed in [[double brackets]], causing the frontmatter parser to interpret them as double-nested lists.
    # I want to convert these to strings.
    for key, value in frontmatter.items():
        if isinstance(value, list):
            if isinstance(value[0], list):
                frontmatter[key] = value[0][0]
    return frontmatter


def get_dataview_fields(text) -> dict[str, list[str]]:
    dv_fields_pattern: re.Pattern[str] = re.compile(
        r"(?:[(\[]|^- )(?P<dvKey>[\w ]+):: (?:\[{0,2})(?:\w*\|)?(?P<dvValue>[^\[\]]*?)(?:[)\]]|$|\n)"
    )
    matches: list[re.Match[str]] = list(dv_fields_pattern.finditer(text))
    dv_fields: dict[str, list[str]] = {}
    if not matches:
        return dv_fields
    for match in matches:
        dv_key: str = simplify_text(match.group("dvKey"))
        dv_value: str = match.group("dvValue")
        # Continue just in case the key is empty somehow.
        if not dv_key or dv_key == "":
            continue
        # If this key is already present, change the existing value to a list and append the new value.
        if dv_key in dv_fields:
            dv_fields[dv_key] = [*dv_fields[dv_key], dv_value]
        else:
            dv_fields[dv_key] = [dv_value]
    return dv_fields


def get_images(text) -> list[str]:
    image_file_pattern = re.compile(r"\[\[(?P<filename>.*?\.(?:jpg|png|jpeg|webp))")
    matches = list(image_file_pattern.finditer(text))
    images = []
    if not matches:
        return images
    for match in matches:
        images.append(match.group("filename"))
    return images


def remove_wikilinks(text: str) -> str:
    """
    Extracts the string contents of all wikilinks from a string.
    If there is alt text, use that instead of the name of the file.
    Leaves embeds (`![[link]]`) alone.
    """
    pattern = re.compile(
        r"(?<![!])\[\[(?P<link>.+?)(?:\|)?(?P<altText>(?<=\|).+?)?\]\]"
    )
    matches = pattern.finditer(text)
    for match in matches:
        if match.group("altText"):
            text = text.replace(match.group(0), match.group("altText"))
        else:
            text = text.replace(match.group(0), match.group("link"))
    return text


def markdown_to_dict(text: str) -> ObsidianPageData:
    """Dumps a Markdown string to a dict.

    Args:

        - `text (str)`: Input markdown text.

    Returns:

        - `frontmatter`: The key-value pairs from the document's frontmatter.
        - `content`: A `dict` with each header as the key and the content under that header as the value.
        - `dataview_fields`: The key-value pairs of each inline Dataview field contained in `content`.
            - Because Dataview doesn't restrict users to one key per page, all values in this field are returned as a `list`.
            - Should detect:
                - `(key:: value)`
                - `[key:: value]`
                - `- key:: value`
        - `images`: A list of all embedded image filenames.
    """
    return ObsidianPageData(text)
