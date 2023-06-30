#!/usr/bin/env python3

import yfinance as yf
import json
import time
import argparse
import regex as rx
import inspect
import math
import mongo 

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
    print(function_id())
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



def retrieve_block_of_stocks(stocks):
    print(function_id())
    stock_symbols = ' '.join(stocks)
    print(stock_symbols)
    stock_count = 0
    time_start = time.perf_counter()
    quotes = yf.Tickers(stock_symbols)
    for quote in quotes.tickers:
        valid_quote = True
        try:
            quote_info = quote.info
        except (IndexError, KeyError, ValueError) as e:
            valid_quote = False
            print('Error')
            print(e)
        if valid_quote:
            quote_dict_sanatized = validate_quote_dict(quote_info)
    return


def retrieve_stocks(stocks):
    print(function_id())
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
            quote_dict_sanatized = validate_quote_dict(quote_info)
            print(quote_dict_sanatized)
    return



def load_stocks(stock_filename):
    print(function_id())
    stocks = list()
    with open(stock_filename) as stock_file:
        for line in stock_file:
            stock_symbol = strdelcc(line)
            if stock_symbol:
                stocks.append(stock_symbol)
    return stocks


#
#   main code
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='input file with ticker symbols to retrieve')
    args = parser.parse_args()
    mongo = mongo.Mongo("", "", "")
    print(mongo)
    print("***")

    stocks = load_stocks(args.file)
    print(retrieve_block_of_stocks)
    retrieve_stocks(stocks)

