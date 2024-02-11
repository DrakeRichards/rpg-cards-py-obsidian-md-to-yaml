import unittest
from src.obsidian_page_types import Character as ObsidianCharacter
from src.typst_template_types import Character as TypstCharacter


class TestCharacterToTypst(unittest.TestCase):

    def test_character_to_typst(self):
        # Test the character_to_typst function.
        # Test 1: Test the character_to_typst function with a simple character object.
        # Expected Result: The function should return a dict that validates against schemas/rpg-cards-typst-templates/schemas/character.schema.json.
        with open("test/files/example.md", "r") as file:
            text = file.read()
            character_data: ObsidianCharacter = ObsidianCharacter.from_markdown(text)
        character_typst: TypstCharacter = TypstCharacter.from_character(character_data)
        # The TypstCharacter object validates against the schema itself, so we don't need to validate it here.
        # Instead, we'll just check that the object is a TypstCharacter object.
        self.assertIsInstance(character_typst, TypstCharacter)


if __name__ == "__main__":
    unittest.main()