import logging
import random
from collections.abc import Sequence
from copy import deepcopy

from definitions import Reproduction, Chromosome


class RandomPick(Reproduction):
    """
    Random Pick crossover.

    Perform crossover by selecting each gene randomly from the parents.

    parent1 = [1, 0, 1, 1]
    parent2 = [0, 0, 1, 0]

    child1 = [1, 0, 1, 0]

    Each gene from parent1 and parent2 is chosen at an equal 50/50 chance. Here the child1 is a composition of
    child1=[parent_gene_1, parent_gene_2, parent_gene_1, parent_gene_2]. Note that each gene in the child has been chosen
    randomly from the parents. If more than
    """

    def __init__(self, children: int):
        self.children = children

    def breed(self, parents: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        Breed using a random pick crossover reproduction.

        Parents are unmodified. Every gene has the same probability of being chosen for the child.
        Note: The genome of the children have the same size as the shortest genome of the parents.

        If the number of children=2 then:
        [parent1, parent2, parent3, ...] → [child1, child2], where for example, parent1 = [1, 4, 2, 1],
        parent2 = [0, 1, 1, 0], etc. Now the algorithm picks one random parent, let's say parent1.

        Each gene is picked randomly for the parents. See below.
        child1 = [parent_gene2, parent_gene3, parent_gene1, parent_gene2, ...]

        :param parents: parents that will create children.
        :param children: number of children to
        :return: Children from the parents
        """
        tmp_children = []
        for _ in range(self.children):
            # Retrieve a child which is a deepcopy of the shortest genome of the parents
            child = deepcopy(min(*parents, key=lambda chromosome: len(chromosome.genes)))
            # Child does not yet have a fitness.
            # The fitness should be calculated at a later time.
            child.fitness = None
            for i in range(len(child.genes)):
                # Pick a random gene from one of the parents
                # This is the gene to append on the child
                parent = parents[random.randint(0, len(parents) - 1)]
                # Reference to gene
                gene_to_copy = parent.genes[i]
                # Update child gene
                child.genes[i] = deepcopy(gene_to_copy)
            tmp_children.append(child)
        return tmp_children


class Uniform(Reproduction):
    """
    Uniform Crossover.
    # parent1 = [1, 1, 1, 1]
    # parent2 = [0, 0, 1, 0]

    # child1 = [1, 0, 1, 0]
    # child2 = [0, 1, 1, 1]
    child1 genes are chosen with a probability and child2 genome is the opposite pick to child1 genome.
    Note gene at parent1[2]=parent2[2] hence both children have gene value 1 at this position.
    """

    def __init__(self, co_prob=0.5):
        """
        :param co_prob: crossover probability for parent1 compared to parent2.
        """
        self.co_prob = co_prob

    def breed(self, parents: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        Create two children which are the crossover of each parent.

        :param parents: two parents
        :return: two children
        """
        if len(parents) != 2 or len(parents[0].genes) != len(parents[1].genes):
            logging.warning("There can only be two parents of equal length genome.")
            return []
        child1, child2 = deepcopy(parents[0]), deepcopy(parents[1])
        child1.fitness, child2.fitness = None, None
        for i in range(len(child1.genes)):
            if random.random() <= self.co_prob:
                child1.genes[i] = deepcopy(parents[0].genes[i])
                child2.genes[i] = deepcopy(parents[1].genes[i])
            else:
                child1.genes[i] = deepcopy(parents[1].genes[i])
                child2.genes[i] = deepcopy(parents[0].genes[i])
        return [child1, child2]


if __name__ == "__main__":
    from investopy.algorithms.genetic.gene import StockGene
    from investopy.algorithms.genetic.chromosome import StockChromosome
    from investopy.algorithms.genetic.objective_function import IndexWeight

    func = IndexWeight()
    sg1 = StockGene(name="1", price=1, amount=1, weight=0)
    sg2 = StockGene(name="2", price=1, amount=2, weight=0)
    sg3 = StockGene(name="3", price=1, amount=3, weight=0)
    sg4 = StockGene(name="4", price=1, amount=4, weight=0)
    individual1 = StockChromosome(genes=[sg1, sg2])
    individual2 = StockChromosome(genes=[sg1, sg1, sg1, sg1])
    individual3 = StockChromosome(genes=[sg3, sg4])
    individual4 = StockChromosome(genes=[sg2, sg2, sg2, sg2])
    individual1.fitness = func.fitness(individual1)
    individual2.fitness = func.fitness(individual2)
    individual3.fitness = func.fitness(individual3)
    individual4.fitness = func.fitness(individual4)

    randpick = RandomPick(2)
    uniform = Uniform()

    offspring = randpick.breed([individual1, individual2, individual3, individual4])
    offspring2 = uniform.breed([individual2, individual4])

    [print("Random Pick genome: ", child.genes) for child in offspring]
    [print("Uniform genome: ", child.genes) for child in offspring2]
