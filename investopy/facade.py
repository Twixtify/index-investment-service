from .invoker import PortfolioController
from .portfolio import Portfolio


class Facade:
    def __int__(self):
        self.controller = PortfolioController()

    def analyse(self, portfolio: Portfolio) -> None:
        self.controller.execute(portfolio)
