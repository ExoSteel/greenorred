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

model_name = "ProsusAI/finbert"
save_path = "./.local_model"

if not os.path.exists(save_path):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)
else:
    tokenizer = BertTokenizer.from_pretrained(model_name, local_files_only=True)
    model = BertForSequenceClassification.from_pretrained(model_name, local_files_only=True)

finbert = pipeline(
    "sentiment-analysis", 
    model=model, 
    tokenizer=tokenizer
)

def readNews(ticker):
    try:
        with open(f"./news/news_{ticker}.json", 'rt') as infile:
            data = json.loads(infile.read())
    
        return data
    except Exception as e:
        print(e)

def getPrediction(ticker):
    data = readNews(ticker)

    if data == []:
        return []

    newsHeadlines = []

    for news in data:
        string = news["headline"] + news["summary"]
        newsHeadlines.append(string)

    pred = finbert(
        newsHeadlines, 
        truncation=True, 
        #max_length=512
    )

    return pred

def savePrediction(ticker, data):
    if not os.path.exists("./predictions"):
        os.makedirs("./predictions")

    with open(f"./predictions/predictions_{ticker}.json", 'wt') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print("Saved: Predictions")

if __name__ == "__main__":
    preds = getPrediction("GOOG")
    savePrediction("GOOG", preds)

    