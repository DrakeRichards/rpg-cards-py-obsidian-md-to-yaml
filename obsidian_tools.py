import json
import re

import frontmatter as fm
import markdown_to_json

from dataclasses import dataclass, field

@dataclass
class Page:
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
    frontmatter: dict[str,str] = field(init=False)
    content: dict[str,str|dict] = field(init=False)
    dataview_fields: dict[str, list[str]] = field(init=False)
    images: list[str] = field(init=False)

    def __frontmatter(self) -> dict[str, str]:
        parsed = fm.parse(self.text)
        frontmatter = parsed[0]
        return frontmatter
    
    def __content(self) -> dict[str,str|dict]:
        # Pull the frontmatter into a dict.
        parsed = fm.parse(self.text)

        # Pull the rest of the non-frontmatter markdown content.
        text_markdown = parsed[1]

        # Parse the markdown into a dict.
        data_json = markdown_to_json.jsonify(text_markdown)
        data = json.loads(data_json)
        return data

    def __dataview_fields(self) -> dict[str, list[str]]:
        dv_fields_pattern: re.Pattern[str] = re.compile(r"(?:[(\[]|^- )(?P<dvKey>[\w ]+):: (?:\[{0,2})(?:\w*\|)?(?P<dvValue>[\w \-/,]*?)(?:[)\]]|$|\n)")
        matches: list[re.Match[str]] = list(dv_fields_pattern.finditer(self.text))
        dv_fields: dict[str, list[str]] = {}
        if not matches:
            return dv_fields
        for match in matches:
            dv_key: str = match.group('dvKey')
            dv_value: str = match.group('dvValue')
            # Continue just in case the key is empty somehow.
            if not dv_key or dv_key == '':
                continue
            # If this key is already present, change the existing value to a list and append the new value.
            if dv_key in dv_fields:
                dv_fields[dv_key] = [*dv_fields[dv_key], dv_value]
            else:
                dv_fields[dv_key] = [dv_value]
        return dv_fields
        
    def __get_images(self) -> list[str]:
        image_file_pattern = re.compile(r"!\[\[(?P<filename>.*?\.(?:jpg|png|jpeg|webp))\|\+character\]\]")
        matches = list(image_file_pattern.finditer(self.text))
        images = []
        if not matches:
            return images
        for match in matches:
            images.append(match.group('filename'))
        return images
    
    def __post_init__(self):
        self.frontmatter = self.__frontmatter()
        self.content = self.__content()
        self.dataview_fields = self.__dataview_fields()
        self.images = self.__get_images()
