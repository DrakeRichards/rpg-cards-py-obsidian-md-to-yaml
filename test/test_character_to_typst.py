import unittest
from src.page_types.character import Character
from src.interfaces.character_to_typst import TypstCharacter
from jsonschema import validate
from json import load
from dataclasses import asdict


class TestCharacterToTypst(unittest.TestCase):

    def test_character_to_typst(self):
        # Test the character_to_typst function.
        # Test 1: Test the character_to_typst function with a simple character object.
        # Expected Result: The function should return a dict that validates against schemas/rpg-cards-typst-templates/schemas/character.schema.json.
        with open("test/files/example.md", "r") as file:
            text = file.read()
            character_data: Character = Character.from_markdown(text)
        character_typst: TypstCharacter = TypstCharacter.from_character(character_data)
        character_dict = asdict(character_typst)
        # Validate the character_typst object against the schema.
        with open(
            "schemas/rpg-cards-typst-templates/schemas/character.schema.json"
        ) as file:
            schema = load(file)
            try:
                validate(character_dict, schema)
                is_valid = True
            except "ValidationError":
                is_valid = False
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()
