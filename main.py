import argparse
from dataclasses import asdict
from pathlib import Path
from shutil import copy
from typing import List

import yaml

import src.image_validation as imageValidation
import src.obsidian_rpg as obsidian_rpg
import src.typst as typst


def getFilesWithExtension(directoryPath: str, extension: str) -> List[str]:
    """Get all files in a directory with a specific extension.

    Args:
        directoryPath (str): The path to the directory.
        extension (str): The file extension, including the period.

    Returns:
        List[str]: A list of file paths.
    """
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]
    markdownFiles = [f for f in files if f.endswith(extension)]
    return [f"{directoryPath}/{file}" for file in markdownFiles]


def parseToTypstCard(filepath: str) -> typst.rpgCardInterface:
    """Parse an Obsidian markdown file into a Typst card.

    Args:
        text (str): The text of the markdown file.

    Returns:
        rpgCardInterface: A Typst card.
    """
    with open(filepath, "r") as file:
        text: str = file.read()
        pageObject: obsidian_rpg.RpgData = obsidian_rpg.newPage(text)
        pageTypst: typst.rpgCardInterface = typst.fromPageObject(pageObject)
        return pageTypst


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


if __name__ == "__main__":
    # Get all markdown files in the input directory
    markdownFiles = getFilesWithExtension(params.inputDirectoryPath, ".md")
    outputFilePath = params.outputFilePath
    typstCards = {"cards": []}
    for file in markdownFiles:
        try:
            pageTypst = parseToTypstCard(file)
            typstCards["cards"].append(asdict(pageTypst))
        except KeyError as identifier:
            print(f"🔴 '{file}' KeyError: {identifier}")
            pass
        except ValueError as identifier:
            print(f"🔴 '{file}' ValueError: {identifier}")
            pass
    if typstCards["cards"].count == 0:
        raise ValueError("No cards were generated.")

    # Iterate through each card to validate and convert its image.
    for card in typstCards["cards"]:
        if card["image"] == "":
            continue
        # Find the image file the card links to and check if it's in the input directory.
        imageFilePath = Path(f"{params.inputDirectoryPath}/{card['image']}")
        # If it isn't, set the card's image to "" so that the Typst template doesn't try to use a file that doesn't exist.
        if not imageValidation.is_image(imageFilePath):
            card["image"] = ""
            continue
        # If it is, check whether its extension matches its MIME type.
        if not imageValidation.does_extension_match(imageFilePath):
            # If it doesn't, convert the image to the correct format.
            newFilepath = imageValidation.new_file_from_mimetype(imageFilePath)
            card["image"] = newFilepath.name
        # Copy the image to the output directory.
        destinationFilePath = Path(outputFilePath).parent / card["image"]
        copy(imageFilePath, destinationFilePath)

    # Write the Typst YAML to a file
    with open(outputFilePath, "w") as file:
        yaml.dump(data=typstCards, stream=file, Dumper=yaml.SafeDumper)
    print(f"Successfully wrote {outputFilePath}.")
