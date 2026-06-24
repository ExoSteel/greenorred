import os
import sys
import warnings

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

import json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

sys.stderr = old_stderr

# from modules.helper import readNews

def readNews(ticker):
    try:
        with open(f"./news/news_{ticker}.txt", 'rt') as infile:
            raw = infile.readlines()
            data = [d.strip("\n") for d in raw]
    
        return data
    except Exception as e:
        print(e)

def getPrediction(ticker):
    model_name = "ProsusAI/finbert" 
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    finbert = pipeline(
        "sentiment-analysis", 
        model=model, 
        tokenizer=tokenizer
    )

    data = readNews(ticker)

    if data == []:
        return []

    pred = finbert(
        data, 
        truncation=True, 
        max_length=512
    )

    return pred

def savePrediction(ticker, data):
    if not os.path.exists("./predictions"):
        os.makedirs("./predictions")

    with open(f"./predictions/predictions_{ticker}.txt", 'wt') as outfile:
        outfile.writelines([json.dumps(data)])

if __name__ == "__main__":
    preds = getPrediction("AAPL")
    savePrediction("AAPL", preds)