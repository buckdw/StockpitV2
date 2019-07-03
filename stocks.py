import yfinance as yf
import mysql.connector

REGULAR_MARKET_VOLUME = u'regularMarketVolume'
SYMBOL = u'symbol'
LONG_NAME = u'longName'
REGULAR_MARKET_OPEN = u'regularMarketOpen'
AVERAGE_DAILY_VOLUME_10DAY = u'averageDailyVolume10Day'
SHARES_OUTSTANING = u'sharesOutstanding'
MARKET_CAP = u'marketCap'

mysql_handle = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="j0sepace",
                               database="stockpit"
                               )
def retrieve(stocks):
    for stock in stocks:
        quote = yf.Ticker(stock)
        quote_dict = quote.info
        print(quote_dict[SYMBOL]
          , quote_dict[LONG_NAME]
          , quote_dict[REGULAR_MARKET_VOLUME]
          , quote_dict[AVERAGE_DAILY_VOLUME_10DAY]
          , quote_dict[REGULAR_MARKET_OPEN]
          , quote_dict[SHARES_OUTSTANING]
          , quote_dict[MARKET_CAP]

          )
    return

stocks = ["SSYS", "DDD", "AAPL", "DASTY"]
retrieve(stocks)


