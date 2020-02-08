import os
import threading

import requests
from bs4 import BeautifulSoup


class AvanzaSpider(threading.Thread):
    def __init__(self, _id, url, options, file):
        """
        Constructor of StockSpider
        :param url: Supplied stock on Avanza.
        :param options: What options to track on Avanza
        """
        threading.Thread.__init__(self)
        self.id = _id
        self.url = url
        self.options = options
        self.stock_soup = None
        self.stock_name = None
        if not os.path.isfile(file.file_path):
            print("No such file: " + file.file_name)
            exit(1)
        else:
            self.file = file

    @staticmethod
    def get_soup(url):
        html = requests.get(url, allow_redirects=False)
        return BeautifulSoup(html.text, 'html.parser')

    def get_stock_values(self):
        values = []
        tags = self.stock_soup.find_all("li", attrs={"class": "tLeft"})
        for option in self.options:
            for tag in tags:
                subtag = tag.find_all("span", recursive=False)
                if option in subtag[0].text:
                    values.append(subtag[1].text)
        if not len(values) >= 1:
            print(self.__class__, ": No values found on %s" % self.url)
        return values

    def init_spider(self):
        self.stock_soup = self.get_soup(self.url)
        self.stock_name = self.stock_soup.find_all('title')[0].text.split(" - ")[0]

    def run(self):
        self.init_spider()
        stock_values_list = self.get_stock_values()
        self.file.append_row([self.id, self.stock_name, *stock_values_list])
