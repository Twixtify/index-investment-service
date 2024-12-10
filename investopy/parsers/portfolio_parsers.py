import ast

from pandas import DataFrame

from investopy.config import PORTFOLIO_COLUMNS
from .base_parser import BaseParser


class IBIndex(BaseParser):
    def parse_content(self, html: str) -> DataFrame:
        products = ast.literal_eval(html)
        df_rows = []
        for product in products:
            stock = product['productName']
            weight = product['weight']
            df_rows.append({PORTFOLIO_COLUMNS[0]: stock, PORTFOLIO_COLUMNS[1]: weight})
        return DataFrame(df_rows, columns=PORTFOLIO_COLUMNS)
