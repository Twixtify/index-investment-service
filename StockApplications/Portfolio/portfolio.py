from StockApplications.Portfolio.Methods.calculate import Calculate
from StockApplications.Portfolio.Methods.csv_file import CSVFile
from StockApplications.Portfolio.Methods.data_folder import DataFolder
from StockApplications.Portfolio.Methods.text_file import TextFile
from StockApplications.Portfolio.Methods.text_parser import TextParser

from StockApplications.Portfolio.Spiders.avanza_spider import AvanzaSpider
from StockApplications.Portfolio.Spiders.ibindex_spider import IBIndexSpider
from StockApplications.Portfolio.Spiders.manage_threads import ManageThreads

from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.config import DIR_PATH
from StockApplications.Portfolio.config import FILE_PATH
from StockApplications.Portfolio.config import INDEX_VALUES


class Portfolio:
    ibindex = "ibindex"

    def __init__(self, deposit, portfolio_name, stock_data_file_name, data_csv_folder_path, index_file_name,
                 index_file_folder_path):
        self.deposit = deposit
        self.portfolio_name = portfolio_name
        self.urls = TextFile(self.portfolio_name, DIR_PATH['portfolios']).read_rows()
        DataFolder(self.portfolio_name.title() + "Data").create_folder()
        self.data_file = CSVFile(stock_data_file_name, data_csv_folder_path)
        self.data_file.write_row(DATA_TO_SAVE)
        self.index_file = CSVFile(index_file_name, index_file_folder_path)
        self.manage_threads = ManageThreads()

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
        if using_index.lower() == Portfolio.ibindex:
            results = calculator.calculate_ibindex_distribution(self.deposit, excluding)
            total_price, amount_to_buy, prices_to_buy, index_weights = [*results]
            return total_price, amount_to_buy, prices_to_buy, index_weights, index_data

    def gather_data(self, using_index):
        self.manage_threads.add_threads(self.create_avanza_spiders(self.urls, DATA_TO_SAVE, self.data_file))
        if using_index.lower() == Portfolio.ibindex:
            self.manage_threads.add_thread(self.create_ibindex_spider(self.index_file))
        self.manage_threads.start_threads()
        self.manage_threads.join_threads()

    def sort_data(self):
        self.sort_data_by_column(self.data_file, DATA_TO_SAVE.index('Stock'), header_in_file=True)
        self.sort_data_by_column(self.index_file, INDEX_VALUES.index('Stock'), header_in_file=False)

    def get_price_and_index(self):
        price_data = self.get_numeric_data(self.data_file, DATA_TO_SAVE.index('Senast'), header_in_file=True)
        index_data = self.get_numeric_data(self.index_file, INDEX_VALUES.index('Weight'), header_in_file=False)
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
        print("Total price:", total_price, "Difference:", self.deposit-total_price)

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

    @classmethod
    def create_avanza_spiders(cls, urls, crawl_options, csv_file):
        spiders_list = []
        for thread_id, url in enumerate(urls):
            spiders_list.append(AvanzaSpider(thread_id, url, crawl_options, csv_file))
        return spiders_list

    @classmethod
    def create_ibindex_spider(cls, csv_file):
        return IBIndexSpider(csv_file)


if __name__ == "__main__":
    import os
    portfolios_file = 'investmentbolag'
    p = Portfolio(deposit=7500,
                  portfolio_name=portfolios_file,
                  stock_data_file_name=os.path.basename(FILE_PATH['csv'][portfolios_file]),
                  data_csv_folder_path=DIR_PATH['data'][portfolios_file],
                  index_file_name=os.path.basename(FILE_PATH['csv'][portfolios_file+'sindex']),
                  index_file_folder_path=DIR_PATH['data'][portfolios_file])
    p.run(using_index="IBIndex", stocks_to_exclude=['hav', 'NAXS'])
