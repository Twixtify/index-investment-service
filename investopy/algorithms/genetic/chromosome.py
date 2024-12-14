from dataclasses import dataclass
from typing import Optional

from gene import StockGene


@dataclass
class StockChromosome:
    stocks: list[StockGene]
    fitness: Optional[float]

    def fitness(self):
        """
        Calculate the fitness of this candidate solution.
            # Total price: P += n * s, where n is the amount and s the stock price.
            # Fitness: f(x) += x^2
        """
        self.fitness = 0
        total_price = sum([gene.amount * gene.price for gene in self.stocks])
        for gene in self.stocks:
            self.fitness += gene.score(total_price) * gene.score(total_price)
