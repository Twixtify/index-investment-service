from StockApplications.Portfolio.Methods.csv_file import CSVFile
from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.portfolio import Portfolio


class Fornybarenergi(Portfolio):
    def __init__(self, deposit, portfolio_name):
        super().__init__(deposit, portfolio_name)
        self.data_file = CSVFile(stock_data_file_name, data_csv_folder_path)
        self.data_file.write_row(DATA_TO_SAVE)
        self.index_file = CSVFile(index_file_name, index_file_folder_path)