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


def initialize_sql():
    return mysql.connector.connect(host="localhost", user="root", passwd="j0sepace", database="stockpit")


def insert_stock(quote_dict, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        INSERT INTO nasdaq (
            symbol,
            long_name,
            regular_market_open,
            close,
            market_cap,
            eps,
            forward_pe
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """
    val = (quote_dict[SYMBOL]
           , quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , 0
           , quote_dict[MARKET_CAP]
           , 0
           , quote_dict[FORWARD_PE]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def upsert_stock(quote_dict, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        SELECT *
          FROM nasdaq
         WHERE symbol = %s
        """
    val = (quote_dict[SYMBOL], )
    mysql_cursor.execute(sql, val)
    record = mysql_cursor.fetchone()
    mysql_handle.commit()
    mysql_cursor.close()
    if record is None:
        insert_stock(quote_dict, mysql_handle)
        return
    update_stock(quote_dict, mysql_handle)
    return


def update_stock(quote_dict, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        UPDATE nasdaq
           SET long_name = %s,
               regular_market_open = %s,
               market_cap = %s,
               forward_pe = %s
         WHERE symbol = %s
        """
    val = (quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , quote_dict[MARKET_CAP]
           , quote_dict[FORWARD_PE]
           , quote_dict[SYMBOL])
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def retrieve_stocks(stocks, mysql_handle):
    for stock in stocks:
        quote = yf.Ticker(stock)
        quote_dict = quote.info
        upsert_stock(quote_dict, mysql_handle)
    return


stocks = ["SSYS", "DDD", "AAPL", "DASTY", "AMAT", "KLAC", "SBUX", "NXPI"]
mysql_handle = initialize_sql()
retrieve_stocks(stocks, mysql_handle)


