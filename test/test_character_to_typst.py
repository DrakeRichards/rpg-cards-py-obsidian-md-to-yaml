import unittest
from src.obsidian_page_types import ObsidianCharacter as ObsidianCharacter
from src.typst_template_types import TypstCharacter as TypstCharacter


class TestCharacterToTypst(unittest.TestCase):

    def test_character_to_typst(self):
        # Test the character_to_typst function.
        # Test 1: Test the character_to_typst function with a simple character object.
        # Expected Result: The function should return a dict that validates against schemas/rpg-cards-typst-templates/schemas/character.schema.json.
        with open("test/files/example.md", "r") as file:
            text = file.read()
            character_data: ObsidianCharacter = ObsidianCharacter(text)
        character_typst: TypstCharacter = TypstCharacter(character_data)
        self.assertIsInstance(character_typst, TypstCharacter)
        self.assertTrue(character_typst.validateSchema())


if __name__ == "__main__":
    unittest.main()
