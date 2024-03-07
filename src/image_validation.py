"""
Tools to verify and modify the extensions of image files.
"""

import shutil
from pathlib import Path

import magic


def is_image(filepath: Path) -> bool:
    """
    Check if a file is an image.

    Args:
        file_path (Path): The path to the file.

    Returns:
        bool: True if the file is an image, False if not.
    """
    file_path_str = str(filepath.resolve())
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path_str)
    return file_type.startswith("image")


def does_extension_match(filepath: Path) -> bool:
    """
    Check if the file extension matches the file type.

    Args:
        filepath (Path): The path to the file.

    Returns:
        bool: True if the extension matches the file type, False if not.
    """
    file_path_str = str(filepath.resolve())
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path_str)
    mime_extension = mime_type.split("/")[1]
    if mime_extension == "jpeg":
        mime_extension = "jpg"
    file_extension = filepath.suffix.replace(".", "")
    return mime_extension == file_extension


def copy_file_from_mimetype(filepath: Path) -> Path:
    """
    Make a copy of a file with a mismatched extension to match the file type.

    Args:
        filepath (Path): The path to the original file.

    Returns:
        Path: The path to the new file.
    """
    file_path_str = str(filepath.resolve())
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path_str)
    mime_extension = mime_type.split("/")[1]
    if mime_extension == "jpeg":
        mime_extension = "jpg"
    new_filepath = filepath.with_suffix("." + mime_extension)
    shutil.copy(filepath, new_filepath)
    return new_filepath
