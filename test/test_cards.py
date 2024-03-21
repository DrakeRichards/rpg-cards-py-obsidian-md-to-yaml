import unittest
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml
from attr import dataclass
from jsonschema import ValidationError

import obsidian.rpg_pages as pages
import typst


class TestCard(unittest.TestCase):
    # Tests to determine if we can generate a data.yaml file from each type of markdown file.
    def setUp(self) -> None:

        @dataclass
        class InputFile:
            type: pages.PageTypes
            path: Path

        @dataclass
        class TestingFile:
            input_file: InputFile

            @property
            def type(self) -> pages.PageTypes:
                return self.input_file.type

            @property
            def path(self) -> Path:
                return self.input_file.path

            @property
            def markdown_text(self) -> str:
                return self.input_file.path.read_text()

            @property
            def page_data(self) -> pages.rpg_data_abc.RpgData:
                return pages.new_page(self.markdown_text)

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
            InputFile(pages.PageTypes.CHARACTER, Path("test/files/character.md")),
            InputFile(pages.PageTypes.LOCATION, Path("test/files/location.md")),
            InputFile(pages.PageTypes.ITEM, Path("test/files/item.md")),
        ]

        self.testing_files: list[TestingFile] = [
            TestingFile(input_file) for input_file in self.input_files
        ]

    def test_identify_page_type(self):
        # Properly identify a given markdown file.
        # Expected Result: The function should return the correct PageType.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                page_type = pages.get_page_type(testing_file.path.read_text())
                self.assertEqual(page_type, testing_file.type)

    def test_generate_obsidian_object(self):
        # Generate an RpgData object from a character markdown string.
        # Expected Result: The function should return an RpgData object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(
                    testing_file.page_data, pages.rpg_data_abc.RpgData
                )

    def test_generate_typst_character(self):
        # Generate a Typst Card object from an RpgData object.
        # Expected Result: The function should return a Typst Card object.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.card_obj, typst.Card)

    def test_validate_typst_character(self):
        # Validate the Typst Card object using the validateSchema method.
        # Expected Result: The function should return True.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertTrue(testing_file.card_obj.validate_schema())

    def test_generate_data_yaml(self):
        # Generate a data.yaml file from the Typst Card object.
        # Expected Result: The function should return a string.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                self.assertIsInstance(testing_file.cards_yaml, str)

    def test_validate_data_yaml(self):
        # Validate the data.yaml file against the rpg-cards-typst schema.
        # Expected Result: The function should return True.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                try:
                    testing_file.card_obj.validate_schema()
                    is_valid = True
                except ValidationError:
                    is_valid = False
                self.assertTrue(is_valid)

    def test_content(self):
        # Test most of the content the card_obj object.
        # Doesn't test the lists because I don't feel like writing that.
        for testing_file in self.testing_files:
            with self.subTest(input_file=testing_file):
                match testing_file.type:
                    case pages.PageTypes.CHARACTER:
                        self.assertEqual(
                            testing_file.card_obj.name, "Bob the Barbarian"
                        )
                        self.assertEqual(testing_file.card_obj.image, "image-good.jpg")
                        self.assertEqual(
                            testing_file.card_obj.body_text,
                            "Bob is a barbarian who has been traveling the world for many years. He is a skilled warrior and has a strong sense of justice.",
                        )
                        self.assertEqual(testing_file.card_obj.banner_color, "#800000")
                        self.assertEqual(
                            testing_file.card_obj.image_subtext, "Male Human"
                        )
                        self.assertEqual(
                            testing_file.card_obj.name_subtext, "Barbarian"
                        )
                        self.assertEqual(
                            testing_file.card_obj.template, "landscape-content-left"
                        )
                    case pages.PageTypes.LOCATION:
                        self.assertEqual(
                            testing_file.card_obj.name, "Spiceleaf Library"
                        )
                        self.assertEqual(testing_file.card_obj.image, "1696133819.png")
                        self.assertEqual(
                            testing_file.card_obj.body_text,
                            "The Spiceleaf Library is a grand two-story building with marble pillars and a large stained glass window depicting a world map. The shelves are filled with dusty tomes and ancient scrolls, while cozy reading nooks are scattered throughout the space.\n\nThe library specializes in foreign works that Madame Spiceleaf has collected throughout her travels. It also has collections of Waterdavian flatsheets and history books.",
                        )
                        self.assertEqual(testing_file.card_obj.banner_color, "#191970")
                        self.assertEqual(testing_file.card_obj.image_subtext, "")
                        self.assertEqual(
                            testing_file.card_obj.name_subtext, "North Ward"
                        )
                        self.assertEqual(
                            testing_file.card_obj.template, "landscape-content-right"
                        )
                    case pages.PageTypes.ITEM:
                        self.assertEqual(
                            testing_file.card_obj.name, "Dagger Of Trollsbane +1"
                        )
                        self.assertEqual(testing_file.card_obj.image, "1709939907.png")
                        self.assertEqual(
                            testing_file.card_obj.body_text,
                            "A +1 dagger forged for the Stormcrest Clan. Its hilt bears their family crest: a tower on a field of blue and white. Its blade seems to hum if you listen closely. It prevents the regeneration effect of trolls, just like fire, though it deals no fire damage itself.",
                        )
                        self.assertEqual(testing_file.card_obj.banner_color, "#195905")
                        self.assertEqual(testing_file.card_obj.image_subtext, "")
                        self.assertEqual(testing_file.card_obj.name_subtext, "Dagger")
                        self.assertEqual(
                            testing_file.card_obj.template, "landscape-content-right"
                        )


class EdgeCases(unittest.TestCase):
    # Test what happens when the input files are not formatted correctly.

    def test_extra_headers(self):
        # What happens when the markdown file has extra headers?
        # Expected Result: The function should return an ObsidianCharacter object, and the extra headers should be ignored.
        character_markdown_file: Path = Path("test/files/character-extra-headers.md")
        character_markdown: str = character_markdown_file.read_text()
        character_data: pages.character.Character = pages.character.Character(
            character_markdown
        )
        self.assertIsInstance(character_data, pages.character.Character)

    # TODO: Single-header input files for each card type.


if __name__ == "__main__":
    unittest.main()
