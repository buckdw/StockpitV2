import yfinance as yf
import mysql.connector
import json
import time
import argparse
import regex as rx
import inspect


REGULAR_MARKET_VOLUME = u'regularMarketVolume'
SYMBOL = u'symbol'
LONG_NAME = u'longName'
REGULAR_MARKET_OPEN = u'regularMarketOpen'
AVERAGE_DAILY_VOLUME_10DAY = u'averageDailyVolume10Day'
SHARES_OUTSTANDING = u'sharesOutstanding'
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


def function_id():
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame, 2)
    return caller_frame[1][3]


def strdelcc(str):
    return rx.sub(r'\p{C}', '', str)
    
    
def validate_quote_dict(quote_dict):
    quote_dict_clean = {}
    quote_dict_clean[SYMBOL] = quote_dict[SYMBOL] if LONG_NAME in quote_dict and quote_dict[SYMBOL] else ''
    quote_dict_clean[LONG_NAME] = quote_dict[LONG_NAME] if LONG_NAME in quote_dict and quote_dict[LONG_NAME] else ''
    quote_dict_clean[REGULAR_MARKET_OPEN] = quote_dict[REGULAR_MARKET_OPEN] if REGULAR_MARKET_OPEN in quote_dict and quote_dict[REGULAR_MARKET_OPEN] else 0
    quote_dict_clean[MARKET_CAP] = quote_dict[MARKET_CAP] if MARKET_CAP in quote_dict and quote_dict[MARKET_CAP] else 0
    quote_dict_clean[FORWARD_PE] = quote_dict[FORWARD_PE] if FORWARD_PE in quote_dict and quote_dict[FORWARD_PE] else 0
    quote_dict_clean[REGULAR_MARKET_PRICE] = quote_dict[REGULAR_MARKET_PRICE] if REGULAR_MARKET_PRICE in quote_dict and quote_dict[REGULAR_MARKET_PRICE] else 0
    quote_dict_clean[REGULAR_MARKET_VOLUME] = quote_dict[REGULAR_MARKET_VOLUME] if REGULAR_MARKET_VOLUME in quote_dict and quote_dict[REGULAR_MARKET_VOLUME] else 0
    quote_dict_clean[FIFTY_TWO_WEEK_LOW] = quote_dict[FIFTY_TWO_WEEK_LOW] if FIFTY_TWO_WEEK_LOW in quote_dict and quote_dict[FIFTY_TWO_WEEK_LOW] else 0
    quote_dict_clean[FIFTY_TWO_WEEK_HIGH] = quote_dict[FIFTY_TWO_WEEK_HIGH] if FIFTY_TWO_WEEK_HIGH in quote_dict and quote_dict[FIFTY_TWO_WEEK_HIGH] else 0
    quote_dict_clean[FIFTY_DAY_AVERAGE] = quote_dict[FIFTY_DAY_AVERAGE] if FIFTY_DAY_AVERAGE in quote_dict and quote_dict[FIFTY_DAY_AVERAGE] else 0
    quote_dict_clean[AVERAGE_DAILY_VOLUME_10DAY] = quote_dict[AVERAGE_DAILY_VOLUME_10DAY] if AVERAGE_DAILY_VOLUME_10DAY in quote_dict and quote_dict[AVERAGE_DAILY_VOLUME_10DAY] else 0
    quote_dict_clean[EPS_TRAILING_TWELVE_MONTH] = quote_dict[EPS_TRAILING_TWELVE_MONTH] if EPS_TRAILING_TWELVE_MONTH in quote_dict and quote_dict[EPS_TRAILING_TWELVE_MONTH] else 0
    quote_dict_clean[REGULAR_MARKET_CHANGE] = quote_dict[REGULAR_MARKET_CHANGE] if REGULAR_MARKET_CHANGE in quote_dict and quote_dict[REGULAR_MARKET_CHANGE] else 0
    quote_dict_clean[EPS_FORWARD] = quote_dict[EPS_FORWARD] if EPS_FORWARD in quote_dict and quote_dict[EPS_FORWARD] else 0
    quote_dict_clean[SHARES_OUTSTANDING] = quote_dict[SHARES_OUTSTANDING] if SHARES_OUTSTANDING in quote_dict and  quote_dict[SHARES_OUTSTANDING] else 0
    return quote_dict_clean


