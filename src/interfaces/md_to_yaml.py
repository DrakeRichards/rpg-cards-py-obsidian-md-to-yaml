# This script is used to convert a character file to a YAML file.
from yaml import dump
from pathlib import Path
from src.obsidian_page_types import Character
import argparse

parser = argparse.ArgumentParser(
    description="Parse a character file and output a YAML file."
)
parser.add_argument("input", help="The input file to parse.")
parser.add_argument("output", help="The output directory to write the YAML file to.")
args = parser.parse_args()

if __name__ == "__main__":
    characterFileText = Path(args.input).read_text()

    char: dict[str, str] = Character.from_markdown(characterFileText)

    # Export to a YAML file.
    outfile: str = f"{args.output}/{char['name']}.yaml"
    print(f"Writing to {outfile}")
    with open(outfile, mode="wt", encoding="utf-8") as file:
        dump(char, file)
