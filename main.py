import argparse
from dataclasses import asdict
from os import listdir
from os.path import isfile, join
from pathlib import Path
from shutil import copy
from typing import List

import yaml

import typst as typst
import utils.image as iutil
import utils.string as sutil
from obsidian import rpg_pages


def get_files_with_extension(directory: Path, extension: str) -> List[str]:
    """Get all files in a directory with a specific extension.

    Args:
        directory (Path): The path to the directory.
        extension (str): The file extension, including the period.

    Returns:
        List[str]: A list of file paths.
    """

    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    markdown_files = [f for f in files if f.endswith(extension)]
    return [f"{directory}/{file}" for file in markdown_files]


def parse_md_to_typst_card(filepath: str) -> typst.Card:
    """Parse an Obsidian markdown file into a Typst card.

    Args:
        text (str): The text of the markdown file.

    Returns:
        rpgCardInterface: A Typst card.
    """
    with open(filepath, "r") as file:
        text: str = file.read()
        cleaned_text = sutil.replace_uncommon_characters(text)
        page_object: rpg_pages.rpg_data_abc.RpgData = rpg_pages.new_page(cleaned_text)
        page_typst: typst.Card = page_object.to_typst_card()
        return page_typst


def parse_args():
    parser = argparse.ArgumentParser(
        description="Converts Obsidian markdown files to Typst YAML."
    )
    parser.add_argument(
        "--input-markdown-directory",
        help="The path to the directory containing the markdown files.",
        metavar="input_markdown_directory",
        type=Path,
        default="in",
    )
    parser.add_argument(
        "--input-image-directory",
        help="The path to the directory containing the images.",
        metavar="input_image_directory",
        type=Path,
        default="in",
    )
    parser.add_argument(
        "--output-file-path",
        help="The path to the output YAML file, including its extension.",
        metavar="output_file_path",
        type=Path,
        default="data.yaml",
    )
    parser.add_argument(
        "--output-image-directory",
        help="The path to the output directory for the images.",
        metavar="output_image_directory",
        type=Path,
        default=".",
    )
    return parser.parse_args()


if __name__ == "__main__":
    params = parse_args()

    # Get all markdown files in the input directory
    md_files = get_files_with_extension(params.input_markdown_directory, ".md")
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
        except AttributeError as identifier:
            print(f"🔴 '{file}' AttributeError: {identifier}")
            pass
    if typst_cards["cards"].count == 0:
        raise ValueError("No cards were generated.")

    # Iterate through each card to validate and convert its image.
    for card in typst_cards["cards"]:
        if card["image"] == "":
            continue
        # Find the image file the card links to and check if it's in the input directory.
        image_file = Path(f"{params.input_image_directory}/{card['image']}")
        # If it isn't, set the card's image to "" so that the Typst template doesn't try to use a file that doesn't exist.
        if not image_file.exists():
            card["image"] = ""
            continue
        if not iutil.is_image(image_file):
            card["image"] = ""
            continue
        # If it is, check whether its extension matches its MIME type.
        if not iutil.does_extension_match(image_file):
            # If it doesn't, convert the image to the correct format.
            new_file: Path = iutil.new_file_from_mimetype(image_file)
            card["image"] = new_file.name
        # Copy the image to the output directory.
        dest_file: Path = params.output_image_directory / card["image"]
        copy(image_file, dest_file)

    # Write the Typst YAML to a file
    with open(params.output_file_path, "w") as file:
        yaml.dump(data=typst_cards, stream=file, Dumper=yaml.SafeDumper)
    print(f"Successfully wrote {params.output_file_path}.")
