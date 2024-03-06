"""
Convert an Obsidian markdown file to a YAML file.
"""

from dataclasses import asdict
from pathlib import Path

from yaml import dump

from src.obsidian_page_types import ObsidianCharacter
from src.typst_template_types import TypstCharacter


def markdown_to_yaml(inputFile: str, outputDirectory: str) -> None:
    characterFileText = Path(inputFile).read_text()

    character_obsidian = ObsidianCharacter(characterFileText)
    character_typst = TypstCharacter(character_obsidian)
    character_dict = asdict(character_typst)

    # Export to a YAML file. Use the same base filename as the input file.
    outfile: str = f"{outputDirectory}/{Path(inputFile).stem}.yaml"
    with open(outfile, mode="wt", encoding="utf-8") as file:
        dump(character_dict, file)
    return
