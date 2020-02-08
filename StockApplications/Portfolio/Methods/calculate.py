import numpy as np


class Calculate:
    def __init__(self, price_data, index_data):
        self.price_data = np.array(price_data)
        self.index_weights = np.array(index_data)

    @staticmethod
    def percent_to_fraction(weights, norm):
        norm_weights = np.divide(weights, norm)
        return norm_weights

    def calculate_ibindex_distribution(self, deposit, weights_to_exclude=None):
        if weights_to_exclude:
            excluded_weights = np.take(self.index_weights, weights_to_exclude)
            self.index_weights = np.delete(self.index_weights, weights_to_exclude)
            self.index_weights += np.sum(excluded_weights)/self.index_weights.size

        self.index_weights = self.percent_to_fraction(self.index_weights, 100)
        prices_to_buy = np.multiply(self.index_weights, deposit)
        amount_to_buy = np.rint(np.divide(prices_to_buy, self.price_data))
        total_price = np.sum(amount_to_buy * self.price_data)
        prices_to_buy = np.round(prices_to_buy, decimals=2)
        self.index_weights = np.round(np.multiply(self.index_weights, 100), decimals=2)
        return total_price, amount_to_buy.tolist(), prices_to_buy.tolist(), self.index_weights
