import mysql.connector
import json
import time
import argparse

from yahoo_fin.stock_info import *
from velleman import *

def initialize_sql():
    return mysql.connector.connect(host="localhost"
                                   , user="root"
                                   , passwd="j0sepace"
                                   , database="stockpit"
                                   )
def retrieve_stocks(stocks, mysql_handle):
    average_response_network = 0
    average_response_sql = 0
    stock_count = 0
    for stock in stocks:
        time_start = time.clock()
        cash_flow = get_cash_flow(stock)
        print(cash_flow)
        time_delta_network = time.clock() - time_start
        average_response_network = average_response_network + time_delta_network
        stock_count = stock_count + 1
        if quote:
            quote_dict = validate_quote_dict(quote.info)
            time_start = time.clock()
            #            upsert_stock(quote_dict, mysql_handle)
            time_delta_sql = time.clock() - time_start
            average_response_sql = average_response_sql + time_delta_sql
                # print("-------------------------------")
                # print("Stocks={:d}".format(stock_count))
                # print("Network response average={:4.2f}".format((average_response_network * 1000 * 1000) / stock_count))
                # print("SQL response average={:4.2f}".format((average_response_sql * 1000 * 1000) / stock_count))
                # print("-------------------------------")
    return


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
    retrieve_stocks(stocks, mysql_handle)
