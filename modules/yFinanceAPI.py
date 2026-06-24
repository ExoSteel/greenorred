import yfinance as yf
import json, os
from curl_cffi.requests import Session

session = Session(impersonate="chrome")

def getNews(ticker):
    tick = yf.Ticker(ticker, session=session)
    return tick.news

def saveNews(ticker, data):
    if not os.path.exists("./news"):
        os.makedirs("./news")

    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in data:
            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")


def getCandles(ticker):
    tick = yf.Ticker(ticker, session=session)
    data = tick.history(period="max", auto_adjust=False)
    data = data.dropna()
    # data = yf.download(ticker, period='max')
    # data.columns = data.columns.get_level_values(0)
    return data

def saveCandles(ticker, data):
    if not os.path.exists("./daily"):
        os.makedirs("./daily")

    data.to_csv(f"./daily/daily_{ticker}.csv")
    print("Saved: Candles")


def getOptionsChain(ticker):
    data = yf.Ticker(ticker, session=session)

    options = data.options
    opt = data.option_chain(options[0])

    calls_df = opt.calls
    puts_df = opt.puts

    return calls_df, puts_df

def saveOptionsChain(ticker, calls_df, puts_df):
    if not os.path.exists("./calls"):
        os.makedirs("./calls")
    if not os.path.exists("./puts"):
        os.makedirs("./puts")

    calls_df.to_csv(f"./calls/calls_{ticker}.csv")
    puts_df.to_csv(f"./puts/puts_{ticker}.csv")
    print("Saved: Calls & Puts")


def getIncomeSTMT(ticker):
    tick = yf.Ticker(ticker, session=session)
    data = tick.get_income_stmt()

    return data

def saveIncomeSTMT(ticker, data):
    if not os.path.exists("./statements"):
        os.makedirs("./statements")

    data.to_csv(f"./statements/statements_{ticker}.csv")
    print("Saved: Income Statement")


def getBalanceSheet(ticker):
    tick = yf.Ticker(ticker, session=session)
    data = tick.get_balance_sheet()

    return data

def saveBalanceSheet(ticker, data):
    if not os.path.exists("./balances"):
        os.makedirs("./balances")

    data.to_csv(f"./balances/balance_{ticker}.csv")
    print("Saved: Balance Sheet")

if __name__ == '__main__':
    # df = getCandles("DZN")
    # print(df.to_csv("./daily/daily_DZN.csv"))
    # options = getOptionsChain("AAPL")
    # print(getCandles("AAPL"))
    # pass

    # tick = yf.Ticker("GOOG")
    print(getCandles("GOOG").columns)
    saveCandles("GOOG", getCandles("GOOG"))
    # print(tick.get_balance_sheet().index)