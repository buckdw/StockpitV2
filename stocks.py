import yfinance as yf
import mysql.connector
import json
import time

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
FIFTY_TWO_WEEK_HIGH = u'fiftyTwoWeekHigh'
FIFTY_DAY_AVERAGE = u'fiftyDayAverage'
AVERAGE_DAILY_VOLUME_10DAY = u'averageDailyVolume10Day'
EPS_TRAILING_TWELVE_MONTH = u'epsTrailingTwelveMonths'
REGULAR_MARKET_CHANGE = u'regularMarketChange'
EPS_FORWARD = u'epsForward'


def validate_quote_dict(quote_dict):
    quote_dict_clean = {}
    quote_dict_clean[SYMBOL] = quote_dict[SYMBOL] if LONG_NAME in quote_dict else ''
    quote_dict_clean[LONG_NAME] = quote_dict[LONG_NAME] if LONG_NAME in quote_dict else ''
    quote_dict_clean[REGULAR_MARKET_OPEN] = quote_dict[REGULAR_MARKET_OPEN] if REGULAR_MARKET_OPEN in quote_dict else 0
    quote_dict_clean[MARKET_CAP] = quote_dict[MARKET_CAP] if MARKET_CAP in quote_dict else 0
    quote_dict_clean[FORWARD_PE] = quote_dict[FORWARD_PE] if FORWARD_PE in quote_dict else 0
    quote_dict_clean[REGULAR_MARKET_PRICE] = quote_dict[REGULAR_MARKET_PRICE] if REGULAR_MARKET_PRICE in quote_dict else 0
    quote_dict_clean[REGULAR_MARKET_VOLUME]  = quote_dict[REGULAR_MARKET_VOLUME] if REGULAR_MARKET_VOLUME in quote_dict else 0
    quote_dict_clean[FIFTY_TWO_WEEK_LOW] = quote_dict[FIFTY_TWO_WEEK_LOW] if FIFTY_TWO_WEEK_LOW in quote_dict else 0
    quote_dict_clean[FIFTY_TWO_WEEK_HIGH] = quote_dict[FIFTY_TWO_WEEK_HIGH] if FIFTY_TWO_WEEK_HIGH in quote_dict else 0
    quote_dict_clean[FIFTY_DAY_AVERAGE] = quote_dict[FIFTY_DAY_AVERAGE] if FIFTY_DAY_AVERAGE in quote_dict else 0
    quote_dict_clean[AVERAGE_DAILY_VOLUME_10DAY] = quote_dict[AVERAGE_DAILY_VOLUME_10DAY] if AVERAGE_DAILY_VOLUME_10DAY in quote_dict else 0
    quote_dict_clean[EPS_TRAILING_TWELVE_MONTH] = quote_dict[EPS_TRAILING_TWELVE_MONTH] if EPS_TRAILING_TWELVE_MONTH in quote_dict else 0
    quote_dict_clean[REGULAR_MARKET_CHANGE] = quote_dict[REGULAR_MARKET_CHANGE] if REGULAR_MARKET_CHANGE in quote_dict else 0
    quote_dict_clean[EPS_FORWARD] = quote_dict[EPS_FORWARD] if EPS_FORWARD in quote_dict else 0
    quote_dict_clean[SHARES_OUTSTANING] = quote_dict[SHARES_OUTSTANING] if SHARES_OUTSTANING in quote_dict else 0
    return quote_dict_clean


def initialize_sql():
    return mysql.connector.connect(host="localhost"
                                   , user="root"
                                   , passwd="j0sepace"
                                   , database="stockpit"
                                   )


def drop_table():
    mysql_cursor = mysql_handle.cursor()
    sql = """
        DROP TABLE IF EXISTS `nasdaq`
        """
    mysql_cursor.execute(sql)
    mysql_cursor.close()
    return


