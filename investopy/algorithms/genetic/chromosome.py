from dataclasses import dataclass
from typing import Optional, Iterable

from gene import StockGene
from investopy.algorithms.genetic.definitions import Chromosome


@dataclass
class StockChromosome(Chromosome):
    genes: Iterable[StockGene]
    fitness: Optional[float] = None
