import logging
import random
from collections.abc import Sequence
from itertools import batched

from definitions import Recombination
from investopy.algorithms.genetic.definitions import Chromosome


class RandomPairing(Recombination):
    """
    Pick parents at random and pair them for breeding.

    The algorithm does not have knowledge of how parents will be used for crossover and
    therefore the number of pairs must be supplied to it.
    """

    def __init__(self, pairings: int, pairing_size: int):
        """
        :param pairings: Number of pairs to create
        :param pairing_size: Size of the pairs to create
        """
        self.pairings = pairings
        self.pairing_size = pairing_size

    def pair(self, parents: Sequence[Chromosome]) -> Sequence[Chromosome]:
        if len(parents) < self.pairing_size:
            logging.warning("Pairing size must be smaller or equal to the number of parents")
            return []
        for i in range(self.pairings):
            yield random.sample(parents, self.pairing_size)


class GroupByNeighbour(Recombination):
    def __init__(self, size=2):
        """
        :param size: Size of grouping pairs
        """
        self.size = size

    def pair(self, parents: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        Create non-overlapping pairs from the sequence of parents.
        If the number of parents are not divisible by self.size an empty list is returned.

        # batched('ABCDEFG', 3) → ABC DEF G

        :param parents: Parents to pair.
        :return: tuples of parents.
        """
        # Parents are not even
        if len(parents) % self.size != 0:
            logging.warning("Cannot group parents into groups of size %s evenly", self.size)
            return []
        # Return non-overlapping pairs
        for batch in batched(parents, self.size):
            yield list(batch)


if __name__ == "__main__":
    from investopy.algorithms.genetic.gene import StockGene
    from investopy.algorithms.genetic.chromosome import StockChromosome
    from investopy.algorithms.genetic.objective_function import IndexWeight

    func = IndexWeight()
    sg1 = StockGene(name="sg1", price=1, amount=1, weight=0)
    sg2 = StockGene(name="sg2", price=1, amount=1, weight=0)
    sg3 = StockGene(name="sg3", price=1, amount=1, weight=0)
    sg4 = StockGene(name="sg4", price=1, amount=1, weight=0)
    individual1 = StockChromosome(genes=[sg1])
    individual1.fitness = func.fitness(individual1)
    individual2 = StockChromosome(genes=[sg2])
    individual2.fitness = func.fitness(individual2)
    individual3 = StockChromosome(genes=[sg3])
    individual3.fitness = func.fitness(individual3)
    individual4 = StockChromosome(genes=[sg4])
    individual4.fitness = func.fitness(individual4)

    rp = RandomPairing(pairings=2, pairing_size=2)
    gn = GroupByNeighbour(1)

    result = rp.pair([individual1, individual2, individual3, individual4])
    result2 = gn.pair([individual1, individual2, individual3, individual4])

    [print("Random: ", c) for c in result]
    [print("Neighbour: ", c) for c in result2]
