import unittest
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml
from attr import dataclass
from jsonschema import ValidationError

import obsidian
import typst


class TestCard(unittest.TestCase):
    # Tests to determine if we can generate a data.yaml file from a character markdown file.
    # 1. Properly identify a given markdown file as a character.
    # 2. Generate an ObsidianCharacter object from a character markdown string.
    # 3. Generate a TypstCharacter object from an ObsidianCharacter object.
    # 4. Validate the TypstCharacter object using the rpgCardInterface.validateSchema method.
    # 5. Generate a data.yaml file from the TypstCharacter object.
    # 6. Validate the data.yaml file against the remote rpg-cards-typst schema.

    def setUp(self) -> None:

        @dataclass
        class InputFile:
            type: obsidian.rpg_pages.PageTypes
            path: Path

        @dataclass
        class TestingFile:
            type: obsidian.rpg_pages.PageTypes
            path: Path
            markdown_text: str
            page_data: obsidian.rpg_pages.RpgData
            card_obj: typst.Card
            card_dict: dict
            cards: dict[str, list[dict]]
            cards_yaml: str

            def __init__(self, input_file: InputFile):
                self.type = input_file.type
                self.path = input_file.path
                self.markdown_text = input_file.path.read_text()
                self.page_data = obsidian.rpg_pages.new_page(self.markdown_text)
                self.card_obj = self.page_data.to_typst_card()
                self.card_dict = asdict(self.card_obj)
                self.cards = {"cards": [self.card_dict]}
                self.cards_yaml = yaml.dump(self.cards)

        self.input_files: list[InputFile] = [
            InputFile(
                obsidian.rpg_pages.PageTypes.CHARACTER, Path("test/files/character.md")
            ),
            InputFile(
                obsidian.rpg_pages.PageTypes.LOCATION, Path("test/files/location.md")
            ),
            InputFile(obsidian.rpg_pages.PageTypes.ITEM, Path("test/files/item.md")),
        ]

        self.testing_files: list[TestingFile] = [
            TestingFile(input_file) for input_file in self.input_files
        ]

    def test_identify_page_type(self):
        # Test 1: Properly identify a given markdown file as a character.
        # Expected Result: The function should return "character".
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                page_type = obsidian.rpg_pages.get_page_type(
                    testing_file.path.read_text()
                )
                self.assertEqual(page_type, testing_file.type)

    def test_generate_obsidian_object(self):
        # Test 2: Generate an ObsidianCharacter object from a character markdown string.
        # Expected Result: The function should return an ObsidianCharacter object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(
                    testing_file.page_data, obsidian.rpg_pages.RpgData
                )

    def test_generate_typst_character(self):
        # Test 3: Generate a TypstCharacter object from an ObsidianCharacter object.
        # Expected Result: The function should return a TypstCharacter object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.card_obj, typst.Card)

    def test_validate_typst_character(self):
        # Test 4: Validate the TypstCharacter object using the rpgCardInterface.validateSchema method.
        # Expected Result: The function should return True.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertTrue(testing_file.card_obj.validate_schema())

    def test_generate_data_yaml(self):
        # Test 5: Generate a data.yaml file from the TypstCharacter object.
        # Expected Result: The function should return a string.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.cards_yaml, str)

    def test_validate_data_yaml(self):
        # Test 6: Validate the data.yaml file against the remote rpg-cards-typst schema.
        # Expected Result: The function should return True.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                try:
                    testing_file.card_obj.validate_schema()
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
