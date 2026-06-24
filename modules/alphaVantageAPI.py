from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from dotenv import load_dotenv
import os, csv

load_dotenv()
AV_API_KEY = os.getenv("AV_API_KEY")

# def getCandles(ticker):
#     try:
#         ts = TimeSeries(key=AV_API_KEY, output_format='pandas')

#         data, meta = ts.get_daily(symbol=ticker, outputsize='compact')

#         return data, meta
#     except Exception as e:
#         print(e)
#         return None
    
# def saveCandles(ticker, data):
#     if not os.path.exists("./daily"):
#         os.makedirs("./daily")

#     data.to_csv(f"./daily/daily_{ticker}.csv", mode='w')
#     print("Saving Candle: Done!")
#     print()


def getOverview(ticker):
    try:
        fd = FundamentalData(key='AV_API_KEY')
        data, meta = fd.get_company_overview(symbol=ticker)
        print("Getting Overview: Done!")

        return data, meta
    except Exception as e:
        print(e)
        return None, None

def saveOverview(ticker, data):
    if not os.path.exists("./overviews"):
        os.makedirs("./overviews")

    with open(f"./overviews/overview_{ticker}.csv", "wt") as outfile:
        writer = csv.writer(outfile)
        for key, value in data.items():
            writer.writerow([key, value])
    
    print("Saving Overview: Done!")
    print()


# def getBBands(ticker):
#     try:
#         ti = TechIndicators(key='AV_API_KEY', output_format='pandas')
#         data, meta_data = ti.get_bbands(symbol=ticker, interval='60min', time_period=60)
#         return data
#     except Exception as e:
#         print(e)
#         return None

# def saveBBands(ticker, data):
#     data.to_csv(f"./bbands/bbands_{ticker}.csv")
#     print("done!")
#     print()

if __name__ == "__main__":
    # bbands = getBBands("AAPL")
    # print(bbands)
    # saveBBands("AAPL", bbands)

    overview, meta = getOverview("GOOG")
    saveOverview("GOOG", overview)