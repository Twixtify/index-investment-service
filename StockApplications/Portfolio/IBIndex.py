import pandas as pd

from StockApplications.Portfolio.Spiders.ibindex_spider import IBIndexSpider
from StockApplications.Portfolio.config import ID, STOCK, LATEST_PRICE, IBINDEX
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
    return str(f * 100) + '%'


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
        self.result = pd.DataFrame(columns=[ID, STOCK, LATEST_PRICE])

    def calculate(self, index_data, stocks_to_exclude):
        """
        :param index_data: Pandas DataFrame('Stock', 'Weight')
        :param stocks_to_exclude: List of stocks from ibindex to exclude.
        :return:
        """
        self.result[LATEST_PRICE] = self.result[LATEST_PRICE].map(string_to_float)
        index_data[IBINDEX] = index_data[IBINDEX].map(percent_to_float)
        excluding_stocks = index_data.loc[index_data[STOCK].isin(stocks_to_exclude)]
        print(excluding_stocks)
        print(self.result)
        # self
        # calculator = Calculate(self.deposit, index_data)
        # if stocks_to_exclude is not None:
        #     excluding = self.index_file.get_items_row_index(stocks_to_exclude)
        #     _, rows_to_exclude = self.index_file.read_and_exclude_rows(stocks_to_exclude)
        #     for i in sorted(excluding, reverse=True):
        #         del index_data[i]
        #     for row in rows_to_exclude:
        #         print("Excluding: ", row)
        # if using_index.lower() == IBIndex.portfolio:
        #     results = calculator.calculate_ibindex_distribution(self.deposit, excluding)
        #     total_price, amount_to_buy, prices_to_buy, index_weights = [*results]
        #     return total_price, amount_to_buy, prices_to_buy, index_weights, index_data

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
        # price_data, index_data = self.get_price_and_index()
        # total_price, n_stocks, price_stocks, index_weights, index_data = self.calculate(using_index,
        #                                                                                 price_data,
        #                                                                                 index_data,
        #                                                                                 stocks_to_exclude)
        # stock_names = self.data_file.read_csv_column(DATA_TO_SAVE.index('Stock'), header_in_file=True)
        # result = zip(["name", *stock_names],
        #              ["ibindex", *index_data],
        #              ["weights", *index_weights],
        #              ["price each", *price_data],
        #              ["total", *price_stocks],
        #              ["number", *n_stocks])
        # result_file = CSVFile('result.csv', self.data_file.folder_path)
        # result_file.write_rows(result)
        # result_file.pprint_self()
        # print("Total price:", total_price, "Difference:", self.deposit - total_price)


if __name__ == "__main__":
    p = IBIndex(deposit=10000)
    p.run(stocks_to_exclude=['Havsfrun Investment B',
                             'NAXS',
                             'Traction  B',
                             'Öresund',
                             'Karolinska Development B',
                             'Fastator'])
