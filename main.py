import src.obsidian_page_types as obsidianPages
from src.typst_card_abc import rpgCardInterface
from typing import List
import src.typst_template_types as typstTemplates
import yaml
import argparse
from dataclasses import asdict

parser = argparse.ArgumentParser(
    description="Converts Obsidian markdown files to Typst JSON."
)
parser.add_argument(
    "inputDirectoryPath",
    help="The path to the directory containing the markdown files.",
)
parser.add_argument("outputFilePath", help="The path to the output JSON file.")
params = parser.parse_args()


def getMarkdownFiles(directoryPath: str) -> List[str]:
    """Returns a list of all markdown files in a directory."""
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]
    markdownFiles = [f for f in files if f.endswith(".md")]
    return [f"{directoryPath}/{file}" for file in markdownFiles]


if __name__ == "__main__":
    markdownFiles = getMarkdownFiles(params.inputDirectoryPath)
    outputFilePath = params.outputFilePath
    typstCards = {"cards": []}
    for file in markdownFiles:
        with open(file, "r") as file:
            text: str = file.read()
            pageObject: obsidianPages.RpgData = obsidianPages.newPage(text)
            pageTypst: rpgCardInterface = typstTemplates.fromPageObject(pageObject)
            typstCards["cards"].append(asdict(pageTypst))
    with open(outputFilePath, "w") as file:
        yaml.dump(data=typstCards, stream=file, Dumper=yaml.SafeDumper)
    print(f"Successfully wrote {outputFilePath}.")
