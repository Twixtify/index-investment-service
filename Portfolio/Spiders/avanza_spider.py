import concurrent.futures
import re
import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Portfolio.config import STOCK, BUY, SELL, LATEST_PRICE


def get_driver(path_driver=r"C:\drivers\chromedriver.exe"):
    options = Options()
    options.headless = True
    return webdriver.Chrome(executable_path=path_driver, options=options)


def get_content(driver, url):
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content


def get_soup(url_source, parser='html.parser'):
    return BeautifulSoup(url_source, parser)


class AvanzaSpider(threading.Thread):
    MAX_THREADS = 30

    def __init__(self, urls, options):
        """
        :param urls: Supplied stock on Avanza.
        :param options: What options to track on Avanza
        """
        threading.Thread.__init__(self)
        self.urls = urls
        self.options = options
        self.result = []

    @classmethod
    def get_stock_name(cls, soup):
        return soup.find_all('h1')[0].text.strip()

    def get_latest_stock_value(self, soup, stock_name):
        try:
            latest_value = soup.find_all("span", attrs={"class": re.compile(r'\blatest\b')})[0].text.split()[0]
            float(latest_value.replace(',', '.'))
            return latest_value
        except (ValueError, IndexError) as e:
            print(e)
            print(self.__class__, ": No values found on %s" % stock_name)

    def crawl(self, url):
        result = {}

        driver = get_driver()
        content = get_content(driver, url)
        soup = get_soup(content)
        stock_name = self.get_stock_name(soup)
        result[STOCK] = stock_name
        for option in self.options:
            if option == BUY:
                # TODO: Implement get-highest-stock-value
                pass
            if option == SELL:
                # TODO: Implement get-lowest-stock-value
                pass
            if option == LATEST_PRICE:
                latest_price = self.get_latest_stock_value(soup, stock_name)
                result[LATEST_PRICE] = latest_price
                print("Success! Latest price {stock} : {price}".format(stock=stock_name, price=latest_price))
        return result

    def run(self):
        threads = min(self.MAX_THREADS, len(self.urls))

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for url in self.urls:
                future_obj = executor.submit(self.crawl, url)
                futures.append(future_obj)

        for future in concurrent.futures.as_completed(futures):
            crawl_result = future.result()
            self.result.append(crawl_result)


def main():
    spider = AvanzaSpider(urls=["https://www.avanza.se/aktier/om-aktien.html/5277/bure-equity",
                                "https://www.avanza.se/aktier/om-aktien.html/26268/aak"],
                          options=[LATEST_PRICE])
    spider.run()


if __name__ == "__main__":
    main()
