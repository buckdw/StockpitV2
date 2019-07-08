import yfinance as yf
import mysql.connector
import json
import time

from yahoo_fin.stock_info import *

def initialize_sql():
    return mysql.connector.connect(host="localhost"
                                   , user="root"
                                   , passwd="j0sepace"
                                   , database="stockpit"
                                   )

def load_stocks(stock_filename):
    stocks = list()
    with open(stock_filename) as stock_file:
        for line in stock_file:
            stocks.append(line)
    return stocks

#
#   main code
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    args = parser.parse_args()

    stocks = load_stocks(args.file)
    mysql_handle = initialize_sql()
