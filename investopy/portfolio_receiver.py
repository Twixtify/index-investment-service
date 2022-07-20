import concurrent.futures
from dataclasses import dataclass

from config import MAX_THREADS
from data import ibindex, privataffarer
from scrapers.single_page_scraper import SinglePageScraper
from parsers.portfolio_parsers import IBIndex
from parsers.stock_parsers import PrivataAffarer


@dataclass
class IBIndexOperation:
    """A receiver to carry out a specific portfolio operation"""
    _portfolio_scraper = SinglePageScraper(ibindex['url'], ibindex['headers'])
    _stock_scraper = SinglePageScraper(privataffarer['url'], privataffarer['headers'])
    _portfolio_parser = IBIndex()
    _stock_parser = PrivataAffarer()

    def action(self):
        web_scrapers = [self._portfolio_scraper, self._stock_scraper]
        threads = min(MAX_THREADS, len(web_scrapers))

        # Tasks initialized
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for scraper in web_scrapers:
                executor.submit(scraper.run)
        # Tasks completed
        portfolio_data = self._portfolio_parser.parse_content(self._portfolio_scraper.response)
        stock_data = self._stock_parser.parse_content(self._stock_scraper.response)

        print(portfolio_data)
        print(stock_data)
