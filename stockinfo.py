import yfinance as yf
import mysql.connector
import json
import time

from yahoo_fin.stock_info import *


#
#   main code
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    args = parser.parse_args()

