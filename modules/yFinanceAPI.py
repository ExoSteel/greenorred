import yfinance as yf
import json, os

def getNews(ticker):
    tick = yf.Ticker(ticker)
    return tick.news

def saveNews(ticker, data):
    if not os.path.exists("./news"):
        os.makedirs("./news")

    with open(f"./news/news_{ticker}.txt", 'wt') as infile:
        for article in data:
            infile.write(f"{article['content']['title']}, {article['content']['summary']}\n")


def getCandles(ticker):
    tick = yf.Ticker(ticker)
    data = tick.history(period="max")

    # data = yf.download(ticker, period='max')
    # data.columns = data.columns.get_level_values(0)
    return data

def saveCandles(ticker, data):
    if not os.path.exists("./daily"):
        os.makedirs("./daily")

    data.to_csv(f"./daily/daily_{ticker}.csv")
    print("Saved: Candles")


def getOptionsChain(ticker):
    data = yf.Ticker(ticker)

    options = data.options
    # print(options)

    # 2. Fetch the specific option chain for a date
    opt = data.option_chain(options[0])

    # 3. Separate into calls and puts DataFrames
    calls_df = opt.calls
    puts_df = opt.puts

    # print(calls_df.head(5))
    # print()
    # print(puts_df.head())
    return calls_df, puts_df

    # # This returns columns like: strike, lastPrice, bid, ask, volume, openInterest, impliedVolatility
    # print(calls_df)
    # print()
    # print(puts_df)

    # columns = ['strike', 'lastPrice', 'volume', 'openInterest']

    # import plotly.graph_objects as go
    # headers = [
    #     "Call Volume",
    #     "Call Last",
    #     "Call Bid"
    #     "Strike",
    #     "Put Last",
    #     "Put Volume"
    # ]


    # fig = go.Figure(data=[go.Table(
    #     header=dict(
    #         values=headers,
    #         align="center"

    #     ),
    #     cells=dict(
    #         values=[calls_df[col].tolist() for col in columns],
    #         align="center"
    #     )
    # )])

    # fig.show()

def saveOptionsChain(ticker, calls_df, puts_df):
    if not os.path.exists("./calls"):
        os.makedirs("./calls")
    if not os.path.exists("./puts"):
        os.makedirs("./puts")

    calls_df.to_csv(f"./calls/calls_{ticker}.csv")
    puts_df.to_csv(f"./puts/puts_{ticker}.csv")
    print("Saved: Calls & Puts")


def getIncomeSTMT(ticker):
    tick = yf.Ticker(ticker)
    data = tick.get_income_stmt()

    return data

def saveIncomeSTMT(ticker, data):
    if not os.path.exists("./statements"):
        os.makedirs("./statements")

    data.to_csv(f"./statements/statements_{ticker}.csv")
    print("Saved: Income Statement")


def getBalanceSheet(ticker):
    tick = yf.Ticker(ticker)
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

    tick = yf.Ticker("AAPL")
    print(tick.get_balance_sheet().index)