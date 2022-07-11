from typing import Protocol


class Portfolio(Protocol):
    """
    Protocol for survey an investment in a portfolio given a deposit.
    Inspired by the command pattern.
    """

    def survey(self) -> None:
        ...
