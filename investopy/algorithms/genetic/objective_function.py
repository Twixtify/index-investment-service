from investopy.algorithms.genetic.chromosome import StockChromosome
from investopy.algorithms.genetic.definitions import ObjectiveFunction, T


class IndexWeight(ObjectiveFunction):
    """
    Calculate the fitness of an individual to the targeted index.

        # Total price: P += n * s, where n is the amount and s the stock price.
        # Fitness: f(x) += x^2, x is the encoding of each stock.
    """

    def fitness(self, chromosome: StockChromosome) -> T:
        """
        Get the fitness of this candidate solution.
        """
        # The total price of this chromosome with stocks
        total_price = sum([gene.parameter * gene.price for gene in chromosome.genes])
        # sum of x_i*x_i were x_i = stock amount * stock price / total price - stock weight
        return sum([gene.encoding(total_price) * gene.encoding(total_price) for gene in chromosome.genes])
