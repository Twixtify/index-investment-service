from StockApplications.Portfolio.Methods.calculate import Calculate
from StockApplications.Portfolio.Methods.csv_file import CSVFile
from StockApplications.Portfolio.Spiders.ibindex_spider import IBIndexSpider
from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.config import INDEX_VALUES
from StockApplications.Portfolio.portfolio import Portfolio


class IBIndex(Portfolio):
    ibindex = "ibindex"

    def __init__(self, deposit, portfolio_name):
        super().__init__(deposit, portfolio_name)
        self.data_file = super().create_csv(self.data_file_name, self.data_folder)
        self.data_file.write_row(DATA_TO_SAVE)
        self.index_file = super().create_csv(self.index_file_name, self.index_folder)

    def calculate(self, using_index, price_data, index_data, stocks_to_exclude=None):
        excluding = None
        calculator = Calculate(price_data, index_data)
        if stocks_to_exclude is not None:
            excluding = self.index_file.get_items_row_index(stocks_to_exclude)
            _, rows_to_exclude = self.index_file.read_and_exclude_rows(stocks_to_exclude)
            for i in sorted(excluding, reverse=True):
                del index_data[i]
            for row in rows_to_exclude:
                print("Excluding: ", row)
        if using_index.lower() == IBIndex.ibindex:
            results = calculator.calculate_ibindex_distribution(self.deposit, excluding)
            total_price, amount_to_buy, prices_to_buy, index_weights = [*results]
            return total_price, amount_to_buy, prices_to_buy, index_weights, index_data

    def gather_data(self, using_index):
        self.manage_threads.add_threads(super().create_avanza_spiders(self.urls, DATA_TO_SAVE, self.data_file))
        if using_index.lower() == IBIndex.ibindex:
            self.manage_threads.add_thread(self.create_ibindex_spider(self.index_file))
        self.manage_threads.start_threads()
        self.manage_threads.join_threads()

    def sort_data(self):
        super().sort_data_by_column(self.data_file, DATA_TO_SAVE.index('Stock'), header_in_file=True)
        super().sort_data_by_column(self.index_file, INDEX_VALUES.index('Stock'), header_in_file=False)

    def get_price_and_index(self):
        price_data = super().get_numeric_data(self.data_file, DATA_TO_SAVE.index('Senast'), header_in_file=True)
        index_data = super().get_numeric_data(self.index_file, INDEX_VALUES.index('Weight'), header_in_file=False)
        return price_data, index_data

    def run(self, using_index, stocks_to_exclude):
        self.gather_data(using_index)
        self.sort_data()
        price_data, index_data = self.get_price_and_index()
        total_price, n_stocks, price_stocks, index_weights, index_data = self.calculate(using_index,
                                                                                        price_data,
                                                                                        index_data,
                                                                                        stocks_to_exclude)
        stock_names = self.data_file.read_csv_column(DATA_TO_SAVE.index('Stock'), header_in_file=True)
        result = zip(["name", *stock_names],
                     ["ibindex", *index_data],
                     ["weights", *index_weights],
                     ["price each", *price_data],
                     ["total", *price_stocks],
                     ["number", *n_stocks])
        result_file = CSVFile('result.csv', self.data_file.folder_path)
        result_file.write_rows(result)
        result_file.pprint_self()
        print("Total price:", total_price, "Difference:", self.deposit - total_price)

    @classmethod
    def create_ibindex_spider(cls, csv_file):
        return IBIndexSpider(csv_file)


if __name__ == "__main__":
    p = IBIndex(deposit=7500, portfolio_name='investmentbolag')
    p.run(using_index="IBIndex", stocks_to_exclude=['hav', 'NAXS'])
