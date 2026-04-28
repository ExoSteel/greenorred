from dotenv import load_dotenv
import os
import finnhub
import time

# Current Unix time
now = int(time.time())
one_month = now - (30 * 24 * 60 * 60)

load_dotenv()
API_KEY = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key=API_KEY)

with open("tickers.txt", "rt") as infile:
    data = infile.readlines()
    tickers = [d.strip("\n") for d in data]

for ticker in tickers:
    print(ticker)
    news = finnhub_client.company_news(ticker, _from="2026-04-01", to="2026-04-28")

    # for article in news:
    #     print(f"Headline: {article['headline']}")
    #     print(f"Summary: {article['summary']}")
    #     print("-" * 20)

    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
            for article in news:
                infile.write(f"{article['headline']}, {article['summary']}\n")

    candles = finnhub_client.stock_candles(ticker, 'D', one_month, now)

    print(candles)
    break