"""
An index is a set portfolio.
"""
from investopy.facade import Facade
from investopy.strategy import ibindex_strategy

PORTFOLIO_STRATEGIES = {
    "ibindex": ibindex_strategy
}


def main(portfolio: str, deposit: float) -> None:
    selected_portfolio = PORTFOLIO_STRATEGIES[portfolio](deposit)
    facade = Facade()
    facade.analyse(selected_portfolio)
    return


if __name__ == "__main__":
    from scrapers.single_page_scraper import SinglePageScraper
    from data import target

    s = SinglePageScraper(target['url'], target['headers'])
    s.run()
    print(s.response())
    main("ibindex", 1000.0)
