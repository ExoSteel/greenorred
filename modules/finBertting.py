import json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
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
    with open(f"./predictions/predictions_{ticker}.txt", 'wt') as outfile:
        outfile.writelines([json.dumps(data)])