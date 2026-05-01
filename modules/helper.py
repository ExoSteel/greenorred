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

def readCandle(ticker):
    data = pd.read_csv(f"./daily/daily_{ticker}.csv")
    return data

def readNews(ticker):
    with open(f"./news/news_{ticker}.txt", 'rt') as infile:
        raw = infile.readlines()
        data = [d.strip("\n") for d in raw]
    
    return data

def readPredictions(ticker):
    with open(f"./predictions/predictions_{ticker}.txt", "rt") as infile:
        data = json.loads(infile.read())
    
    return data

def readOverview(ticker):
    with open(f'./overviews/overview_{ticker}.csv', 'rt') as infile:
        reader = csv.reader(infile)
        data = {}
        for row in reader:
            data[row[0]] = row[1]
        
    return data

if __name__ == "__main__":
    # addTicker("AMZN")
    # readOverview("AAPL")
    data = readCandle("AAPL")
    print(data.iloc[0])