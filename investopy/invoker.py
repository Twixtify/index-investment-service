from .portfolio import Portfolio


class PortfolioController:
    """
    Command pattern invoker.
    Has knowledge of how to execute a portfolio (command).
    """

    def execute(self, portfolio: Portfolio) -> None:
        portfolio.survey()
