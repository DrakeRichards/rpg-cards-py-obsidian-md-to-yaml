import unittest
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml
from attr import dataclass
from jsonschema import ValidationError

import obsidian
import typst


class TestCard(unittest.TestCase):
    # Tests to determine if we can generate a data.yaml file from each type of markdown file.
    # 1. Properly identify a given markdown file as the appropriate type.
    # 2. Generate an RpgData object from a markdown string.
    # 3. Generate a Typst Card object from an RpgData object.
    # 4. Validate the Typst Card object against the rpg-cards-typst schema.
    # 5. Generate a data.yaml file from the Typst Card object.
    # 6. Validate the data.yaml file against the rpg-cards-typst schema.

    def setUp(self) -> None:

        @dataclass
        class InputFile:
            type: obsidian.rpg_pages.PageTypes
            path: Path

        @dataclass
        class TestingFile:
            input_file: InputFile

            @property
            def type(self) -> obsidian.rpg_pages.PageTypes:
                return self.input_file.type

            @property
            def path(self) -> Path:
                return self.input_file.path

            @property
            def markdown_text(self) -> str:
                return self.input_file.path.read_text()

            @property
            def page_data(self) -> obsidian.rpg_pages.RpgData:
                return obsidian.rpg_pages.new_page(self.markdown_text)

            @property
            def card_obj(self) -> typst.Card:
                return self.page_data.to_typst_card()

            @property
            def card_dict(self) -> dict:
                return asdict(self.card_obj)

            @property
            def cards(self) -> dict[str, list[dict]]:
                return {"cards": [self.card_dict]}

            @property
            def cards_yaml(self) -> str:
                return yaml.dump(self.cards)

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
        # Test 1: Properly identify a given markdown file.
        # Expected Result: The function should return the correct PageType.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                page_type = obsidian.rpg_pages.get_page_type(
                    testing_file.path.read_text()
                )
                self.assertEqual(page_type, testing_file.type)

    def test_generate_obsidian_object(self):
        # Test 2: Generate an RpgData object from a character markdown string.
        # Expected Result: The function should return an RpgData object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(
                    testing_file.page_data, obsidian.rpg_pages.RpgData
                )

    def test_generate_typst_character(self):
        # Test 3: Generate a Typst Card object from an RpgData object.
        # Expected Result: The function should return a Typst Card object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.card_obj, typst.Card)

    def test_validate_typst_character(self):
        # Test 4: Validate the Typst Card object using the validateSchema method.
        # Expected Result: The function should return True.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertTrue(testing_file.card_obj.validate_schema())

    def test_generate_data_yaml(self):
        # Test 5: Generate a data.yaml file from the Typst Card object.
        # Expected Result: The function should return a string.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.cards_yaml, str)

    def test_validate_data_yaml(self):
        # Test 6: Validate the data.yaml file against the rpg-cards-typst schema.
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
    # Test what happens when the input files are not formatted correctly.

    def test_extra_headers(self):
        # What happens when the markdown file has extra headers?
        # Expected Result: The function should return an ObsidianCharacter object, and the extra headers should be ignored.
        character_markdown_file: Path = Path("test/files/character-extra-headers.md")
        character_markdown: str = character_markdown_file.read_text()
        character_data: obsidian.rpg_pages.Character = obsidian.rpg_pages.Character(
            character_markdown
        )
        self.assertIsInstance(character_data, obsidian.rpg_pages.Character)

    # TODO: Single-header input files for each card type.


if __name__ == "__main__":
    unittest.main()
