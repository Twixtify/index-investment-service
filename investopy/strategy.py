from typing import Callable

from .portfolio import Portfolio
from .commands import IBIndex
from .portfolio_receiver import IBIndexOperation

PortfolioSurveyStrategy = Callable[[float], Portfolio]


def ibindex_strategy(deposit: float) -> Portfolio:
    receiver = IBIndexOperation()
    return IBIndex(deposit, receiver)
