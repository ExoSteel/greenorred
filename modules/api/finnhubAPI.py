from dotenv import load_dotenv
import os, json, finnhub
from datetime import datetime, timedelta, timezone

load_dotenv()
finnhub_client = finnhub.Client(api_key=os.getenv("FH_API_KEY"))

def getNews(ticker, days=62):
    today = datetime.now(timezone.utc).date()
    delta = (today - timedelta(days=days))

    news = finnhub_client.company_news(ticker, _from=delta, to=today)

    for new in news:
        timestamp = new["datetime"]
        new["date"] = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")

    return news

def saveNews(ticker, news):
    if not os.path.exists("./news"):
        os.makedirs("./news")

    with open(f"./news/news_{ticker}.json", 'wt') as outfile:
        json.dump(news, outfile, ensure_ascii=False, indent=4)
    print("Saved: News")


def getFinancials(ticker):
    try:
        data = finnhub_client.company_basic_financials(ticker, 'all')
        return data
    except Exception as e:
        print(e)

def saveFinancials(ticker, data):
    if not os.path.exists("./financials"):
        os.makedirs("./financials")

    with open(f"./financials/financials_{ticker}.json", 'wt') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print("Saved: Financials")

if __name__ == "__main__":
    # data = finnhub_client.company_basic_financials('AAPL', 'all')
    
    data = getNews("GOOG")
    saveNews("GOOG", data)