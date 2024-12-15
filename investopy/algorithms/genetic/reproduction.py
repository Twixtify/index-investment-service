from typing import Iterable

from investopy.algorithms.genetic.definitions import Reproduction, Chromosome


class Uniform(Reproduction):
    """
    Uniform crossover
    """
    def breed(self, parents: Iterable[Chromosome], *args) -> Iterable[Chromosome]:
        pass
