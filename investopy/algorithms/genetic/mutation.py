import random
from dataclasses import dataclass

from investopy.algorithms.genetic.definitions import Mutation


@dataclass
class UniformStepMutation(Mutation):
    mut_prob: float

    def mutate(self, value: int, step: int) -> None:
        """
        Mutate an integer by picking a random integer in an interval [-step, step] inclusively around the value.
        """
        if random.random() <= self.mut_prob:
            value += random.randint(-step, step)
