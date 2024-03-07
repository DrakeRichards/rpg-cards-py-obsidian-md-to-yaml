import argparse
from dataclasses import asdict
from pathlib import Path
from shutil import copy
from typing import List

import yaml

import src.image_validation as image_validation
import src.obsidian_rpg as obsidian_rpg


def get_files_with_extension(directory_path: str, extension: str) -> List[str]:
    """Get all files in a directory with a specific extension.

    Args:
        directoryPath (str): The path to the directory.
        extension (str): The file extension, including the period.

    Returns:
        List[str]: A list of file paths.
    """
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    markdown_files = [f for f in files if f.endswith(extension)]
    return [f"{directory_path}/{file}" for file in markdown_files]


def parse_md_to_typst_card(filepath: str) -> obsidian_rpg.TypstCard:
    """Parse an Obsidian markdown file into a Typst card.

    Args:
        text (str): The text of the markdown file.

    Returns:
        rpgCardInterface: A Typst card.
    """
    with open(filepath, "r") as file:
        text: str = file.read()
        page_object: obsidian_rpg.RpgData = obsidian_rpg.new_page(text)
        page_typst: obsidian_rpg.TypstCard = page_object.to_typst_card()
        return page_typst


if __name__ == "__main__":
    # Parser setup
    parser = argparse.ArgumentParser(
        description="Converts Obsidian markdown files to Typst YAML."
    )
    parser.add_argument(
        "inputDirectoryPath",
        help="The path to the directory containing the markdown files.",
    )
    parser.add_argument("outputFilePath", help="The path to the output YAML file.")
    params = parser.parse_args()

    # Get all markdown files in the input directory
    md_files = get_files_with_extension(params.inputDirectoryPath, ".md")
    out_file_path = params.outputFilePath
    typst_cards: dict[str, list[dict]] = {"cards": []}
    for file in md_files:
        try:
            page_typst = parse_md_to_typst_card(file)
            typst_cards["cards"].append(asdict(page_typst))
        except KeyError as identifier:
            print(f"🔴 '{file}' KeyError: {identifier}")
            pass
        except ValueError as identifier:
            print(f"🔴 '{file}' ValueError: {identifier}")
            pass
    if typst_cards["cards"].count == 0:
        raise ValueError("No cards were generated.")

    # Iterate through each card to validate and convert its image.
    for card in typst_cards["cards"]:
        if card["image"] == "":
            continue
        # Find the image file the card links to and check if it's in the input directory.
        image_file = Path(f"{params.inputDirectoryPath}/{card['image']}")
        # If it isn't, set the card's image to "" so that the Typst template doesn't try to use a file that doesn't exist.
        if not image_validation.is_image(image_file):
            card["image"] = ""
            continue
        # If it is, check whether its extension matches its MIME type.
        if not image_validation.does_extension_match(image_file):
            # If it doesn't, convert the image to the correct format.
            new_file: Path = image_validation.new_file_from_mimetype(image_file)
            card["image"] = new_file.name
        # Copy the image to the output directory.
        dest_file: Path = Path(out_file_path).parent / card["image"]
        copy(image_file, dest_file)

    # Write the Typst YAML to a file
    with open(out_file_path, "w") as file:
        yaml.dump(data=typst_cards, stream=file, Dumper=yaml.SafeDumper)
    print(f"Successfully wrote {out_file_path}.")
