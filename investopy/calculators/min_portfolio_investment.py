from dataclasses import dataclass
from itertools import zip_longest
from typing import Optional

from pandas import DataFrame, to_numeric
import numpy as np

from .calculator import Calculator
from investopy.config import PORTFOLIO_COLUMNS


def is_match(s1: str, s2: str) -> bool:
    """Check if either string is a substring of the other"""
    char_tuples = zip(list(s1), list(s2))
    for i, j in list(char_tuples):
        if i != j:
            return False
    return True


def is_words_match(words1: list[str], words2: list[str]) -> bool:
    """Check if sequence of words is a match"""
    for w1, w2 in list(zip_longest(words1, words2)):
        if not is_match(w1, w2):
            return False
    return True


def unify(df1: DataFrame, df2: DataFrame, on_col: str, by_left=True) -> list:
    """
    Unify row string values between two DataFrames on a common column.
    @param df1: DataFrame.
    @param df2: DataFrame.
    @param on_col: On column, the column name to unify both DataFrames.
    @param by_left: Use df1 to replace values in df2.
    """
    if by_left:
        val1 = df1[on_col].to_numpy()
        val2 = df2[on_col].to_numpy()
    else:
        val1 = df2[on_col].to_numpy()
        val2 = df1[on_col].to_numpy()
    to_update = []
    for val_i in val1:
        words1 = val_i.split()
        for val_j in val2:
            words2 = val_j.split()
            # Add if it's a match and the values has not already been added.
            if is_words_match(words1, words2) and val_i not in dict(to_update).values():
                tmp = (val_j, val_i)
                if tmp[0] != tmp[1]:
                    to_update.append(tmp)
    return to_update


@dataclass
class MinPortfolioInvestment(Calculator):
    data: Optional[DataFrame] = None

    def prepare_data(self, stocks: DataFrame, portfolio: DataFrame) -> None:
        # Remove NaN
        stocks.dropna()
        portfolio.dropna()
        # Replace comma with dot
        stocks = stocks.apply(lambda x: x.astype(str).str.replace(',', '.'))
        portfolio = portfolio.apply(lambda x: x.astype(str).str.replace(',', '.'))
        # Strip strings
        stocks = stocks.apply(lambda x: x.str.strip())
        portfolio = portfolio.apply(lambda x: x.str.strip())

        # Find common columns
        stocks_col = stocks.columns
        portfolio_col = portfolio.columns
        intersecting_col = stocks_col.intersection(portfolio_col)
        to_merge = intersecting_col.to_list()

        print(f"Performing merge on {to_merge}")
        unified_column = unify(portfolio, stocks, to_merge[0])
        stocks.replace(to_replace=dict(unified_column), value=None, regex=True, inplace=True)

        # Save result to data variable
        self.data = portfolio.merge(stocks, how="left", on=to_merge)
        self.data = self.data.apply(to_numeric, errors='ignore')

    def run(self) -> DataFrame:
        w = self.data[PORTFOLIO_COLUMNS[1]].to_numpy().flatten() / 100
        s = self.data["Köp"].to_numpy().flatten()
        P = np.divide(s, w)
        Pk = np.amax(P)
        return self.data
