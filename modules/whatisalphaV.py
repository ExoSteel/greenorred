from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd
from dotenv import load_dotenv
import os, time, csv

load_dotenv()
AV_API_KEY = os.getenv("AV_API_KEY")

fd = FundamentalData(key='AV_API_KEY')
# ts = TimeSeries(key=AV_API_KEY, output_format='pandas')

with open("tickers.txt", "rt") as infile:
    data = infile.readlines()
    tickers = [d.strip("\n") for d in data]

for ticker in tickers:
    print(ticker)
    time.sleep(2)
    # data, meta = ts.get_daily(symbol=ticker, outputsize='compact')

    # data.to_csv(f"./daily/daily_{ticker}.csv")
    # print("done!")
    # print()

    data, meta = fd.get_company_overview(symbol=ticker)

    with open(f"./overviews/overview_{ticker}.csv", "wt") as outfile:
        writer = csv.writer(outfile)
        for key, value in data.items():
            writer.writerow([key, value])
    # print(data)