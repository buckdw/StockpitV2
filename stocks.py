import fix_yahoo_finance as yf
import mysql.connector
import yfinance as yf

stocks = ["SSYS", "DDD", "AAPL", "DASTY"]
for stock in stocks:
    quote = yf.Ticker(stock)
    print(quote.info)

