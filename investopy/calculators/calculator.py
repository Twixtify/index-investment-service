from abc import ABC, abstractmethod
from typing import TypeVar

from pandas import DataFrame

T = TypeVar('T', bound=DataFrame)


class Calculator(ABC):
    """Perform calculation(s) for portfolios."""

    @abstractmethod
    def prepare_data(self, stocks: T, portfolio: T) -> None:
        """Structure and extract data for calculation"""
        ...

    @abstractmethod
    def run(self):
        """Run a calculation and return the result"""
        ...
