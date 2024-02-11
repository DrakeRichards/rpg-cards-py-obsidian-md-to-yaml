import unittest
from src.markdown_to_typst_yaml import markdown_to_yaml
from pathlib import Path
from yaml import load, FullLoader


class TestMarkdownToTypstYaml(unittest.TestCase):
    def test_markdown_to_typst_yaml(self):
        # Test that the function works.
        markdown_to_yaml("test/files/example.md", "test/files")

        # Test that the file was created.
        self.assertTrue(Path("test/files/Nelra Treewhisper.yaml").exists())

        # Test that the file has the correct content.
        # Parse the YAML file into a dict and compare it to the expected dict.
        yaml_text = """
bodyText: Nelra Treewhisper is deeply connected to the urban creatures of Waterdeep.
  Known as a protector of city pests and vermin, Nelra acts as a bridge between their
  world and the world of Waterdeep's denizens, standing up for their rights, and providing
  valuable information from the city streets.
image: 1697169189.png
imageSubtext: Female Wood Elf
lists:
- items:
  - name: Quirk
    value: She habitually takes in strays and tends to whisper when conversing.
  - name: Likes
    value: Cross-species communication, liberty of urban wildlife, shadowy corners.
  - name: Dislikes
    value: People who dismiss the importance of small creatures, cages, excessive
      noise.
  title: Personality
- items:
    - name: Location
      value: North Ward
  title: ''
name: Nelra Treewhisper
nameSubtext: Information Broker and Verdant Advocate
"""
        expected_dict = load(yaml_text, Loader=FullLoader)
        actual_dict = load(
            Path("test/files/Nelra Treewhisper.yaml").read_text(), Loader=FullLoader
        )
        self.assertEqual(expected_dict, actual_dict)
