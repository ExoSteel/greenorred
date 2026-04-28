import yfinance as yf
import json

def getNews(ticker):
    tick = yf.Ticker(ticker)
    return tick.news

def saveNews(ticker, data):
    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in data:
            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")