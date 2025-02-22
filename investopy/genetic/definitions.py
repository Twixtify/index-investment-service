from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, Any

T = TypeVar("T", bound=int | float)
S = TypeVar("S", bound=int | float | str)


class Gene(ABC):
    """
    Define a gene for a chromosome.

    Genes are encoded parameters. Encoding strategies like binary-, float- or order values are common use cases.
    For example:
    encoded_individual_binary=[0, 1, 1, 0]
    encoded_individual_float=[0.34, 4.241, 51.123, 0.4567]
    encoded_individual_order=[2, 4, 1, 7]
    """

    @property
    @abstractmethod
    def parameter(self):
        """The parameter the genetic algorithm is fitting to."""
        raise NotImplementedError()

    @parameter.setter
    @abstractmethod
    def parameter(self, parameter: S) -> None:
        """Setter for the parameter"""
        raise NotImplementedError()

    @abstractmethod
    def encoding(self, *args) -> S:
        """
        Return the encoded value of this gene.
        """
        raise NotImplementedError()


class Chromosome(ABC):
    """
    Define a chromosome protocol of the population.

    Individuals or chromosomes represent the generation to evolve through the genetic algorithm process.
    Each individual represent a set of parameters or genes.
    These genes are encoded parameters. Encoding strategies are for example binary-, float- or order values.
    The fitness for each chromosome represent the quality of this chromosome.
    """
    genes: Sequence[Gene]

    @property
    @abstractmethod
    def fitness(self) -> T:
        raise NotImplementedError()

    @fitness.setter
    def fitness(self, fitness: T) -> None:
        """
        Update fitness of this chromosome.

        The fitness is determined in relation to an objective function which is specific for a population.
        The population defines the problem we want to solve.
        Therefore, the fitness is determined by the Population and not the individual chromosome.
        """
        raise NotImplementedError()


class Selection(ABC):
    """
    Selection is the process of selecting parents to generate the children of the next generation.
    The idea is that those individuals who are not selected will unfortunately succumb to the challenges of this generation,
    i.e. they will not survive to the next generation.
    """

    @abstractmethod
    def get_survivors(self, population: Sequence[Chromosome]) -> Sequence[Chromosome]:
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
        raise NotImplementedError()


class Recombination(ABC):

    @abstractmethod
    def pair(self, parents: Sequence[Chromosome]) -> Sequence[Sequence[Chromosome]]:
        """
        Pair parents from a selection step to be passed on to the reproduction step.
        """
        raise NotImplementedError()


class Reproduction(ABC):
    """
    Define the protocol for generating children (crossover).

    Crossover is the process of creating children from individuals.
    There exists many types of crossover methods. Below some of them have been listed.

    1) Uniform crossover is the process of swapping genes between two individuals to produce two children.
    2) One point crossover is the process of picking a point in each individuals genome and swapping the
    tail after this point between them.
    """

    @abstractmethod
    def breed(self, parents: Sequence[Chromosome]) -> Sequence[Chromosome]:
        """
        Parents breed, also known as the chromosomes undergo crossover, to produce new individuals (children).
        """
        raise NotImplementedError()


class Mutation(ABC):
    """
    Define a mutation protocol.

    Mutation is the process of changing a gene of an individual by random chance.
    This process is used to maintain and introduce diversity in the population.
    """

    @abstractmethod
    def mutate(self, chromosome: Chromosome) -> None:
        """
        Call upon this method to potentially mutate individuals in the population.

        Here is a list of possible mutation strategies:
        1) Perturbation: Change at random some gene of the individual by perturbing its value.
        2) Swap: Choose two genes and swap their position.
        3) Scramble: Choose a random length segment and interchange genes in this segment.
        4) Inversion: Choose a random length segment and reverse the order of genes in it.
        """
        raise NotImplementedError()


class ObjectiveFunction(ABC):

    @abstractmethod
    def fitness(self, chromosome: Chromosome) -> T:
        """
        Calculate the fitness of a candidate solution or chromosome.
        """
        raise NotImplementedError()


class Termination(ABC):
    """
    Define the termination protocol of the population.
    """

    @abstractmethod
    def terminate(self) -> bool:
        """
        Determine if the population should stop evolving.

        Some stopping conditions could be:
        1) Maximum number of generations reached.
        2) Timelimit.
        3) A fitness limit reached.
        4) Population stagnation, the average fitness of the population does not change between generations in
        comparison to some predefined metric.
        5) Time stagnation, the average fitness of the population does not change within a certain amount of time.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def condition(self) -> Any:
        """Optional condition to evaluate in the terminate method."""
        raise NotImplementedError()

    @condition.setter
    def condition(self, arg: Any) -> None:
        raise NotImplementedError()


class Population(ABC):
    """
    General protocol of a population.

    Returns the fittest individual after the termination condition is met.
    """
    selection: Selection
    recombination: Recombination
    reproduction: Reproduction
    mutation: Mutation
    objective: ObjectiveFunction
    termination: Termination

    @abstractmethod
    def __init__(self, selection: Selection,
                 recombination: Recombination,
                 reproduction: Reproduction,
                 mutation: Mutation,
                 objective: ObjectiveFunction,
                 termination: Termination):
        """
        Initialize
        #    selection
        #    recombination
        #    reproduction
        #    mutation
        #    objective
        #    termination
        for this population
        """
        self.selection = selection
        self.recombination = recombination
        self.reproduction = reproduction
        self.mutation = mutation
        self.objective = objective
        self.termination = termination

    @abstractmethod
    def evolve(self) -> Sequence[Chromosome]:
        """
        Main method of the Genetic Algorithm.

        This is the process of
        1. Calculate the fitness of each candidate solution.
        2. Select candidates for the next generation.
        3. Perform crossover.
        4. Mutate candidates.
        5. Evaluate termination condition.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_initial_population(self) -> Sequence[Chromosome]:
        """Create the initial population"""
        raise NotImplementedError()
