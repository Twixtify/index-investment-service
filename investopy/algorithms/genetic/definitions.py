from typing import Protocol, TypeVar, Any, Iterable

T = TypeVar("T", bound=int | float)
S = TypeVar("S", bound=int | float | str)


class Mutation(Protocol):
    """
    Define a mutation protocol for genes.

    Mutation is the process of changing a gene of an individual by random chance.
    This process is used to maintain and introduce diversity in the population.
    """

    def mutate(self, mut_prob: float, *args) -> None:
        """
        Mutate the gene method.

        Here is a list of possible mutation strategies:
        Perturbation: Change at random some gene of the individual by perturbing its value.
        Swap: Choose two genes and swap their position.
        Scramble: Choose a random length segment and interchange genes in this segment.
        Inversion: Choose a random length segment and reverse the order of genes in it.
        """
        ...


class Population(Protocol):
    """
    General protocol of a population.
    """

    def evolve(self, *args, **kwargs) -> Any:
        """
        Evolve the population.

        This is the process of
        1. Calculate the fitness of each candidate solution.
        2. Select candidates for the next generation.
        3. Perform crossover.
        4. Mutate candidates.
        5. Evaluate termination condition.
        """
        ...

    def termination_condition(self, *args, **kwargs) -> bool:
        """
        Determine if the population should stop evolving.
        """
        ...


class Chromosome(Protocol):
    """
    Define a chromosome protocol of the population.

    Individuals or chromosomes represent the generation to evolve through the genetic algorithm process.
    Each individual represent a set of parameters or genes.
    These genes are encoded parameters. Encoding strategies are for example binary-, float- or order values.
    """

    def fitness(self) -> T:
        """
        The fitness for each chromosome represent the quality of this chromosome.
        """
        ...


class Gene(Protocol):
    """
    Define a gene protocol for chromosomes.

    Genes are encoded parameters. Encoding strategies like binary-, float- or order values are common use cases.
    For example:
    individual_binary=[0, 1, 1, 0]
    individual_float=[0.34, 4.241, 51.123, 0.4567]
    individual_order=[2, 4, 1, 7]
    """

    def encoding(self) -> S:
        """
        Return the encoded value of this gene.
        """
        ...

    def mutate(self, mutation: Mutation, *args, **kwargs) -> None:
        """
        Call a mutation function on this gene.
        """
        ...


class Selection(Protocol):
    """
    Selection is the process of selecting parents to generate the children of the next generation.
    The idea is that those individuals who are not selected will unfortunately succumb to the challenges of this generation,
    i.e. they will not survive to the next generation.
    """

    def get(self, population: Iterable[Chromosome]) -> Iterable[Chromosome]:
        """
        Retrieve surviving chromosomes using their fitness.

        Selection methods commonly used are for example:
        1) Tournament selection.
        2) Stochastic Universal Sampling (SUS).
        3) Roulette wheel.
        4) Randomly select.
        5) Select worst.
        6) Select best.
        """
        ...
