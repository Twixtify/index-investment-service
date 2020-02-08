from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.config import DIR_PATH
from StockApplications.Portfolio.config import FILE_PATH
from StockApplications.Portfolio.config import INDEX_VALUES

from StockApplications.Portfolio.Methods.data_folder import DataFolder
from StockApplications.Portfolio.Methods.text_file import TextFile


class Portfolio:
    def __init__(self, deposit, portfolio_name):
        self.deposit = deposit
        self.portfolio_name = portfolio_name
        self.urls = TextFile(self.portfolio_name, DIR_PATH['portfolios']).read_rows()
        DataFolder(self.portfolio_name.title() + "Data").create_folder()

    def run(self, *args):
        pass
