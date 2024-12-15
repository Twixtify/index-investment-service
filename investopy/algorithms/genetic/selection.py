from typing import Iterable

from investopy.algorithms.genetic.definitions import Selection, Chromosome


class SUS(Selection):
    """
    Stochastic Universal Sampling
    """

    def get_survivors(self, population: Iterable[Chromosome]) -> Iterable[Chromosome]:
        pass
