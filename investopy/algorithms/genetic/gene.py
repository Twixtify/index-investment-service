from dataclasses import dataclass

from definitions import Mutation


@dataclass
class StockGene:
    name: str
    price: float
    weight: float
    amount: int
    mutation: Mutation  # Define a mutation process for this gene

    def score(self, total_price_solution: float) -> float:
        if total_price_solution != 0:
            return self.amount * self.price / total_price_solution - self.weight

    def mutate(self):
        self.mutation.mutate()

    def set_amount(self, amount: int) -> None:
        self.amount = amount
