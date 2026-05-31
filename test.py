from modules.helper import readTicker, addTicker, readCandle, readPredictions, readOverview
from modules.alphaVantageAPI import getOverview, saveOverview, getBBands
from modules.yFinanceAPI import getNews, saveNews, getCandles, saveCandles
from modules.finBertting import getPrediction, savePrediction
import os
from pprint import pprint


ticker = readTicker()

predictions = readPredictions("NVDA")

pprint(predictions)