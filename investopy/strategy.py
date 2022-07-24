from typing import Callable

from calculators.min_portfolio_investment import MinPortfolioInvestment
from .commands import IBIndex
from .portfolio import Portfolio
from .portfolio_receiver import IBIndexOperation

PortfolioSurveyStrategy = Callable[[float], Portfolio]


def ibindex_strategy(deposit: float) -> Portfolio:
    calculator = MinPortfolioInvestment()
    receiver = IBIndexOperation(calculator)
    return IBIndex(deposit, receiver)
