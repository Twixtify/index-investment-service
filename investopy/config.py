# ------ General settings ------
ENCODING = 'utf-8'
# ------ Web scraper settings ------
# Connect and read timeout define how long (in seconds) the scraper will wait for a http connection and response.
CONNECT_TIMEOUT = 3
READ_TIMEOUT = 5
# Maximum number of attempts for reconnecting to a web page.
MAX_RETRIES = 3
MAX_THREADS = 5
# ------ Web parser settings ------
HTML_PARSER = "html.parser"
PORTFOLIO_COLUMNS = ['Aktie', 'Viktning (%)']
STOCK_COLUMNS = ['Aktie', 'Köp (sek)']
