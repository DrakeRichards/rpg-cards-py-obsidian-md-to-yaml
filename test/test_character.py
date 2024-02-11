import unittest
from src.obsidian_page_types import Character
from dataclasses import asdict


class TestCharacter(unittest.TestCase):

    def test_parse(self):
        # Test the parse function.
        # Test 1: Test the parse function with a simple markdown file.
        # File is located in test/files/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/example.md", "r") as file:
            text = file.read()
            character_data = Character.from_markdown(text)
        example_character_data = {
            "name": "Nelra Treewhisper",
            "physicalInfo": {
                "gender": "Female",
                "race": "Wood Elf",
                "job": "Information Broker and Verdant Advocate",
            },
            "description": {
                "overview": "Nelra Treewhisper is deeply connected to the urban creatures of Waterdeep. Known as a protector of city pests and vermin, Nelra acts as a bridge between their world and the world of Waterdeep's denizens, standing up for their rights, and providing valuable information from the city streets.",
                "looks": "With leaf-green eyes that mirror the verdancy of nature, Nelra is a slender elf with waist-length chestnut hair, usually adorned with small creatures. Her attire usually includes worn-out leather boots, a cloak decorated with feathers and bones, and a well-worn hat.",
                "voice": "Nelra's voice is melodious, with a soft and gentle pitch, occasionally punctuated with chirping and squeaking noises.",
            },
            "personality": {
                "quirk": "She habitually takes in strays and tends to whisper when conversing.",
                "likes": "Cross-species communication, liberty of urban wildlife, shadowy corners.",
                "dislikes": "People who dismiss the importance of small creatures, cages, excessive noise.",
            },
            "hooks": {
                "goals": "Nelra wishes to create safe passages and homes for the city's vermin and ensure a harmonious existence between them and the city folk. Her ultimate goal is to make Waterdeep a haven for all creatures, big and small.",
                "frustration": "There's a rumor circulating that the city council plans to exterminate the city's rat population, and Nelra is straining to obtain concrete details to stop them.",
            },
            "image": "1697169189.png",
            "location": None,
            "groupName": "The Possums",
            "groupTitle": "",
            "groupRank": "3",
        }
        self.assertEqual(asdict(character_data), example_character_data)


if __name__ == "__main__":
    unittest.main()
