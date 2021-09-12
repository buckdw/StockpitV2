import yfinance as yf
import time
import argparse
import regex as rx
import inspect
import serial
import serial.tools.list_ports

from velleman import *

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
    quote_dict_clean[REGULAR_MARKET_OPEN] = quote_dict[REGULAR_MARKET_OPEN] if REGULAR_MARKET_OPEN in quote_dict and \
                                                                               quote_dict[REGULAR_MARKET_OPEN] else 0
    quote_dict_clean[MARKET_CAP] = quote_dict[MARKET_CAP] if MARKET_CAP in quote_dict and quote_dict[MARKET_CAP] else 0
    quote_dict_clean[FORWARD_PE] = quote_dict[FORWARD_PE] if FORWARD_PE in quote_dict and quote_dict[FORWARD_PE] else 0
    quote_dict_clean[REGULAR_MARKET_PRICE] = quote_dict[REGULAR_MARKET_PRICE] if REGULAR_MARKET_PRICE in quote_dict and \
                                                                                 quote_dict[REGULAR_MARKET_PRICE] else 0
    quote_dict_clean[REGULAR_MARKET_VOLUME] = quote_dict[
        REGULAR_MARKET_VOLUME] if REGULAR_MARKET_VOLUME in quote_dict and quote_dict[REGULAR_MARKET_VOLUME] else 0
    quote_dict_clean[FIFTY_TWO_WEEK_LOW] = quote_dict[FIFTY_TWO_WEEK_LOW] if FIFTY_TWO_WEEK_LOW in quote_dict and \
                                                                             quote_dict[FIFTY_TWO_WEEK_LOW] else 0
    quote_dict_clean[FIFTY_TWO_WEEK_HIGH] = quote_dict[FIFTY_TWO_WEEK_HIGH] if FIFTY_TWO_WEEK_HIGH in quote_dict and \
                                                                               quote_dict[FIFTY_TWO_WEEK_HIGH] else 0
    quote_dict_clean[FIFTY_DAY_AVERAGE] = quote_dict[FIFTY_DAY_AVERAGE] if FIFTY_DAY_AVERAGE in quote_dict and \
                                                                           quote_dict[FIFTY_DAY_AVERAGE] else 0
    quote_dict_clean[AVERAGE_DAILY_VOLUME_10DAY] = quote_dict[
        AVERAGE_DAILY_VOLUME_10DAY] if AVERAGE_DAILY_VOLUME_10DAY in quote_dict and quote_dict[
        AVERAGE_DAILY_VOLUME_10DAY] else 0
    quote_dict_clean[EPS_TRAILING_TWELVE_MONTH] = quote_dict[
        EPS_TRAILING_TWELVE_MONTH] if EPS_TRAILING_TWELVE_MONTH in quote_dict and quote_dict[
        EPS_TRAILING_TWELVE_MONTH] else 0
    quote_dict_clean[REGULAR_MARKET_CHANGE] = quote_dict[
        REGULAR_MARKET_CHANGE] if REGULAR_MARKET_CHANGE in quote_dict and quote_dict[REGULAR_MARKET_CHANGE] else 0
    quote_dict_clean[EPS_FORWARD] = quote_dict[EPS_FORWARD] if EPS_FORWARD in quote_dict and quote_dict[
        EPS_FORWARD] else 0
    quote_dict_clean[SHARES_OUTSTANDING] = quote_dict[SHARES_OUTSTANDING] if SHARES_OUTSTANDING in quote_dict and \
                                                                             quote_dict[SHARES_OUTSTANDING] else 0
    return quote_dict_clean


def retrieve_stocks(stocks):
    stock_quotes = []
    for stock_symbol in stocks:
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
            quote_dict_sanatized = validate_quote_dict(quote_info)
            stock_quotes.append(quote_dict_sanatized)
    return stock_quotes


def load_stocks(stock_filename):
    stocks = list()
    with open(stock_filename) as stock_file:
        for line in stock_file:
            stock_symbol = strdelcc(line)
            if stock_symbol:
                stocks.append(stock_symbol)
    return stocks


def find_serial_port(filter):
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        usb_port = str(port)
        if filter in usb_port:
            return usb_port
    return None


#
#   main code
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='input file with ticker symbols to retrieve')
    args = parser.parse_args()
    stocks = load_stocks(args.file)
    stock_quotes = retrieve_stocks(stocks)
    port = find_serial_port("cu.usb")
    serial_connection = serial.Serial(port
                                      , baudrate='9600'
                                      , parity=serial.PARITY_NONE
                                      , stopbits=1
                                      , bytesize=serial.EIGHTBITS
                                      , xonxoff=True
                                      , rtscts=False
                                      , dsrdtr=False
                                      )
    line = send_page(ID00
                     , 1
                     , 'A'
                     , COLOR_RED
                     , WAIT_3S
                     , FUNCTION_SPEED_1
                     )
    print(line)
    time.sleep(1)
#   serial_connection.write(line.encode())
    index = 0
    page = 'A'
    pagenumber = ord(page[0])
    for stock_quote in stock_quotes:
        ticker = stock_quote[SYMBOL]
        quote_open = float(stock_quote[REGULAR_MARKET_OPEN])
        quote = float(stock_quote[REGULAR_MARKET_PRICE])
        fluctuation = 100 * (quote - quote_open) / quote_open
        line = send_page(ID00
                         , 1
                         , chr(pagenumber)
                         , COLOR_RED
                         , WAIT_3S
                         , '{ticker}: {quote:.2f} ({fluctuation:.1f}%)'.format(ticker=ticker
                                                                             , quote=quote
                                                                             , fluctuation=fluctuation
                                                                             )
                         )
        pagenumber += 1
        print(line)
 #       time.sleep(1)
 #       serial_connection.write(line.encode())
