def get_lower_keys(content: dict[str, str]) -> dict[str, str]:
    """Converts the keys of a dictionary to lowercase.

    Args:
        content (dict[str, str]): A dictionary.

    Returns:
        dict[str, str]: A dictionary with lowercase keys.
    """
    lower_keys = {k.lower(): v for k, v in content.items()}
    return lower_keys
