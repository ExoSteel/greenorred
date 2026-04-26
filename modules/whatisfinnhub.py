from dotenv import load_dotenv
import os
import finnhub

load_dotenv()
API_KEY = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key=API_KEY)

tickers = [
    "AAPL",
    "GOOG",
    "NVDA",
    "META",
    "INTC",
    "AMD",
    "TSM",
    "NFLX",
    "T",
    "V",
    "MA",
    "COST",
    "BTC",
    # "700"
]

for ticker in tickers:
    news = finnhub_client.company_news(ticker, _from="2026-04-01", to="2026-04-25")

    # for article in news:
    #     print(f"Headline: {article['headline']}")
    #     print(f"Summary: {article['summary']}")
    #     print("-" * 20)

    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
            for article in news:
                infile.write(f"{article['headline']}, {article['summary']}\n")