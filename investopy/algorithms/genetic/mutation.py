import random
from abc import ABC
from dataclasses import dataclass


class Mutation(ABC):
    """
    Define a mutation protocol for genes.
    """
    mut_prob: float

    def mutate(self, **kwargs) -> None:
        ...


@dataclass
class MutateRange(Mutation):
    mut_prob: float

    def mutate(self, amount: int, sample_range: int) -> None:
        if random.random() <= self.mut_prob:
            amount = amount + random.randint(-sample_range, sample_range)
