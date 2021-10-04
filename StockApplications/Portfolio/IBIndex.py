import pandas as pd

import numpy as np

from StockApplications.Portfolio.Spiders.ibindex_spider import IBIndexSpider
from StockApplications.Portfolio.config import ID, STOCK, LATEST_PRICE, IBINDEX, WEIGHT, TOTAL_PRICE, AMOUNT_TO_BUY
from StockApplications.Portfolio.portfolio import Portfolio


def string_to_float(s):
    """
    Convert a price to float
    :param s: String
    :return: float
    """
    return float(s.replace(',', '.'))


def percent_to_float(s):
    """
    Convert to float like: '10%' -> 0.1
    :param s: String with '%' sign in it.
    :return: A float
    """
    return float(s.strip('%').replace(',', '.')) / 100


def float_to_percent(f):
    """
    Convert to string like: '0.1' -> 10%
    :param f: Float.
    :return: String
    """
    return str(np.round(f * 100, decimals=2)) + '%'


class IBIndex(Portfolio):
    """
    TODO: Create own "Investmentbolagsindex".
    """
    portfolio = "investmentbolag"

    def __init__(self, deposit):
        super().__init__(deposit, IBIndex.portfolio)
        self.thread_manager.add_thread(IBIndexSpider())
        spiders = self.create_avanza_spiders(crawl_options=[ID, STOCK, LATEST_PRICE])
        self.thread_manager.add_threads(spiders)
        self.result = pd.DataFrame(columns=[STOCK, LATEST_PRICE])

    def calculate(self, index_data, stocks_to_exclude):
        """
        :param index_data: Pandas DataFrame('Stock', 'Weight')
        :param stocks_to_exclude: List of stocks from ibindex to exclude.
        :return:
        """
        self.result[LATEST_PRICE] = self.result[LATEST_PRICE].map(string_to_float)
        excluding_stocks = index_data.loc[index_data[STOCK].isin(stocks_to_exclude)]
        print("Excluding: \n", excluding_stocks)
        excluding_arr = excluding_stocks[IBINDEX].map(percent_to_float).to_numpy()
        to_add = np.sum(excluding_arr) / len(self.result.index)
        print("Average weight to add from excluded stocks: ", float_to_percent(to_add))
        self.result[WEIGHT] = self.result[IBINDEX].map(lambda x: percent_to_float(x) + to_add)
        self.result[AMOUNT_TO_BUY] = self.deposit * self.result[WEIGHT] / self.result[LATEST_PRICE]
        self.result[AMOUNT_TO_BUY] = self.result[AMOUNT_TO_BUY].map(lambda x: np.rint(x))
        self.result[TOTAL_PRICE] = self.result[AMOUNT_TO_BUY] * self.result[LATEST_PRICE]

    def gather_data(self):
        self.thread_manager.start_threads()
        self.thread_manager.join_threads()

    def extract_and_sort(self):
        """
        Extract data from spiders and add to respective dataframe.
        Sort DataFrame by stock name.
        :return:
        """
        index_df = pd.DataFrame()
        for spider in self.thread_manager.threads:
            if not isinstance(spider, IBIndexSpider):
                self.result = self.result.append(spider.stock_values_list, ignore_index=True)
            else:
                index_df = index_df.append(spider.df)
        self.result = self.result.sort_values(by=STOCK)
        return index_df.sort_values(by=STOCK)

    def run(self, stocks_to_exclude):
        self.gather_data()
        index_data = self.extract_and_sort()
        self.result = self.result.merge(index_data, on=STOCK)
        self.calculate(index_data, stocks_to_exclude)
        self.result[WEIGHT] = self.result[WEIGHT].map(float_to_percent)


if __name__ == "__main__":
    p = IBIndex(deposit=10000)
    p.run(stocks_to_exclude=['Havsfrun Investment B',
                             'NAXS',
                             'Traction  B',
                             'Öresund',
                             'Karolinska Development B',
                             'Fastator'])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(p.result.to_string(index=False))
    print("Total price:", p.result[TOTAL_PRICE].sum(), "Difference:", p.deposit - p.result[TOTAL_PRICE].sum())
