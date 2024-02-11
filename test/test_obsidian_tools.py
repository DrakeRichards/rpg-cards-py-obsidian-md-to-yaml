import unittest
import src.obsidian_tools as ot


class TestObsidianTools(unittest.TestCase):

    def test_get_frontmatter(self):
        # Test the get_frontmatter function.
        # Test 1: Test the get_frontmatter function with a simple markdown file.
        # File is located in test/files/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/test.md", "r") as file:
            text = file.read()
            frontmatter = ot.get_frontmatter(text)
            self.assertEqual(frontmatter, {"title": "Example", "tags": "example, test"})

    def test_get_frontmatter_with_double_brackets(self):
        # Test the get_frontmatter function with double brackets.
        # Test 1: Test the get_frontmatter function with a markdown file that contains double brackets.
        # File is located in test/files/test_with_double_brackets.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/test_with_double_brackets.md", "r") as file:
            text = file.read()
            frontmatter = ot.get_frontmatter(text)
            self.assertEqual(frontmatter, {"title": "Example", "doubled": "foo"})

    def test_get_dataview_fields(self):
        # Test the get_dataview_fields function.
        # Test 1: Test the get_dataview_fields function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/test.md", "r") as file:
            text = file.read()
            dataview_fields = ot.get_dataview_fields(text)
            self.assertEqual(dataview_fields, {"foo": ["bar"], "baz": ["qux"]})

    def test_get_images(self):
        # Test the get_images function.
        # Test 1: Test the get_images function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a list with the expected structure.
        with open("test/files/test.md", "r") as file:
            text = file.read()
            images = ot.get_images(text)
            self.assertEqual(images, ["image1.png", "image2.jpg"])

    def test_get_content(self):
        # Test the get_content function.
        # Test 1: Test the get_content function with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The function should return a dictionary with the expected structure.
        with open("test/files/test.md", "r") as file:
            text = file.read()
            content = ot.get_content(text)
            print(content)
            self.assertEqual(
                content,
                {
                    "Example Header 1": {
                        "Example Header 2": {
                            "Example Header 3": ["List item 1", "List item 2"],
                            "Example Header 3-1": "This text should get captured.",
                        }
                    }
                },
            )

    def test_ObsidianPageData(self):
        # Test the ObsidianPageData class.
        # Test 1: Test the ObsidianPageData class with a simple markdown file.
        # File is located in test/test.md
        # Expected Result: The class should return a dictionary with the expected structure.
        with open("test/files/test.md", "r") as file:
            text = file.read()
            page = ot.ObsidianPageData(text)
            self.assertEqual(
                page.content,
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
                page.frontmatter, {"title": "Example", "tags": "example, test"}
            )
            self.assertEqual(page.dataview_fields, {"foo": ["bar"], "baz": ["qux"]})
            self.assertEqual(page.images, ["image1.png", "image2.jpg"])


if __name__ == "__main__":
    unittest.main()
