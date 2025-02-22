from dataclasses import dataclass
from itertools import zip_longest
from typing import Optional

import numpy as np
import pandas as pd
from pandas import DataFrame, to_numeric

from investopy.config import PORTFOLIO_COLUMNS, STOCK_COLUMNS
from investopy.genetic.gene import StockGene
from investopy.genetic.mutation import UniformStepMutation
from investopy.genetic.objective_function import IndexWeight
from investopy.genetic.population import StockPopulation
from investopy.genetic.recombination import RandomPairing
from investopy.genetic.reproduction import RandomPick
from investopy.genetic.selection import Sort
from investopy.genetic.termination import GenerationLimit
from .calculator import Calculator


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
class MinPortfolio(Calculator):
    deposit: Optional[float]  # Not important
    stocks_to_exclude: Optional[list[str]] = None
    data: Optional[DataFrame] = None
    _updated_weight_col = "Ny viktning (%)"  # Weight after excluding stocks
    _amount_to_buy_col = "Antal att köpa"
    _total_price_col = "Totalt pris"
    _approximate_weight = "Köpets viktning (%)"  # Algorithm weight

    def run(self):
        population = self.prepare_algorithm()
        result = population.evolve(gene_lower_limit=1, gene_upper_limit=10)
        print("Best fit genes: ", result[0].genes)
        # How much of each stock to buy
        self.data[self._amount_to_buy_col] = [gene.parameter for gene in result[0].genes]
        # Total price per stock
        self.data[self._total_price_col] = self.data[self._amount_to_buy_col] * self.data[STOCK_COLUMNS[1]]
        # Approximate weight (amount to buy * price per stock) / total price
        self.data[self._approximate_weight] = 100 * self.data[self._total_price_col] / self.data[
            self._total_price_col].sum()

        # Extract result columns
        result = self.data[[
            PORTFOLIO_COLUMNS[0],
            PORTFOLIO_COLUMNS[1],
            self._updated_weight_col,
            STOCK_COLUMNS[1],
            self._amount_to_buy_col,
            self._total_price_col,
            self._approximate_weight
        ]].copy()
        result[self._amount_to_buy_col] = result[self._amount_to_buy_col].astype(int)
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.float_format', "{:,.2f}".format):
            print(result.to_string(index=False))
        print("Total price:", result[self._total_price_col].sum())
        return result

    def prepare_algorithm(self) -> StockPopulation:
        ### Custom parameters ###
        size_survivors = 20
        ### Population parameters ###
        size = 200
        # Divide by 100 because weight is in %
        genome = [StockGene(row.iloc[0], row.iloc[2], row.iloc[1] / 100) for index, row in self.data.iterrows()]
        # Set survivor selection method
        selection = Sort(size_survivors)
        # Set parent combination technique
        recombination = RandomPairing(pairings=10, pairing_size=2)
        # Children per pair should add up to size-size_survivors
        reproduction = RandomPick(children=int(size / size_survivors))
        # Initialize mutation method
        mutation = UniformStepMutation(mut_prob=0.10, step=1, min_threshold=1)
        # Set fitness function
        objective = IndexWeight()
        # Set termination condition
        termination = GenerationLimit(generation_limit=5000)
        return StockPopulation(size, genome, selection, recombination, reproduction, mutation, objective, termination)

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
        self.data = portfolio.merge(stocks, how="left", on=to_merge[0])
        self.data = self.data.apply(to_numeric, errors='ignore')

        # Remove stocks and add their average weight to remaining stocks
        if self.stocks_to_exclude is not None:
            self._remove_stocks_to_exclude()

    def _remove_stocks_to_exclude(self):
        # Ensure excluded stocks are removed
        unified_name_tags = unify(self.data,
                                  DataFrame(self.stocks_to_exclude, columns=[PORTFOLIO_COLUMNS[0]]),
                                  PORTFOLIO_COLUMNS[0])
        self.data.replace(to_replace=dict(unified_name_tags), value=None, regex=True, inplace=True)
        excluding_stocks = self.data.loc[self.data[PORTFOLIO_COLUMNS[0]].isin(self.stocks_to_exclude)]

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print("Excluding: \n", excluding_stocks.to_string(index=False))
        excluding_arr = excluding_stocks[PORTFOLIO_COLUMNS[1]].to_numpy()
        # Average weight to add on remaining values
        to_add = np.sum(excluding_arr) / (len(self.data) - len(excluding_stocks))
        print("Average weight to add from excluded stocks: ", to_add)

        # Drop values from data
        self.data.drop(index=excluding_stocks.index, inplace=True)
        # Add average weight
        self.data[self._updated_weight_col] = self.data[PORTFOLIO_COLUMNS[1]].map(lambda x: x + to_add)
