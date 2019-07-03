import yfinance as yf
import mysql.connector

REGULAR_MARKET_VOLUME = u'regularMarketVolume'
SYMBOL = u'symbol'
LONG_NAME = u'longName'
REGULAR_MARKET_OPEN = u'regularMarketOpen'
AVERAGE_DAILY_VOLUME_10DAY = u'averageDailyVolume10Day'
SHARES_OUTSTANING = u'sharesOutstanding'
MARKET_CAP = u'marketCap'
FORWARD_PE = u'forwardPE'

mysql_handle = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="j0sepace",
                               database="stockpit"
                               )
def update_stock(quote_dict, mysql_handle):
    print(quote_dict[SYMBOL]
          , quote_dict[LONG_NAME]
          , quote_dict[REGULAR_MARKET_VOLUME]
          )
    mysql_cursor = mysql_handle.cursor()
    sql = "UPDATE nasdaq SET long_name = %s, regular_market_open = %s, market_cap = %s, forward_pe = %s WHERE symbol = %s"
    val = (quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , quote_dict[MARKET_CAP]
           , quote_dict[FORWARD_PE]
           , quote_dict[SYMBOL]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    return

def retrieve_stocks(stocks, mysql_handle):
    for stock in stocks:
        quote = yf.Ticker(stock)
        quote_dict = quote.info
        update_stock(quote_dict, mysql_handle)
    return

stocks = ["SSYS", "DDD", "AAPL", "DASTY"]
retrieve_stocks(stocks, mysql_handle)


