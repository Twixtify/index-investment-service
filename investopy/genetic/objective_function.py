from investopy.genetic.chromosome import StockChromosome
from investopy.genetic.definitions import ObjectiveFunction, T


class IndexWeight(ObjectiveFunction):
    """
    Calculate the fitness of an individual to the targeted index.

        # Total price: P += n * s, where n is the amount and s the stock price.
        # Fitness: f(x) += x^2, x is the encoding of each stock.
    """

    def __init__(self, inverse_fitness=True):
        """
        Inverse the fitness score for the chromosome,
        i.e. the closer it is to the weight the higher its fitness is.
        """
        self.inverse_fitness = inverse_fitness

    def fitness(self, chromosome: StockChromosome) -> T:
        """
        Get the fitness of this candidate solution.
        """
        # The total price of this chromosome with stocks
        total_price = sum([gene.parameter * gene.price for gene in chromosome.genes])
        # sum of x_i*x_i were x_i = stock amount * stock price / total price - stock weight
        score = sum([gene.encoding(total_price) * gene.encoding(total_price) for gene in chromosome.genes])
        # Toggle for fitness score
        return 1. / score if self.inverse_fitness is True else score
