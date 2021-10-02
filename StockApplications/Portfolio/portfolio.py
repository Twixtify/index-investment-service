import os

from StockApplications.Portfolio.Spiders.avanza_spider import AvanzaSpider
from StockApplications.Portfolio.Spiders.manage_threads import ManageThreads
from StockApplications.Portfolio.config import ENCODING
from StockApplications.Portfolio.config import PORTFOLIOS


def read_file(filename):
    """
    Removes newlines from each row.
    :param filename: File name
    :return: List with each row as element
    """
    with open(filename, encoding=ENCODING) as f:
        lines = f.read().splitlines()
    return lines


class Portfolio:
    def __init__(self, deposit, name):
        """
        :param deposit: Amount to buy with.
        :param name: Name of portfolio file in Portfolios folder.
        """
        self.deposit = deposit
        self.name = name
        self.urls = read_file(os.path.join(PORTFOLIOS, name))
        self.thread_manager = ManageThreads()

    def calculate(self, *args):
        pass

    def gather_data(self, *args):
        pass

    def run(self, *args):
        pass

    def create_avanza_spiders(self, crawl_options):
        """
        :param crawl_options: List or single item from DEFAULT_AVANZA_OPTIONS
        :return: ManageThreads object
        """
        spiders_list = []
        for thread_id, url in enumerate(self.urls):
            spiders_list.append(AvanzaSpider(thread_id, url, crawl_options))
        return spiders_list


if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    p = Portfolio(1, "investmentbolag")
    print(vars(p))
