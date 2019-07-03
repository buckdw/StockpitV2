import yfinance as yf

REGULAR_MARKET_VOLUME = u'regularMarketVolume'

stocks = ["SSYS", "DDD", "AAPL", "DASTY"]
for stock in stocks:
    quote = yf.Ticker(stock)
    quote_dict = quote.info
    print(quote_dict[REGULAR_MARKET_VOLUME])


