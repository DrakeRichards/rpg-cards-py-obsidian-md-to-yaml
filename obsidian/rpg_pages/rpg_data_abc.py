from abc import ABC, abstractmethod
from dataclasses import dataclass

import typst

from ..parser import MarkdownData


@dataclass
class RpgData(ABC):
    """
    Base class for each of the types of Obsidian pages.
    """

    input_data: MarkdownData | str

    @property
    def markdown_data(self) -> MarkdownData:
        if isinstance(self.input_data, str):
            return MarkdownData(self.input_data)
        return self.input_data

    @property
    def name(self) -> str:
        # The name of the character should be H1, which is the key of the top-level element.
        return list(self.markdown_data.headers_all.keys())[0]

    @property
    def description(self) -> str:
        # There is a description header, and it's a string.
        if "Description" in self.markdown_data.headers and isinstance(
            self.markdown_data.headers["Description"], str
        ):
            return self.markdown_data.headers["Description"]
        # There is no description header, but the top-level header's content is a string.
        if self.name in self.markdown_data.headers.keys() and isinstance(
            self.markdown_data.headers[self.name], str
        ):
            return self.markdown_data.headers[self.name]  # type: ignore
        return ""

    @property
    def image(self) -> str:
        if self.markdown_data.images:
            return self.markdown_data.images[0]
        return ""

    @abstractmethod
    def to_typst_card(self) -> typst.Card:
        """
        Converts the data to a TypstCard.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")
