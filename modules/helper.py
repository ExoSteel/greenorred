import json, csv
import pandas as pd

def readTicker():
    with open("./tickers.txt", "rt") as infile:
        data = infile.readlines()
        tickers = [d.strip("\n") for d in data]
    
    return tickers

def addTicker(ticker):
    with open("./tickers.txt", "rt") as infile:
        data = infile.readlines()
        tickers = [d.strip("\n") for d in data]
    
    if ticker in tickers:
        return

    with open("./tickers.txt", 'at') as outfile:
        outfile.write("\n" + ticker)

def readCandles(ticker):
    try:
        data = pd.read_csv(f"./daily/daily_{ticker}.csv")
        return data
    except Exception as e:
        print(e)

def readNews(ticker):
    try:
        with open(f"./news/news_{ticker}.txt", 'rt') as infile:
            raw = infile.readlines()
            data = [d.strip("\n") for d in raw]
    
        return data
    except Exception as e:
        print(e)

def readPredictions(ticker):
    try:
        with open(f"./predictions/predictions_{ticker}.txt", "rt") as infile:
            data = json.loads(infile.read())
        
        return data
    except Exception as e:
        print(e)

def readOverview(ticker):
    try:
        with open(f'./overviews/overview_{ticker}.csv', 'rt') as infile:
            reader = csv.reader(infile)
            data = {}
            for row in reader:
                data[row[0]] = row[1]
            
        return data
    except Exception as e:
        print(e)

def readOptionsChain(ticker):
    try:
        calls_df = pd.read_csv(f"./calls/calls_{ticker}.csv")
        puts_df = pd.read_csv(f"./puts/puts_{ticker}.csv")
        return calls_df, puts_df
    except Exception as e:
        print(e)

def readFearAndGreed():
    try:
        data = pd.read_json("./others/fear_and_greed.json")
        return data
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # addTicker("AMZN")
    # readOverview("AAPL")
    # data = readCandle("AAPL")
    # print(data.iloc[0])

    print(readFearAndGreed())