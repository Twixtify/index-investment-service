import random
from dataclasses import dataclass


@dataclass
class MutateRange:
    mut_prob: float

    def mutate(self, amount: int, sample_range: int):
        if random.random() <= self.mut_prob:
            amount += random.randint(-sample_range, sample_range)