def initialize_table():
    mysql_cursor = mysql_handle.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS `nasdaq` (
        `symbol` varchar(8) NOT NULL DEFAULT '',
        `long_name` varchar(255) NOT NULL DEFAULT '',
        `regular_market_open` float NOT NULL DEFAULT '0',
        `market_cap` float NOT NULL DEFAULT '0',
        `forward_pe` float NOT NULL DEFAULT '0',
        `regular_market_price` float NOT NULL DEFAULT '0',
        `regular_market_volume` float NOT NULL DEFAULT '0',
        `fifty_two_week_low` float NOT NULL DEFAULT '0',
        `fifty_two_week_high` float NOT NULL DEFAULT '0',
        `fifty_day_average` float NOT NULL DEFAULT '0',
        `average_daily_volume_10_day` float NOT NULL DEFAULT '0',
        `eps_trailing_twelve_month` float NOT NULL DEFAULT '0',
        `regular_market_change` float NOT NULL DEFAULT '0',
        `eps_forward` float NOT NULL DEFAULT '0',
        `shares_outstanding` decimal NOT NULL DEFAULT '0',
        PRIMARY KEY (`symbol`)
        ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
        """
    mysql_cursor.execute(sql)
    mysql_cursor.close()
    return


def insert_stock(quote_dict, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        INSERT INTO `nasdaq` (
            symbol,
            long_name,
            regular_market_open,
            market_cap,
            forward_pe,
            regular_market_price,
            regular_market_volume,
            fifty_two_week_low,
            fifty_two_week_high,
            fifty_day_average,
            average_daily_volume_10_day,
            eps_trailing_twelve_month,
            regular_market_change,
            eps_forward,
            shares_outstanding
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
            %s,
            %s,
            %s,
            %s
        )
        """
    val = (  quote_dict[SYMBOL]
           , quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , quote_dict[MARKET_CAP]
           , quote_dict[FORWARD_PE]
           , quote_dict[REGULAR_MARKET_PRICE]
           , quote_dict[REGULAR_MARKET_VOLUME]
           , quote_dict[FIFTY_TWO_WEEK_LOW]
           , quote_dict[FIFTY_TWO_WEEK_HIGH]
           , quote_dict[FIFTY_DAY_AVERAGE]
           , quote_dict[AVERAGE_DAILY_VOLUME_10DAY]
           , quote_dict[EPS_TRAILING_TWELVE_MONTH]
           , quote_dict[REGULAR_MARKET_CHANGE]
           , quote_dict[EPS_FORWARD]
           , quote_dict[SHARES_OUTSTANING]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def upsert_stock(quote_dict, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        SELECT *
          FROM `nasdaq`
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
        UPDATE `nasdaq`
           SET long_name = %s,
               regular_market_open = %s,
               market_cap = %s,
               forward_pe = %s,
               regular_market_price = %s,
               regular_market_volume = %s,
               fifty_two_week_low = %s,
               fifty_two_week_high = %s,
               fifty_day_average = %s,
               average_daily_volume_10_day = %s,
               eps_trailing_twelve_month = %s,
               regular_market_change = %s,
               eps_forward = %s,
               shares_outstanding = %s
         WHERE symbol = %s
        """
    val = (  quote_dict[LONG_NAME]
           , quote_dict[REGULAR_MARKET_OPEN]
           , quote_dict[MARKET_CAP]
           , quote_dict[FORWARD_PE]
           , quote_dict[REGULAR_MARKET_PRICE]
           , quote_dict[REGULAR_MARKET_VOLUME]
           , quote_dict[FIFTY_TWO_WEEK_LOW]
           , quote_dict[FIFTY_TWO_WEEK_HIGH]
           , quote_dict[FIFTY_DAY_AVERAGE]
           , quote_dict[AVERAGE_DAILY_VOLUME_10DAY]
           , quote_dict[EPS_FORWARD]
           , quote_dict[REGULAR_MARKET_CHANGE]
           , quote_dict[EPS_FORWARD]
           , quote_dict[SHARES_OUTSTANING]
           , quote_dict[SYMBOL]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def retrieve_stocks(stocks, mysql_handle):
    average_response = 0
    stock_count = 0
    for stock in stocks:
        time_start = time.clock()
        quote = yf.Ticker(stock)
        time_delta = time.clock() - time_start
        average_response = average_response + time_delta
        stock_count = stock_count + 1
        #        print "Network response time={:4.2f} Average={:4.2f}".format(time_delta * 1000 * 1000, (average_response * 1000 * 1000) / stock_count)
        if quote:
            quote_dict = validate_quote_dict(quote.info)
            time_start = time.clock()
            upsert_stock(quote_dict, mysql_handle)
            time_delta = time.clock() - time_start
            # print "SQL response time={:4.2f}".format(time_delta * 1000 * 1000)

            #   print("-------------------")
            #   print(stock)
            #   print(json.dumps(quote_dict, indent=4))
            #   print("-------------------")
    return

#
#   throw out noise
#       companies without market cap are worthless
#       remove penny stocks
#
def remove_stocks(stocks, mysql_handle):
    mysql_cursor = mysql_handle.cursor()
    sql = """
        DELETE
          FROM `nasdaq`
         WHERE market_cap < 100000
        """
    mysql_cursor.execute(sql)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def load_stocks():
    stocks = list()
    with open('stocks.txt') as stock_file:
        for line in stock_file:
            stocks.append(line)
    return stocks

stocks = load_stocks()
mysql_handle = initialize_sql()
# drop_table()
initialize_table()
retrieve_stocks(stocks, mysql_handle)
remove_stocks(stocks, mysql_handle)

