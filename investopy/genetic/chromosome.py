from collections.abc import Sequence
from dataclasses import dataclass

from investopy.genetic.definitions import Chromosome, T
from .gene import StockGene


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
