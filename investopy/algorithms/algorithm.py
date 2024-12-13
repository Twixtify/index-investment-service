from typing import Protocol


class Algorithm(Protocol):
    """
    Protocol for heuristic algorithms.
    Any heuristic algorithm created must have a search method.
    """

    def search(self):
        ...
