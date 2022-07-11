from .invoker import PortfolioController
from .portfolio import Portfolio


class Facade:
    controller = PortfolioController()

    def analyse(self, portfolio: Portfolio) -> None:
        self.controller.execute(portfolio)
