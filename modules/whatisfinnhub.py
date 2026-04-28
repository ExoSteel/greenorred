from dotenv import load_dotenv
import os
import finnhub
import time

load_dotenv()
finnhub_client = finnhub.Client(api_key=os.getenv("FH_API_KEY"))

def getNews(ticker):
    news = finnhub_client.company_news(ticker, _from="2026-04-01", to="2026-04-28")

    return news

def saveNews(ticker, news):
     with open(f"./news/news_{ticker}.txt", 'wt') as infile:
            for article in news:
                infile.write(f"{article['headline']}, {article['summary']}\n")

def getCandles(ticker):
    now = int(time.time())
    one_month = now - (30 * 24 * 60 * 60)

    candles = finnhub_client.stock_candles(ticker, 'D', one_month, now)

    return candles

def saveCandles(ticker, candles):
    pass