import os
import sys
import warnings

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

import json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

sys.stderr = old_stderr

from modules.helper import readNews

def getPrediction(ticker):
    model_name = "ProsusAI/finbert" 
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    data = readNews(ticker)

    if data == []:
        return []

    pred = finbert(data)

    return pred

def savePrediction(ticker, data):
    if not os.path.exists("./predictions"):
        os.makedirs("./predictions")

    with open(f"./predictions/predictions_{ticker}.txt", 'wt') as outfile:
        outfile.writelines([json.dumps(data)])