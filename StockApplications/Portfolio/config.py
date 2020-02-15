import os

# Path to this 'config.py' folder
PATH = os.path.dirname(os.path.realpath(__file__))
ENCODING = 'utf-8'
DIR_PATH = {
    'base': PATH,
    'methods': PATH + "\\" + "Methods",
    'portfolios': PATH + "\\" + "Portfolios",
    'spiders': PATH + "\\" + "Spiders",
    'data': {
        'base': PATH + "\\" + "PortfolioData",
        'investmentbolag': PATH + "\\" + "PortfolioData" + "\\" + "InvestmentbolagData",
        'fornybarenergi': PATH + "\\" + "PortfolioData" + "\\" + "FornybarenergiData"
    }
}
FILE_PATH = {
    'csv': {
        'investmentbolag': DIR_PATH['data']['investmentbolag'] + "\\" + "data.csv",
        'investmentbolagindex': DIR_PATH['data']['investmentbolag'] + "\\" + "index.csv",
        'fornybarenergi': DIR_PATH['data']['fornybarenergi'] + "\\" + "data.csv",
        'fornybarenergiindex': DIR_PATH['portfolios'] + "\\" + "fornybarenergiindex.csv"
    },
    'urls': {
        'investmentbolag': DIR_PATH['portfolios'] + "\\" + "investmentbolag",
        'fornybarenergi': DIR_PATH['portfolios'] + "\\" + "fornybarenergi"
    }
}
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
DEFAULT_AVANZA_OPTIONS = ['Köp', 'Sälj', 'Senast', 'Tid']
DATA_TO_SAVE = ['ID', 'Stock', DEFAULT_AVANZA_OPTIONS[2]]
INDEX_VALUES = ['Stock', 'Weight']
