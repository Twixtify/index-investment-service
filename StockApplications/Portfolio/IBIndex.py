import pandas as pd

from StockApplications.Portfolio.Methods.calculate import Calculate
from StockApplications.Portfolio.Methods.csv_file import CSVFile
from StockApplications.Portfolio.Spiders.ibindex_spider import IBIndexSpider
from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.config import INDEX_VALUES
from StockApplications.Portfolio.portfolio import Portfolio


class IBIndex(Portfolio):
    """
    TODO: Create own "Investmentbolagsindex".
    """
    portfolio = "investmentbolag"

    def __init__(self, deposit):
        super().__init__(deposit, IBIndex.portfolio)
        self.thread_manager.add_thread(IBIndexSpider())
        spiders = self.create_avanza_spiders(crawl_options=DATA_TO_SAVE[2])
        self.thread_manager.add_threads(spiders)
        self.result = pd.DataFrame(columns=DATA_TO_SAVE)

    def calculate(self, using_index, price_data, index_data, stocks_to_exclude=None):
        """
        TODO: Remove 'using_index' in this method.
        :param using_index: String
        :param price_data: Price per stock
        :param index_data: Weights of the index
        :param stocks_to_exclude: List of stocks from ibindex to exclude.
        :return:
        """
        excluding = None
        calculator = Calculate(price_data, index_data)
        if stocks_to_exclude is not None:
            excluding = self.index_file.get_items_row_index(stocks_to_exclude)
            _, rows_to_exclude = self.index_file.read_and_exclude_rows(stocks_to_exclude)
            for i in sorted(excluding, reverse=True):
                del index_data[i]
            for row in rows_to_exclude:
                print("Excluding: ", row)
        if using_index.lower() == IBIndex.portfolio:
            results = calculator.calculate_ibindex_distribution(self.deposit, excluding)
            total_price, amount_to_buy, prices_to_buy, index_weights = [*results]
            return total_price, amount_to_buy, prices_to_buy, index_weights, index_data

    def gather_data(self):
        self.thread_manager.start_threads()
        self.thread_manager.join_threads()

    def sort_data(self):
        # TODO: sort stocks by name
        super().sort_data_by_column(self.data_file, DATA_TO_SAVE.index('Stock'), header_in_file=True)
        super().sort_data_by_column(self.index_file, INDEX_VALUES.index('Stock'), header_in_file=False)

    def get_price_and_index(self):
        price_data = super().get_numeric_data(self.data_file, DATA_TO_SAVE.index('Senast betalt'), header_in_file=True)
        index_data = super().get_numeric_data(self.index_file, INDEX_VALUES.index('Weight'), header_in_file=False)
        return price_data, index_data

    def run(self, stocks_to_exclude):
        self.gather_data()
        # self.sort_data()
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
    print(vars(p))
    p.run(stocks_to_exclude=['Havsfrun Investment B',
                             'NAXS',
                             'Traction  B',
                             'Öresund',
                             'Karolinska Development B',
                             'Fastator'])
