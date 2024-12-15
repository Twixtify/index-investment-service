from dataclasses import dataclass

from definitions import Gene


@dataclass
class StockGene(Gene):
    name: str
    price: float
    weight: float
    amount: int

    def encoding(self, total_price_solution: float) -> float:
        if total_price_solution != 0:
            return self.amount * self.price / total_price_solution - self.weight
        else:
            raise ValueError("The total price cannot be 0!")
