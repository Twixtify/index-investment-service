from typing import Callable

from .portfolio import Portfolio
from .commands import IBIndex

PortfolioSurveyStrategy = Callable[[float], Portfolio]


def ibindex_strategy(deposit: float) -> Portfolio:
    return IBIndex(deposit)
