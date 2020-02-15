import os

from StockApplications.Portfolio.Methods.csv_file import CSVFile
from StockApplications.Portfolio.Spiders.avanza_spider import AvanzaSpider
from StockApplications.Portfolio.Spiders.manage_threads import ManageThreads
from StockApplications.Portfolio.config import DATA_TO_SAVE
from StockApplications.Portfolio.config import DIR_PATH
from StockApplications.Portfolio.config import FILE_PATH
from StockApplications.Portfolio.config import INDEX_VALUES

from StockApplications.Portfolio.Methods.data_folder import DataFolder
from StockApplications.Portfolio.Methods.text_file import TextFile
from StockApplications.Portfolio.Methods.text_parser import TextParser


class Portfolio:
    def __init__(self, deposit, portfolio_name):
        self.deposit = deposit
        self.portfolio_name = portfolio_name
        self.urls = TextFile(self.portfolio_name, DIR_PATH['portfolios']).read_rows()
        self.data_file_name = os.path.basename(FILE_PATH['csv'][self.portfolio_name])
        self.data_folder = DIR_PATH['data'][self.portfolio_name]
        self.index_file_name = os.path.basename(FILE_PATH['csv'][self.portfolio_name + 'index'])
        self.index_folder = DIR_PATH['data'][self.portfolio_name]
        DataFolder(self.portfolio_name.title() + "Data").create_folder()
        self.manage_threads = ManageThreads()

    def calculate(self, *args):
        pass

    def gather_data(self, using_index):
        pass

    def run(self, *args):
        pass

    @classmethod
    def create_csv(cls, name, folder):
        return CSVFile(name, folder)

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
