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
REGULAR_MARKET_PRICE = u'regularMarketPrice'
FIFTY_TWO_WEEK_LOW = u'fiftyTwoWeekLow'
FIFTY_DAY_AVERAGE = u'fiftyDayAverage'
AVERAGE_DAILY_VOLUME_10DAY = u'averageDailyVolume10Day'


def initialize_sql():
    return mysql.connector.connect(host="localhost", user="root", passwd="j0sepace", database="stockpit")


def drop_table(table):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        DROP TABLE IF EXISTS %s
        """
    val = (table, )
    mysql_cursor.execute(sql, val)
    mysql_cursor.close()
    return


def initialize_table(table):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        CREATE TABLE %s (
        `symbol` varchar(8) NOT NULL DEFAULT '',
        `long_name` varchar(255) NOT NULL DEFAULT '',
        `regular_market_open` float NOT NULL DEFAULT '0',
        `close` float NOT NULL DEFAULT '0',
        `market_cap` float NOT NULL DEFAULT '0',
        `eps` float NOT NULL DEFAULT '0',
        `forward_pe` float NOT NULL DEFAULT '0',
        `regular_market_price` float NOT NULL DEFAULT '0',
        `regular_market_volume` float NOT NULL DEFAULT '0',
        `fifty_two_week_low` float NOT NULL DEFAULT '0',
        `fifty_day_average` float NOT NULL DEFAULT '0',
        `average_daily_volume_10_day` float NOT NULL DEFAULT '0',
        PRIMARY KEY (`symbol`)
        ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
        """
    val = (table,)
    mysql_cursor.execute(sql, table)
    mysql_cursor.close()
    return


def insert_stock(quote_dict, mysql_handle, table):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        INSERT INTO %s (
            symbol,
            long_name,
            regular_market_open,
            close,
            market_cap,
            eps,
            forward_pe,
            regular_market_price,
            regular_market_volume,
            fifty_two_week_low,
            fifty_day_average,
            average_daily_volume_10_day
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """
    val = (table
           , quote_dict[SYMBOL]
           , quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , 0
           , quote_dict[MARKET_CAP]
           , 0
           , quote_dict[FORWARD_PE]
           , quote_dict[REGULAR_MARKET_PRICE]
           , quote_dict[REGULAR_MARKET_VOLUME]
           , quote_dict[FIFTY_TWO_WEEK_LOW]
           , quote_dict[FIFTY_DAY_AVERAGE]
           , quote_dict[AVERAGE_DAILY_VOLUME_10DAY]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def upsert_stock(quote_dict, mysql_handle, table):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        SELECT *
          FROM %s
         WHERE symbol = %s
        """
    val = (table, quote_dict[SYMBOL], )
    mysql_cursor.execute(sql, val)
    record = mysql_cursor.fetchone()
    mysql_handle.commit()
    mysql_cursor.close()
    if record is None:
        insert_stock(quote_dict, mysql_handle, table)
        return
    update_stock(quote_dict, mysql_handle, table)
    return


def update_stock(quote_dict, mysql_handle, table):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        UPDATE %s
           SET long_name = %s,
               regular_market_open = %s,
               market_cap = %s,
               forward_pe = %s,
               regular_market_price = %s,
               regular_market_volume = %s,
               fifty_two_week_low = %s,
               fifty_day_average = %s,
               average_daily_volume_10_day = %s
         WHERE symbol = %s
        """
    val = (table
           , quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , quote_dict[MARKET_CAP]
           , quote_dict[FORWARD_PE]
           , quote_dict[REGULAR_MARKET_PRICE]
           , quote_dict[REGULAR_MARKET_VOLUME]
           , quote_dict[FIFTY_TWO_WEEK_LOW]
           , quote_dict[FIFTY_DAY_AVERAGE]
           , quote_dict[AVERAGE_DAILY_VOLUME_10DAY]
           , quote_dict[SYMBOL]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def retrieve_stocks(stocks, mysql_handle, table):
    for stock in stocks:
        quote = yf.Ticker(stock)
        quote_dict = quote.info
        upsert_stock(quote_dict, mysql_handle, table)
        print(quote_dict)
        print("-------------------")
    return

table = 'nasdaq'
stocks = ["SSYS", "DDD", "AAPL", "DASTY", "AMAT", "KLAC", "SBUX", "NXPI", "SHOP", "SIFY", "GE", "KO"]
mysql_handle = initialize_sql()
drop_table(table)
initialize_table(table)
retrieve_stocks(stocks, mysql_handle, table)