def initialize_sql():
    print(function_id())
    return mysql.connector.connect(host='localhost'
                                   , user='root'
                                   , passwd='Emers0nFitti'
                                   , database='stockpit'
                                   )


def drop_table():
    print(function_id())
    mysql_cursor = mysql_handle.cursor()
    sql = """
        DROP TABLE IF EXISTS `nasdaq`
        """
    mysql_cursor.execute(sql)
    mysql_cursor.close()
    return


def initialize_table():
    print(function_id())
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
        `shares_outstanding` bigint NOT NULL DEFAULT '0',
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
           , quote_dict[SHARES_OUTSTANDING]
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
           , quote_dict[SHARES_OUTSTANDING]
           , quote_dict[SYMBOL]
           )
    mysql_cursor.execute(sql, val)
    mysql_handle.commit()
    mysql_cursor.close()
    return


def retrieve_block_of_stocks(stocks, mysql_cursor):
    print(function_id())
    stock_symbols = ' '.join(stocks)
    print(stock_symbols)
    return


def retrieve_stocks(stocks, mysql_handle):
    print(function_id())
    average_response_network = 0
    average_response_sql = 0
    stock_count = 0
    for stock_symbol in stocks:
        print('*** TICKER = ' + stock_symbol)
        time_start = time.perf_counter()
        quote = yf.Ticker(stock_symbol)
        valid_quote = True
        try:
            quote_info = quote.info
        except (IndexError, KeyError, ValueError) as e:
            valid_quote = False
            print('Error')
            print(e)
        if valid_quote:
            time_delta_network = time.perf_counter() - time_start
            average_response_network = average_response_network + time_delta_network
            stock_count = stock_count + 1
            if quote:
                quote_dict_sanatized = validate_quote_dict(quote_info)
                time_start = time.perf_counter()
                upsert_stock(quote_dict_sanatized, mysql_handle)
                time_delta_sql = time.perf_counter() - time_start
                average_response_sql = average_response_sql + time_delta_sql
    print('-------------------------------')
    print('stocks={:d}'.format(stock_count))
    print('Network response average={:4.2f}'.format((average_response_network * 1000 * 1000) / stock_count))
    print('SQL response average={:4.2f}'.format((average_response_sql * 1000 * 1000) / stock_count))
    print('-------------------------------')
    return

#
#   throw out noise
#       companies without market cap are worthless
#       remove penny stocks
#
def remove_stocks(stocks, mysql_handle):
    print(function_id())
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


def load_stocks(stock_filename):
    print(function_id())
    stocks = list()
    with open(stock_filename) as stock_file:
        for line in stock_file:
            stock_symbol = strdelcc(line)
            stocks.append(stock_symbol)
    return stocks


#
#   main code
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='input file with ticker symbols to retrieve')
    parser.add_argument('--drop', default=False, action='store_true' , help='drop table because of DDL change')
    args = parser.parse_args()
    stocks = load_stocks(args.file)
#
#   preparation for getting chunks of stock_size stocks
#
    stock_begin = 0
    stock_end = len(stocks)
    stock_size = 10
    mysql_handle = initialize_sql()
    if args.drop:
        drop_table()
    initialize_table()
    stock_list = stocks[stock_begin:stock_begin+10]
    print(stock_list)
#
#   for range construction with number of blocks
#   but first adjust retrieve_stocks to handle a set
#
    retrieve_block_of_stocks(stock_list, mysql_handle)
    retrieve_stocks(stocks, mysql_handle)
    remove_stocks(stocks, mysql_handle)

