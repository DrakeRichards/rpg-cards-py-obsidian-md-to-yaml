import unittest
from dataclasses import asdict
from pathlib import Path

import yaml
from jsonschema import ValidationError

import src.obsidian_rpg as obsidian_rpg
from src.typst import TypstCharacter as TypstCharacter


class TestCharacter(unittest.TestCase):
    # Tests to determine if we can generate a data.yaml file from a character markdown file.
    # 1. Properly identify a given markdown file as a character.
    # 2. Generate an ObsidianCharacter object from a character markdown string.
    # 3. Generate a TypstCharacter object from an ObsidianCharacter object.
    # 4. Validate the TypstCharacter object using the rpgCardInterface.validateSchema method.
    # 5. Generate a data.yaml file from the TypstCharacter object.
    # 6. Validate the data.yaml file against the remote rpg-cards-typst schema.

    def setUp(self) -> None:
        # Read the character markdown file.
        character_markdown_file: Path = Path("test/files/standard-character.md")
        self.CHARACTER_MARKDOWN_STANDARD: str = character_markdown_file.read_text()

    def test_identify_page_type(self):
        # Test 1: Properly identify a given markdown file as a character.
        # Expected Result: The function should return "character".
        page_type = obsidian_rpg.get_page_type(self.CHARACTER_MARKDOWN_STANDARD)
        self.assertEqual(page_type, obsidian_rpg.ObsidianPageTypes.CHARACTER)

    def test_generate_obsidian_character(self):
        # Test 2: Generate an ObsidianCharacter object from a character markdown string.
        # Expected Result: The function should return an ObsidianCharacter object.
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            self.CHARACTER_MARKDOWN_STANDARD
        )
        self.assertIsInstance(character_data, obsidian_rpg.ObsidianCharacter)

    def test_generate_typst_character(self):
        # Test 3: Generate a TypstCharacter object from an ObsidianCharacter object.
        # Expected Result: The function should return a TypstCharacter object.
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            self.CHARACTER_MARKDOWN_STANDARD
        )
        character_typst: TypstCharacter = TypstCharacter(character_data)
        self.assertIsInstance(character_typst, TypstCharacter)

    def test_validate_typst_character(self):
        # Test 4: Validate the TypstCharacter object using the rpgCardInterface.validateSchema method.
        # Expected Result: The function should return True.
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            self.CHARACTER_MARKDOWN_STANDARD
        )
        character_typst: TypstCharacter = TypstCharacter(character_data)
        self.assertTrue(character_typst.validate_schema())

    def test_generate_data_yaml(self):
        # Test 5: Generate a data.yaml file from the TypstCharacter object.
        # Expected Result: The function should return a string.
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            self.CHARACTER_MARKDOWN_STANDARD
        )
        character_typst: TypstCharacter = TypstCharacter(character_data)
        character_dict: dict = asdict(character_typst)
        data = {"cards": [character_dict]}
        data_yaml: str = yaml.dump(data)
        self.assertIsInstance(data_yaml, str)

    def test_validate_data_yaml(self):
        # Test 6: Validate the data.yaml file against the remote rpg-cards-typst schema.
        # Expected Result: The function should return True.
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            self.CHARACTER_MARKDOWN_STANDARD
        )
        character_typst: TypstCharacter = TypstCharacter(character_data)
        try:
            character_typst.validate_schema()
            is_valid = True
        except ValidationError:
            is_valid = False
        self.assertTrue(is_valid)


class EdgeCases(unittest.TestCase):
    # Tests what happens when the input files are not formatted correctly.

    def test_extra_headers(self):
        # What happens when the markdown file has extra headers?
        # Expected Result: The function should return an ObsidianCharacter object, and the extra headers should be ignored.
        character_markdown_file: Path = Path("test/files/extra-headers-character.md")
        character_markdown: str = character_markdown_file.read_text()
        character_data: obsidian_rpg.ObsidianCharacter = obsidian_rpg.ObsidianCharacter(
            character_markdown
        )
        self.assertIsInstance(character_data, obsidian_rpg.ObsidianCharacter)


if __name__ == "__main__":
    unittest.main()
