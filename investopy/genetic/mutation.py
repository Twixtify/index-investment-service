import logging
import random
from dataclasses import dataclass

from .definitions import Mutation, Chromosome


@dataclass
class UniformStepMutation(Mutation):
    mut_prob: float
    step: int
    min_threshold: int = None
    max_threshold: int = None

    def mutate(self, chromosome: Chromosome) -> None:
        """
        Mutate an integer by picking a random integer in an interval [-step, step] around the gene parameter value.
        """
        if not all(isinstance(gene.parameter, int) for gene in chromosome.genes):
            logging.warning("Cannot perform uniform step mutation on non-integer genes.")
            return None
        for i, gene in enumerate(chromosome.genes):
            if random.random() <= self.mut_prob:
                gene.parameter += random.randint(-self.step, self.step)
                # Set gene parameter to threshold if it exists
                if self.min_threshold is not None and gene.parameter < self.min_threshold:
                    gene.parameter = self.min_threshold
                elif self.max_threshold is not None and gene.parameter > self.max_threshold:
                    gene.parameter = self.max_threshold


@dataclass
class Scramble(Mutation):
    """
    Scramble.

    The process of selecting a subset of genes and scramble their parameters.
    The picked genes does not have to be contiguous i.e. adjacent to each other.

    Args:
        mut_prob (float): mutation probability
        scramble_size (int): number of genes in the genome to shuffle
    """
    mut_prob: float
    scramble_size: int

    def mutate(self, chromosome: Chromosome) -> None:
        """Mutate the chromosome"""
        # Check if mutation should occur
        if random.random() > self.mut_prob:
            return None
        # Make sure scramble size does not exceed genome
        scramble_size = min(len(chromosome.genes), self.scramble_size)
        # Randomly select indices to scramble
        indices = random.sample(range(len(chromosome.genes)), scramble_size)
        # Extract gene parameters corresponding to indices
        parameters_to_scramble = [chromosome.genes[i].parameter for i in indices]
        # Shuffle the parameters
        random.shuffle(parameters_to_scramble)
        # Insert shuffled parameters at indices position
        for i, index in enumerate(indices):
            chromosome.genes[index].parameter = parameters_to_scramble[i]


if __name__ == "__main__":
    from investopy.genetic.gene import StockGene
    from investopy.genetic.chromosome import StockChromosome
    from investopy.genetic.objective_function import IndexWeight

    func = IndexWeight()
    sg1 = StockGene(name="sg1", price=1, amount=1, weight=0)
    sg2 = StockGene(name="sg2", price=1, amount=2, weight=0)
    sg3 = StockGene(name="sg3", price=1, amount=3, weight=0)
    sg4 = StockGene(name="sg4", price=1, amount=4, weight=0)
    individual1 = StockChromosome(genes=[sg1, sg2, sg3, sg4])
    individual1.fitness = func.fitness(individual1)

    uformstep = UniformStepMutation(0.5, min_threshold=0)
    scramble = Scramble(1, 2)

    # uformstep.mutate(individual1, 10)
    scramble.mutate(individual1, 7)

    print(individual1.genes)
