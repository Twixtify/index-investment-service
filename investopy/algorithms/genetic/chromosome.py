from collections.abc import Sequence
from dataclasses import dataclass

from gene import StockGene
from investopy.algorithms.genetic.definitions import Chromosome, T


@dataclass
class StockChromosome(Chromosome):
    genes: Sequence[StockGene]
    _fitness: T = None

    @property
    def fitness(self) -> T:
        return self._fitness

    @fitness.setter
    def fitness(self, fitness: T):
        self._fitness = fitness
