import os

# Useful variable names
ID = 'ID'
STOCK = 'Stock'
WEIGHT = 'Weight'
BUY = 'Köp'
SELL = 'Sälj'
LATEST_PRICE = 'Senast betalt'
TIME = 'Tid'
IBINDEX = "ibindex"

# Path to this 'config.py' folder
ROOT = os.path.dirname(os.path.realpath(__file__))
ENCODING = 'utf-8'
METHODS = os.path.join(ROOT, "Methods")
PORTFOLIOS = os.path.join(ROOT, "Portfolios")
SPIDERS = os.path.join(ROOT, "Spiders")
DATA = os.path.join(ROOT, "PortfolioData")
INVESTMENTBOLAG_DATA = os.path.join(DATA, "InvestmentbolagData")
FORNYBARENERGI_DATA = os.path.join(DATA, "FornybarenergiData")

# FILE_PATH = {
#    'csv': {
#        'investmentbolag': DIR_PATH['data']['investmentbolag'] + "\\" + "data.csv",
#        'investmentbolagindex': DIR_PATH['data']['investmentbolag'] + "\\" + "index.csv",
#        'fornybarenergi': DIR_PATH['data']['fornybarenergi'] + "\\" + "data.csv",
#        'fornybarenergiindex': DIR_PATH['portfolios'] + "\\" + "fornybarenergiindex.csv"
#    },
#    'urls': {
#        'investmentbolag': DIR_PATH['portfolios'] + "\\" + "investmentbolag",
#        'fornybarenergi': DIR_PATH['portfolios'] + "\\" + "fornybarenergi"
#    }
# }
# dictionary with opening and closing times
MARKET = {
    'OPEN':
        {
            'hour': 9,
            'min': 0,
            'sec': 0
        },
    'CLOSE':
        {
            'hour': 17,
            'min': 30,
            'sec': 0
        }
}

if __name__ == "__main__":
    print(ROOT)
