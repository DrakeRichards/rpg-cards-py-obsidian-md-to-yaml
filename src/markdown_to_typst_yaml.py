"""
Convert an Obsidian markdown file to a YAML file.
"""

from yaml import dump
from pathlib import Path
from src.obsidian_page_types import Character as ObsidianCharacter
from src.typst_template_types import Character as TypstCharacter
from dataclasses import asdict


def markdown_to_yaml(inputFile: str, outputDirectory: str) -> None:
    characterFileText = Path(inputFile).read_text()

    character_obsidian = ObsidianCharacter.from_markdown(characterFileText)
    character_typst = TypstCharacter.from_character(character_obsidian)
    character_dict = asdict(character_typst)

    # Export to a YAML file.
    outfile: str = f"{outputDirectory}/{character_dict['name']}.yaml"
    print(f"Writing to {outfile}")
    with open(outfile, mode="wt", encoding="utf-8") as file:
        dump(character_dict, file)
    return
