import os

# Useful variable names
# ---- DataFrame column names ----
ID = 'ID'
STOCK = 'Aktie'
WEIGHT = 'Viktning'
IBINDEX = "ibindex"
AMOUNT_TO_BUY = 'Antal att köpa'
TOTAL_PRICE = 'Totalt pris'
# ---- Crawl options ----
BUY = 'Köp'
SELL = 'Sälj'
LATEST_PRICE = 'Senast betalt'
TIME = 'Tid'

# Path to this 'config.py' folder
ROOT = os.path.dirname(os.path.realpath(__file__))
ENCODING = 'utf-8'
METHODS = os.path.join(ROOT, "Methods")
PORTFOLIOS = os.path.join(ROOT, "Portfolios")
SPIDERS = os.path.join(ROOT, "Spiders")
DATA = os.path.join(ROOT, "PortfolioData")
INVESTMENTBOLAG_DATA = os.path.join(DATA, "InvestmentbolagData")
FORNYBARENERGI_DATA = os.path.join(DATA, "FornybarenergiData")

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
