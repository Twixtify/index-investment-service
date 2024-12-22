import logging
import random
from collections.abc import Sequence
from copy import deepcopy

from chromosome import StockChromosome
from definitions import Population, Chromosome, Selection, Recombination, Reproduction, Mutation, Termination
from gene import StockGene
from investopy.algorithms.genetic.termination import Stagnation
from objective_function import IndexWeight


class StockPopulation(Population):

    def __init__(self, size: int,
                 genome: Sequence[StockGene],
                 selection: Selection,
                 recombination: Recombination,
                 reproduction: Reproduction,
                 mutation: Mutation,
                 objective: IndexWeight,
                 termination: Termination):
        super().__init__(selection, recombination, reproduction, mutation, objective, termination)
        self.size = size
        self.genome = genome

    def evolve(self, gene_lower_limit: int, gene_upper_limit: int) -> Sequence[Chromosome]:
        if gene_lower_limit <= 0:
            logging.error("Gene parameter cannot be 0 or less")
            return []
        population = self.get_initial_population(gene_lower_limit, gene_upper_limit)
        if isinstance(self.termination, Stagnation.__class__):
            self.termination.condition = population
        while self.termination.terminate() is False:
            survivors = self.selection.get_survivors(population)
            pairs = self.recombination.pair(survivors)
            children = self.reproduction.breed(pairs)
            for child in children:
                self.mutation.mutate(child)
            population = [*survivors, *children]
            for individual in population:
                individual.fitness = self.objective.fitness(individual)
            if isinstance(self.termination, Stagnation.__class__):
                self.termination.condition = population
        return population

    def get_initial_population(self, lower_limit: int, upper_limit: int) -> Sequence[Chromosome]:
        population = []
        for _ in range(self.size):
            genome = deepcopy(self.genome)
            for gene in genome:
                gene.parameter = random.randint(lower_limit, upper_limit)
            chromosome = StockChromosome(genes=genome)
            chromosome.fitness = self.objective.fitness(chromosome)
            population.append(chromosome)
        return population


if __name__ == "__main__":
    ib_pop = StockPopulation()
    ib_pop.selection = tuple([0])
