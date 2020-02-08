import codecs
import csv
import re

from StockApplications.Portfolio.config import ENCODING
from StockApplications.Portfolio.Methods.text_parser import TextParser


###########################################

def get_file_rows(path_file):
    rows = []
    with codecs.open(path_file, 'r', encoding=ENCODING) as file:
        for row in file:
            rows.append(row.strip())
    return rows


###########################################


def parse_numeric(string):
    regex = r'[^\d.]+'
    parser = re.compile(regex)
    return parser.sub('', string)


###########################################


# def sort_csv_file(file, id_col):
#     with codecs.open(file, 'r', encoding=ENCODING) as f_unsorted:
#         data = csv.reader(f_unsorted, delimiter=',')
#         header = next(data, None)
#         sorted_data = sorted(data, key=lambda row: int(row[id_col]))
#     with codecs.open(file, 'w', encoding=ENCODING) as f_sorted:
#         writer = csv.writer(f_sorted)
#         writer.writerow(header)
#         for sorted_row in sorted_data:
#             writer.writerow(sorted_row)


###########################################


def calculate_stock_deposits(deposit, csv_file, index_file):
    weights = get_file_rows(index_file)
    for w_i, weight in enumerate(weights):
        weights[w_i] = TextParser.parse_numeric(weight)
    weights = list(map(float, weights))
    rm_weight = weights.pop(3)
    new_weights = [(weight + (rm_weight/len(weights)))/100 for weight in weights]
    stock_prices, prices_to_buy, amount_to_buy = [], [], []
    with codecs.open(csv_file, 'r', encoding=ENCODING) as file:
        reader = csv.reader(file)
        next(reader, None)
        for index, row in enumerate(reader):
            stock_price = float(row[2].replace(",", "."))
            price_to_buy = deposit * new_weights[index]
            stock_prices.append(stock_price)
            prices_to_buy.append(price_to_buy)
            amount_to_buy.append(int(round(price_to_buy/stock_price)))
            print(row[1], "\t", price_to_buy, "\t", amount_to_buy[index])
    total_price = 0
    for i, number in enumerate(amount_to_buy):
        total_price += number*stock_prices[i]
    print("Total price:", total_price, "Difference: ", deposit-total_price)


###########################################


def lst_to_str(lst):
    return "\t".join(lst).replace(",", ".")


###########################################


if __name__ == '__main__':
    from StockApplications.Portfolio.config import FILE_PATH
    print(get_file_rows(FILE_PATH['urls']['investmentbolag']))
