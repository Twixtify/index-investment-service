from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """
    Interface for scraping a static web page.
    """

    @property
    @abstractmethod
    def response(self) -> str:
        pass

    @abstractmethod
    def run(self) -> None:
        """Make a GET request to the target URL"""
        pass
