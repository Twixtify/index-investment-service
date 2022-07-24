import concurrent.futures
from dataclasses import dataclass

from calculators.calculator import Calculator
from config import MAX_THREADS
from data import ibindex, privataffarer
from parsers.portfolio_parsers import IBIndex
from parsers.stock_parsers import PrivataAffarer
from scrapers.single_page_scraper import SinglePageScraper


@dataclass
class IBIndexOperation:
    """A receiver to carry out a specific portfolio operation"""
    _portfolio_scraper = SinglePageScraper(ibindex['url'], ibindex['headers'])
    _stock_scraper = SinglePageScraper(privataffarer['url'], privataffarer['headers'])
    _portfolio_parser = IBIndex()
    _stock_parser = PrivataAffarer()
    calculator: Calculator

    def action(self):
        # ---- Retrieve data ----
        web_scrapers = [self._portfolio_scraper, self._stock_scraper]
        threads = min(MAX_THREADS, len(web_scrapers))

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for scraper in web_scrapers:
                executor.submit(scraper.run)
        # ---- Parse data ----
        portfolio_data = self._portfolio_parser.parse_content(self._portfolio_scraper.response)
        stock_data = self._stock_parser.parse_content(self._stock_scraper.response)

        # ---- Calculate data ----
        # TODO: Add calculator for portfolio deposit
        self.calculator.prepare_data(stock_data, portfolio_data)
        self.calculator.run()
