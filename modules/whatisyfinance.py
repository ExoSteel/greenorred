import yfinance as yf
import json

with open("tickers.txt", "rt") as infile:
    data = infile.readlines()
    tickers = [d.strip("\n") for d in data]



for ticker in tickers:
    tick = yf.Ticker(ticker)
    news = tick.news
    
    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in news:
            # print(article['content']['title'])
            # print(article['content']['summary'])
            # print()

            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")