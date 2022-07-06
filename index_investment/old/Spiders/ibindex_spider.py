import re
import threading

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from index_investment.old.config import STOCK, IBINDEX


def get_driver(path_driver=r"C:\drivers\chromedriver.exe"):
    options = Options()
    options.headless = True
    return webdriver.Chrome(executable_path=path_driver, options=options)


def get_content(driver, url):
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content


def get_soup(url_content, parser='html.parser'):
    return BeautifulSoup(url_content, parser)


class IBIndexSpider(threading.Thread):
    url = 'http://ibindex.se/ibi/#/index'

    def __init__(self):
        threading.Thread.__init__(self)
        self.result = None
        self.url = IBIndexSpider.url

    def crawl(self):
        driver = get_driver()
        content = get_content(driver, self.url)
        soup = get_soup(content)
        index_values = self.get_index_weights(soup)
        return pd.DataFrame(index_values, columns=[STOCK, IBINDEX])

    def get_index_weights(self, soup):
        """
        Return values in the shape [('name', 'weight')]
        :return:
        """
        weights = []
        tags = soup.find_all("td", attrs={"class": re.compile(r"text-small\s\b(hand|right)\b")})
        for tag in tags:
            if len(tag.contents) == 1:
                weights.append(tag.text.strip())
        if not weights:
            print(self.__class__, ": No values found on %s" % self.url)
            exit(1)
        return list(zip(weights[0::2], weights[1::2]))

    def run(self):
        self.result = self.crawl()
        print("Success! ibindex")


def main():
    ib = IBIndexSpider()
    print(ib.crawl())


if __name__ == '__main__':
    main()
