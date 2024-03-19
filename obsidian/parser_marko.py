"""
Parses Obsidian markdown files into a Python object.
"""

import marko as marko
from attrs import define, field


@define
class MarkdownData:
    """
    Parses text in an Obsidian.md file into a Python object.

    Also extracts Obsidian-specific metadata from the file, such as tags and DataView fields.
    """

    text: str = field(default="")

    @property
    def parsed_text(self) -> marko.block.Document:
        return marko.parse(self.text)


if __name__ == "__main__":
    text = ""
    example_file_path = "in/markdown/Elara Ebonlocke.md"
    with open(example_file_path, "r") as file:
        text = file.read()
    md = MarkdownData(text=text)
    print(md.parsed_text)
    # <Document: [<Heading: level=1 text='Hello, world!'>]>
