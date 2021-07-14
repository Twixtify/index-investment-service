import os

import pandas as pd

from StockApplications.Portfolio.Methods.text_parser import TextParser
from StockApplications.Portfolio.Spiders.avanza_spider import AvanzaSpider
from StockApplications.Portfolio.Spiders.manage_threads import ManageThreads
from StockApplications.Portfolio.config import ENCODING
from StockApplications.Portfolio.config import PORTFOLIOS
from StockApplications.Portfolio.config import DATA_TO_SAVE


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
    def __init__(self, deposit, portfolio_name):
        self.deposit = deposit
        self.portfolio_name = portfolio_name
        self.urls = read_file(os.path.join(PORTFOLIOS, portfolio_name))
        self.result = pd.DataFrame(columns=DATA_TO_SAVE)

    def calculate(self, *args):
        pass

    def gather_data(self, *args):
        pass

    def run(self, *args):
        pass

    @classmethod
    def sort_data_by_column(cls, csv_file, col_index, header_in_file):
        sorted_data = csv_file.sort_csv_file(col_index, header_in_file)
        csv_file.write_rows(sorted_data)

    @classmethod
    def get_numeric_data(cls, csv_file, col_index, header_in_file):
        column_list = csv_file.read_csv_column(col_index, header_in_file)
        return cls.parse_comma_and_numeric(column_list)

    @classmethod
    def parse_comma_and_numeric(cls, string_list):
        text_parser = TextParser(string_list)
        text_parser.update(text_parser.replace_char_texts(",", "."))
        text_parser.update(text_parser.parse_numeric_texts())
        return list(map(float, text_parser.texts))

    def create_avanza_spiders(self, crawl_options):
        """
        :param crawl_options: List or single item from DEFAULT_AVANZA_OPTIONS
        :return: ManageThreads object
        """
        spiders_list = []
        for thread_id, url in enumerate(self.urls):
            spiders_list.append(AvanzaSpider(thread_id, url, crawl_options))
        return ManageThreads().add_threads(spiders_list)


if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    p = Portfolio(1, "investmentbolag")
    print(vars(p))
