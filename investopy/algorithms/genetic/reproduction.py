from collections.abc import Sequence

from investopy.algorithms.genetic.definitions import Reproduction, Chromosome


class Uniform(Reproduction):
    """
    Uniform crossover
    """

    def __init__(self, co_prob: float):
        """
        :param co_prob: crossover probability
        """
        self.co_prob = co_prob

    def breed(self, parents: Sequence[Chromosome], children: int) -> Sequence[Chromosome]:
        """
        Uniform crossover. Each individual keep their length.
        Each gene has a probability co_prob of being swapped chosen.
        :param parents: pairs of parents created from the Recombination algorithm.
        :param children: number of children to return
        :return: Children from the parents
        """

    def parent_combinations(self, parents: Sequence[Chromosome]):
        # If every parent cannot be paired
        if len(parents) % 2 == 1:
            pass
