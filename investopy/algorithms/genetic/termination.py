import logging
import time
from collections.abc import Sequence
from dataclasses import dataclass

from definitions import Chromosome, Termination, T


@dataclass
class Stagnation(Termination):
    """
    Termination condition based on average fitness between generations.
    If the

    Args:
        previous_average_fitness (T): Previous generations average fitness.
        stagnation_threshold (float): Threshold for classifying the average fitness as stagnated.
        stagnation_limit (int): Maximum number of consecutive stagnated generations.
    """
    stagnation_threshold: float
    stagnation_limit: int
    stagnation_count: int = 0
    previous_average_fitness: T = None

    def terminate(self, population: Sequence[Chromosome]) -> bool:
        """Stagnation based termination control"""
        total_population_fitness = sum([chromosome.fitness for chromosome in population])
        # Average population fitness
        average_fitness = total_population_fitness / len(population)
        # Check if first generation
        if self.previous_average_fitness is None:
            self.previous_average_fitness = average_fitness
            return False
        # Check if stagnation has occurred
        if abs(average_fitness - self.previous_average_fitness) < self.stagnation_threshold:
            self.stagnation_count += 1
            if self.stagnation_count >= self.stagnation_limit:
                logging.info("Stagnation reached. Final average fitness is %s", average_fitness)
                return True
        else:
            self.stagnation_count = 0
        # Update fitness
        self.previous_average_fitness = average_fitness
        return False


@dataclass
class GenerationLimit(Termination):
    """
    Stoppage based on maximum number of generations.
    """
    generation_limit: int
    _call_count: int = 0

    def terminate(self) -> bool:
        self._call_count += 1
        return True if self._call_count >= self.generation_limit else False


@dataclass
class TimeLimit(Termination):
    time_limit: int
    start_time: float = None

    def terminate(self) -> bool:
        # Initialize timer
        if self.start_time is None:
            # perf_counter() counts the time between consecutive calls with high precision
            self.start_time = time.perf_counter()
            return False
        # Check condition
        if time.perf_counter() - self.start_time > self.time_limit:
            logging.info("Time limit reached")
            return True
        return False
