import yfinance as yf
import json

tickers = [
    "AAPL",
    "GOOG",
    "NVDA",
    "META",
    "INTC",
    "AMD"
]


for ticker in tickers:
    tick = yf.Ticker(ticker)
    news = tick.news
    
    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in news:
            # print(article['content']['title'])
            # print(article['content']['summary'])
            # print()

            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")