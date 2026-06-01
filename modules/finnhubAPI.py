from dotenv import load_dotenv
import os, json, finnhub
from datetime import datetime, timedelta, timezone

load_dotenv()
finnhub_client = finnhub.Client(api_key=os.getenv("FH_API_KEY"))

def getNews(ticker, days=365):
    today = datetime.now(timezone.utc).date()
    delta = (today - timedelta(days=days))

    news = finnhub_client.company_news(ticker, _from=delta, to=today)


    return news

def saveNews(ticker, news):
    if not os.path.exists("./news"):
        os.makedirs("./news")

    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in news:
            infile.write(f"{article['headline']}, {article['summary']}\n")


if __name__ == "__main__":
    data = finnhub_client.company_basic_financials('AAPL', 'all')
    
    with open(f"./financials/financials_{"AAPL"}.txt", 'wt') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)