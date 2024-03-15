import json
import re
from dataclasses import dataclass, field
from typing import Dict, List

import frontmatter as fm
import markdown_to_json

from utils.string import (
    remove_markdown_links,
    remove_wikilinks,
    replace_uncommon_characters,
    simplify_text,
)


@dataclass
class MarkdownData:
    """
    Parses text in an Obsidian.md file into a Python object.
    Makes it easier to work with Obsidian files in Python.

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

    @property
    def text_cleaned(self) -> str:
        text = self.text
        text = remove_wikilinks(text)
        text = remove_markdown_links(text)
        text = replace_uncommon_characters(text)
        return text

    @property
    def frontmatter(self) -> Dict[str, str]:
        parsed = fm.parse(self.text_cleaned)
        frontmatter = parsed[0]
        # Some frontmatter values are enclosed in [[double brackets]], causing the frontmatter parser to interpret them as double-nested lists.
        # I want to convert these to strings.
        for key, value in frontmatter.items():
            if isinstance(value, list):
                if isinstance(value[0], list):
                    frontmatter[key] = value[0][0]
        return frontmatter

    @property
    def dataview_fields(self) -> Dict[str, List[str]]:
        dv_fields_pattern: re.Pattern[str] = re.compile(
            r"(?:[(\[]|^- )(?P<dvKey>[\w ]+):: (?:\[{0,2})(?:\w*\|)?(?P<dvValue>[^\[\]]*?)(?:[)\]]|$|\n)"
        )
        matches: list[re.Match[str]] = list(
            dv_fields_pattern.finditer(self.text_cleaned)
        )
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

    @property
    def images(self) -> List[str]:
        image_file_pattern = re.compile(r"\[\[(?P<filename>.*?\.(?:jpg|png|jpeg|webp))")
        matches = list(image_file_pattern.finditer(self.text))
        images = []
        if not matches:
            return images
        for match in matches:
            images.append(match.group("filename"))
        return images

    @property
    def content(self) -> Dict[str, str | dict]:  # type: ignore
        # Pull the frontmatter into a dict.
        parsed = fm.parse(self.text_cleaned)

        # Pull the rest of the non-frontmatter markdown content.
        text_markdown = parsed[1]

        # Parse the markdown into a dict.
        # I convert the markdown to JSON and then back to a dict because this way I get a plain dict instead of an OrderedDict.
        data_json = markdown_to_json.jsonify(text_markdown)
        data = json.loads(data_json)
        return data

    @property
    def tags(self) -> List[str]:
        if "tags" in self.frontmatter:
            tags = self.frontmatter["tags"]
            return [tag.split("/")[0] for tag in tags]
        return []
