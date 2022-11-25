from typing import Callable

from calculators.approx_portfolio import ApproxPortfolio
from .commands import IBIndex
from .portfolio import Portfolio
from .portfolio_receiver import IBIndexOperation

PortfolioSurveyStrategy = Callable[[float], Portfolio]


def ibindex_strategy(deposit: float) -> Portfolio:
    calculator = ApproxPortfolio(deposit,
                                 stocks_to_exclude=['Havsfrun Investment B',
                                                    'NAXS',
                                                    'Traction B',
                                                    'Öresund',
                                                    'Karolinska Development B',
                                                    'VEF']
                                 )
    receiver = IBIndexOperation(calculator)
    return IBIndex(deposit, receiver)
