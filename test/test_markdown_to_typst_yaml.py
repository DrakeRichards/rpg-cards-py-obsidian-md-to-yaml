import unittest
from src.markdown_to_typst_yaml import markdown_to_yaml
from pathlib import Path
from yaml import load, FullLoader


class TestMarkdownToTypstYaml(unittest.TestCase):
    def test_markdown_to_typst_yaml(self):
        # Test that the function works.
        markdown_to_yaml("test/files/example.md", "test/files")

        # Test that the file was created.
        self.assertTrue(Path("test/files/example.yaml").exists())

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
  title: ''
- items:
    - name: Location
      value: North Ward
    - name: Member of
      value: The Possums
  title: ''
name: Nelra Treewhisper
nameSubtext: Information Broker and Verdant Advocate
"""
        expected_dict = load(yaml_text, Loader=FullLoader)
        actual_dict = load(
            Path("test/files/example.yaml").read_text(), Loader=FullLoader
        )
        self.assertEqual(expected_dict, actual_dict)

    def test_bad_input(self):
        # Test that the function raises an error when given a bad input file.
        with self.assertRaises(Exception):
            markdown_to_yaml("test/files/bad_input.md", "test/files")

    def test_grommok(self):
        # Test that the function works with the Grommok file.
        markdown_to_yaml("test/files/grommok.md", "test/files")

        # Test that the file was created.
        self.assertTrue(Path("test/files/grommok.yaml").exists())

    def test_gideon_ebonlocke(self):
        # Test that the function works with the Gideon Ebonlocke file.
        markdown_to_yaml("test/files/Gideon Ebonlocke.md", "test/files")

        # Test that the file was created.
        self.assertTrue(Path("test/files/Gideon Ebonlocke.yaml").exists())


if __name__ == "__main__":
    unittest.main()
