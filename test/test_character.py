import unittest
from dataclasses import asdict
from pathlib import Path

import yaml
from jsonschema import ValidationError

import obsidian.parser
import obsidian.rpg_pages
import typst


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
        # Generate an ObsidianCharacter object from the character markdown file.
        self.character_data: obsidian.rpg_pages.Character = (
            obsidian.rpg_pages.Character(self.CHARACTER_MARKDOWN_STANDARD)
        )
        # Generate a TypstCharacter object from the ObsidianCharacter object.
        self.character_typst: typst.Card = self.character_data.to_typst_card()
        self.character_dict: dict = asdict(self.character_typst)
        self.cards: dict[str, list[dict]] = {"cards": [self.character_dict]}
        self.cards_yaml: str = yaml.dump(self.cards)

    def test_identify_page_type(self):
        # Test 1: Properly identify a given markdown file as a character.
        # Expected Result: The function should return "character".
        page_type = obsidian.rpg_pages.get_page_type(self.CHARACTER_MARKDOWN_STANDARD)
        self.assertEqual(page_type, obsidian.rpg_pages.PageTypes.CHARACTER)

    def test_generate_obsidian_character(self):
        # Test 2: Generate an ObsidianCharacter object from a character markdown string.
        # Expected Result: The function should return an ObsidianCharacter object.
        self.assertIsInstance(self.character_data, obsidian.rpg_pages.Character)

    def test_generate_typst_character(self):
        # Test 3: Generate a TypstCharacter object from an ObsidianCharacter object.
        # Expected Result: The function should return a TypstCharacter object.
        self.assertIsInstance(self.character_typst, typst.Card)

    def test_validate_typst_character(self):
        # Test 4: Validate the TypstCharacter object using the rpgCardInterface.validateSchema method.
        # Expected Result: The function should return True.
        self.assertTrue(self.character_typst.validate_schema())

    def test_generate_data_yaml(self):
        # Test 5: Generate a data.yaml file from the TypstCharacter object.
        # Expected Result: The function should return a string.
        self.assertIsInstance(self.cards_yaml, str)

    def test_validate_data_yaml(self):
        # Test 6: Validate the data.yaml file against the remote rpg-cards-typst schema.
        # Expected Result: The function should return True.
        try:
            self.character_typst.validate_schema()
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
        character_data: obsidian.rpg_pages.Character = obsidian.rpg_pages.Character(
            character_markdown
        )
        self.assertIsInstance(character_data, obsidian.rpg_pages.Character)


if __name__ == "__main__":
    unittest.main()
