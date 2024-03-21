import unittest

import obsidian.parser as op
import utils.string as sutil


class TestObsidianTools(unittest.TestCase):

    def setUp(self) -> None:
        self.text = ""
        with open("test/files/test.md", "r") as file:
            self.text = file.read()
            file.close()
        self.data = op.MarkdownData(self.text)

    def test_get_frontmatter(self):
        # Test the get_frontmatter function.
        # Test 1: Test the get_frontmatter function with a simple markdown file.
        # File is located in test/files/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        self.assertEqual(
            self.data.frontmatter, {"title": "Example", "tags": "example, test"}
        )

    def test_get_frontmatter_with_double_brackets(self):
        # Test the get_frontmatter function with double brackets.
        # Test 1: Test the get_frontmatter function with a markdown file that contains double brackets.
        # File is located in test/files/test_with_double_brackets.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/test_with_double_brackets.md", "r") as file:
            text = file.read()
            frontmatter = op.MarkdownData(text).frontmatter
            self.assertEqual(frontmatter, {"title": "Example", "doubled": "foo"})

    def test_get_dataview_fields(self):
        # Test the get_dataview_fields function.
        # Test 1: Test the get_dataview_fields function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        self.assertEqual(self.data.dataview_fields, {"foo": ["bar"], "baz": ["qux"]})

    def test_get_images(self):
        # Test the get_images function.
        # Test 1: Test the get_images function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a list with the expected structure.
        self.assertEqual(self.data.images, ["image1.png", "image2.jpg"])

    def test_get_content(self):
        # Test the get_content function.
        # Test 1: Test the get_content function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        self.assertEqual(
            self.data.headers_all,
            {
                "Example Header 1": {
                    "Example Header 2": {
                        "Example Header 3": ["List item 1", "List item 2"],
                        "Example Header 3-1": "This text should get captured.",
                    }
                }
            },
        )

    def test_remove_wikilinks(self):
        # Test the remove_wikilinks function.
        # Test 1: Test the remove_wikilinks function with a simple markdown string.
        # Expected Result: The function should return a string with the expected structure.
        text = "This is a [[wikilink]]."
        result = sutil.remove_wikilinks(text)
        self.assertEqual(result, "This is a wikilink.")
        # Test 2: Test the remove_wikilinks function with a markdown string that contains an embedded wikilink.
        embedded_text = "This is an ![[embedded wikilink]]."
        embedded_text_result = sutil.remove_wikilinks(embedded_text)
        self.assertEqual(embedded_text_result, "This is an ![[embedded wikilink]].")
        # Test 3: Test the remove_wikilinks function with a markdown string that contains multiple wikilinks.
        multiple_text = "This is a [[wikilink]]. This is another [[wikilink]]."
        multiple_text_result = sutil.remove_wikilinks(multiple_text)
        self.assertEqual(
            multiple_text_result, "This is a wikilink. This is another wikilink."
        )
        # Test 4: Test the remove_wikilinks function with a markdown string that contains a wikilink with alt text.
        alt_text = "This is a [[wikilink|with alt text]]."
        alt_text_result = sutil.remove_wikilinks(alt_text)
        self.assertEqual(alt_text_result, "This is a with alt text.")

    def test_obsidian_page_data(self):
        # Test the ObsidianPageData class.
        # Test 1: Test the ObsidianPageData class with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The class should return a dictionary with the expected structure.
        self.assertEqual(
            self.data.headers_all,
            {
                "Example Header 1": {
                    "Example Header 2": {
                        "Example Header 3": ["List item 1", "List item 2"],
                        "Example Header 3-1": "This text should get captured.",
                    }
                }
            },
        )
        self.assertEqual(
            self.data.frontmatter, {"title": "Example", "tags": "example, test"}
        )
        self.assertEqual(self.data.dataview_fields, {"foo": ["bar"], "baz": ["qux"]})
        self.assertEqual(self.data.images, ["image1.png", "image2.jpg"])


if __name__ == "__main__":
    unittest.main()
