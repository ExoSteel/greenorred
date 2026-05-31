import yfinance as yf
import json

def getNews(ticker):
    tick = yf.Ticker(ticker)
    return tick.news

def saveNews(ticker, data):
    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in data:
            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")

def getCandles(ticker):
    data = yf.download(ticker, period='max')
    data.columns = data.columns.get_level_values(0)
    return data

def saveCandles(ticker, data):
    print(data)
    data.to_csv(f"./daily/daily_{ticker}.csv")
    # with open(f"./daily/daily_{ticker}.txt", 'wt') as infile:
    #     for article in data:
    #         infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")    

if __name__ == '__main__':
    df = getCandles("DZN")
    print(df.to_csv("./daily/daily_DZN.csv"))