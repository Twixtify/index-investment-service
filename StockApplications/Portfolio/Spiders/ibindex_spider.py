import re
import threading

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from StockApplications.Portfolio.config import STOCK, IBINDEX


class IBIndexSpider(threading.Thread):
    url = 'http://ibindex.se/ibi/#/index'

    def __init__(self):
        threading.Thread.__init__(self)
        self.df = None
        self.url = IBIndexSpider.url
        self.index_soup = None
        self.driver = None

    def init_driver(self, path_driver=r"C:\drivers\chromedriver.exe"):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path=path_driver, chrome_options=options)

    def get_soup(self, url):
        self.driver.get(url)
        timeout = 0
        try:
            element_present = ec.presence_of_element_located((By.CLASS_NAME, "index-weight-inner-holder"))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException as te:
            raise te
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def get_stock_values(self):
        """
        Return values in the shape [('name', 'weight')]
        :return:
        """
        weights = []
        tags = self.index_soup.find_all("td", attrs={"class": re.compile(r"text-small\s\b(hand|right)\b")})
        for tag in tags:
            if len(tag.contents) == 1:
                weights.append(tag.text.strip())
        if not weights:
            print(self.__class__, ": No values found on %s" % self.url)
            exit(1)
        return list(zip(weights[0::2], weights[1::2]))

    def run(self):
        self.init_driver()
        self.index_soup = self.get_soup(self.url)
        self.driver.quit()
        stock_values = self.get_stock_values()
        self.df = pd.DataFrame(stock_values, columns=[STOCK, IBINDEX])
        print("Success! ibindex")


if __name__ == '__main__':
    ib = IBIndexSpider()
    ib.start()
