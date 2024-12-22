import logging
import random
from collections.abc import Sequence

from .definitions import Selection, Chromosome


class SUS(Selection):
    """
    Stochastic Universal Sampling (SUS).

    This method has no bias and minimal spread.
    The idea is to map evenly spaced points to fitness values which have been sorted in descending order.
    The number of points is equal to the number of individuals to be selected.
    The larger fitness values will have more pointers inside them. As a consequence, individuals with higher fitness
    will be selected more frequently.

    "https://en.wikipedia.org/wiki/Stochastic_universal_sampling"
    """

    def __init__(self, size: int):
        """
        :param size: number of survivors
        """
        self.size = size

    def get_survivors(self, population: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        :param population: List of fitness values for the population
        :return: the 'size' number of survivors
        """
        # Create list of (index, fitness) pairs
        idx_fitness = [tuple([idx, chromosome.fitness]) for idx, chromosome in enumerate(population)]
        # Sort the list in place by descending order according to the highest fitness
        idx_fitness.sort(key=lambda tup: tup[1], reverse=False)
        # Total fitness
        total_fitness = sum([tup[1] for tup in idx_fitness])
        # Normalize fitness (i.e. map fitness values to the interval [0, 1])
        idx_fitness[:] = [tuple([tup[0], tup[1] / total_fitness]) for tup in idx_fitness]
        # Distance between the pointers to create
        distance = 1 / self.size
        # Initial pointer start
        start = random.uniform(0, distance)
        # Pointers
        pointers = [start + i * distance for i in range(self.size)]

        # Perform selection
        survivors = []
        for pointer in pointers:
            i = 0
            tmp_sum = idx_fitness[i][1]
            while tmp_sum < pointer:
                i += 1
                tmp_sum += idx_fitness[i][1]
            # Append indices of survivors
            survivors.append(idx_fitness[i][0])
        return [population[survivor] for survivor in survivors]


class Sort(Selection):
    def __init__(self, size: int, descending=True):
        """
        :param size: How many sorted individuals to retrieve from population
        :param descending: Boolean for sorting individuals by descending fitness value
        """
        self.size = size
        self.descending = descending

    def get_survivors(self, population: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        Return a subsequence of the population in descending [from highest to lowest] or ascending [lowest to highest]
        order based on the individuals respective fitness value.

        :param population: the population of individuals
        :return: A slice of the population sorted by fitness in descending or ascending order
        """
        if self.size > len(population):
            logging.warning("Cannot create a sorted sequence longer than the population")
            return []
        return sorted(population, key=lambda chromosome: chromosome.fitness, reverse=self.descending)[:self.size]


if __name__ == "__main__":
    from investopy.genetic.gene import StockGene
    from investopy.genetic.chromosome import StockChromosome
    from investopy.genetic.objective_function import IndexWeight

    func = IndexWeight()
    sg1 = StockGene(name="sg1", price=1, amount=1, weight=0.0)
    sg2 = StockGene(name="sg2", price=1, amount=1, weight=0.0)
    sg3 = StockGene(name="sg3", price=1, amount=1, weight=0.0)
    sg4 = StockGene(name="sg4", price=1, amount=1, weight=0.0)
    individual1 = StockChromosome(genes=[sg1])
    individual1.fitness = func.fitness(individual1)
    individual2 = StockChromosome(genes=[sg2])
    individual2.fitness = func.fitness(individual2)
    individual3 = StockChromosome(genes=[sg3])
    individual3.fitness = func.fitness(individual3)
    individual4 = StockChromosome(genes=[sg4])
    individual4.fitness = func.fitness(individual4)
    sus = SUS(2)
    sort = Sort(2)
    result = sus.get_survivors([individual1, individual2, individual3, individual4])
    result2 = sort.get_survivors([individual1, individual2, individual3, individual4])
    [print("SUS: ", c) for c in result]
    [print("Sort: ", c) for c in result2]
#     list1 = [1,0,2,3,0,0,0]
#     result = [tuple([index, val]) for index, val in enumerate(list1)]
#     idx, val = *result
#     print(*result)
