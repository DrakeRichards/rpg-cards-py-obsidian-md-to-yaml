import unittest
from pathlib import Path

import utils.image as image


class TestImageValidation(unittest.TestCase):
    # Tests to verify and modify the extensions of image files.
    # 1. Check if a file is an image.
    # 2. Check if the file extension matches the file type.
    # 3. Rename a file with a mismatched extension to match the file type.

    def setUp(self) -> None:
        # Set up the file paths for the tests.
        self.IMAGE_FILE: Path = Path("test/files/image-good.jpg")
        self.TEXT_FILE: Path = Path("test/files/text.txt")
        self.MISMATCHED_FILE: Path = Path("test/files/image-mismatched.png")

    def test_is_image(self):
        # Test 1: Check if a file is an image.
        # Expected Result: The function should return True for an image file and False for a text file.
        self.assertTrue(image.is_image(self.IMAGE_FILE))
        self.assertFalse(image.is_image(self.TEXT_FILE))

    def test_does_extension_match(self):
        # Test 2: Check if the file extension matches the file type.
        # Expected Result: The function should return True for an image file and False for a mismatched file.
        self.assertTrue(image.does_extension_match(self.IMAGE_FILE))
        self.assertFalse(image.does_extension_match(self.MISMATCHED_FILE))

    def test_fix_mismatched_extension(self):
        # Test 3: Rename a file with a mismatched extension to match the file type.
        # Expected Result: The function should return a Path object with the correct extension.
        new_filepath = image.new_file_from_mimetype(self.MISMATCHED_FILE)
        self.assertEqual(new_filepath, self.MISMATCHED_FILE.with_suffix(".jpg"))
        self.assertTrue(new_filepath.exists())

    def tearDown(self) -> None:
        # Clean up the new file created by the test.
        new_filepath = self.MISMATCHED_FILE.with_suffix(".jpg")
        if new_filepath.exists():
            new_filepath.unlink()


if __name__ == "__main__":
    unittest.main()
