"""
Called from the command line to convert an Obsidian character markdown file to a YAML file.

Args:
    
    - `inputFile (str)`: The input file to parse.
    - `outputDirectory (str)`: The output directory to write the YAML file to.

Returns:

    - None

Example:
    
    - `python convert_character.py test/files/test.md test/files`
"""

import argparse
from src.markdown_to_typst_yaml import markdown_to_yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse a character file and output a YAML file."
    )
    parser.add_argument("inputFile", help="The input file to parse.")
    parser.add_argument(
        "outputDirectory", help="The output directory to write the YAML file to."
    )
    args = parser.parse_args()

    markdown_to_yaml(args.inputFile, args.outputDirectory)
