import os

from StockApplications.Portfolio.Methods.calculate import Calculate
from StockApplications.Portfolio.config import DATA_TO_SAVE, INDEX_VALUES, FILE_PATH, DIR_PATH
from StockApplications.Portfolio.portfolio import Portfolio


class Fornybarenergi(Portfolio):
    def __init__(self, deposit, portfolio_name):
        super().__init__(deposit, portfolio_name)
        self.data_file = super().create_csv(self.data_file_name, self.data_folder)
        self.data_file.write_row(DATA_TO_SAVE)
        self.index_file_name = os.path.basename(FILE_PATH['csv'][self.portfolio_name + 'index'])
        self.index_folder = DIR_PATH['portfolios']
        self.index_file = super().create_csv(self.index_file_name, self.index_folder)

    def gather_data(self):
        self.manage_threads.add_threads(super().create_avanza_spiders(self.urls, DATA_TO_SAVE, self.data_file))
        self.manage_threads.start_threads()
        self.manage_threads.join_threads()

    def sort_data(self):
        super().sort_data_by_column(self.data_file, DATA_TO_SAVE.index('Stock'), header_in_file=True)
        super().sort_data_by_column(self.index_file, INDEX_VALUES.index('Stock'), header_in_file=False)

    def get_price_and_index(self):
        price_data = super().get_numeric_data(self.data_file, DATA_TO_SAVE.index('Senast betalt'), header_in_file=True)
        index_data = super().get_numeric_data(self.index_file, INDEX_VALUES.index('Weight'), header_in_file=False)
        return price_data, index_data

    def calculate(self, price_data, index_data):
        results = Calculate(price_data, index_data).calculate_fornybarenergi_distribution(self.deposit)
        total_price, amount_to_buy, prices_to_buy, index_weights = [*results]
        return total_price, amount_to_buy, prices_to_buy, index_weights, index_data

    def run(self):
        self.gather_data()
        self.sort_data()
        price_data, index_data = self.get_price_and_index()
        total_price, n_stocks, price_stocks, index_weights, index_data = self.calculate(price_data, index_data)
        stock_names = self.data_file.read_csv_column(DATA_TO_SAVE.index('Stock'), header_in_file=True)
        result = zip(["name", *stock_names],
                     ["ibindex", *index_data],
                     ["weights", *index_weights],
                     ["price each", *price_data],
                     ["total", *price_stocks],
                     ["number", *n_stocks])
        result_file = super().create_csv('result.csv', self.data_file.folder_path)
        result_file.write_rows(result)
        result_file.pprint_self()
        print("Total price:", total_price, "Difference:", self.deposit - total_price)


if __name__ == "__main__":
    p = Fornybarenergi(deposit=900, portfolio_name='fornybarenergi')
    p.run()
