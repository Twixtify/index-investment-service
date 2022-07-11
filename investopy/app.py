"""
An index is a set portfolio.
"""
from investopy.facade import Facade
from investopy.strategy import ibindex_strategy

PORTFOLIO_STRATEGIES = {
    "ibindex": ibindex_strategy
}


def main(portfolio: str, deposit: float) -> None:
    _portfolio = PORTFOLIO_STRATEGIES[portfolio](deposit)
    facade = Facade()
    facade.analyse(_portfolio)
    return


if __name__ == "__main__":
    main("ibindex", 1000.0)
