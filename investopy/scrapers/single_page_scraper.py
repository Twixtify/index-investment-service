import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from investopy.config import CONNECT_TIMEOUT, READ_TIMEOUT, MAX_RETRIES
from .base_scraper import BaseScraper


class SinglePageScraper(BaseScraper):
    """
    Scrape a single page with a GET request and return the content.
    """

    def __init__(self, url: str, headers: dict) -> None:
        self.url = url
        self.headers = headers
        self._response = None
        self._session = requests.Session()
        self._session.options(url=self.url, headers=self.headers, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        self._session.mount(self.url, HTTPAdapter(max_retries=MAX_RETRIES))

    @property
    def response(self) -> str:
        """Return response in 'ENCODING' format"""
        return self._response.text

    def run(self) -> None:
        try:
            self._response = self._session.get(self.url)
            self._response.raise_for_status()
        except ConnectionError as ce:
            self._session.close()
            raise ce
