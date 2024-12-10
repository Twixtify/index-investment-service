from abc import ABC, abstractmethod

from pandas import DataFrame


class BaseParser(ABC):
    """
    Interface for parsing a html web page.
    """

    @abstractmethod
    def parse_content(self, html: str) -> DataFrame:
        """Parse html content"""
        pass
