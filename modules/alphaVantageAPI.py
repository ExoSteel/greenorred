from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from dotenv import load_dotenv
import os, csv

load_dotenv()
AV_API_KEY = os.getenv("AV_API_KEY")

def getCandle(ticker):
    ts = TimeSeries(key=AV_API_KEY, output_format='pandas')

    data, meta = ts.get_daily(symbol=ticker, outputsize='compact')

    return data, meta
    
def saveCandle(ticker, data):
    data.to_csv(f"./daily/daily_{ticker}.csv")
    print("done!")
    print()


def getOverview(ticker):
    fd = FundamentalData(key='AV_API_KEY')
    data, meta = fd.get_company_overview(symbol=ticker)

    return data, meta

def saveOverview(ticker, data):
    with open(f"./overviews/overview_{ticker}.csv", "wt") as outfile:
        writer = csv.writer(outfile)
        for key, value in data.items():
            writer.writerow([key, value])
    
    print("done!")
    print()


def getBBands(ticker):
    ti = TechIndicators(key='AV_API_KEY', output_format='pandas')
    data, meta_data = ti.get_bbands(symbol=ticker, interval='60min', time_period=60)
    return data

def saveBBands(ticker, data):
    data.to_csv(f"./bbands/bbands_{ticker}.csv")
    print("done!")
    print()