import torch, json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

model_name = "ProsusAI/finbert" 
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

quotes = [
    "AAPL",
    "GOOG",
    "NVDA",
    "META",
    "INTC",
    "AMD"
]

for quote in quotes:
    with open(f"./news/news_{quote}.txt", 'rt') as infile:
        raw = infile.readlines()
        data = [d.strip("\n") for d in raw]

    # with open("test_X.txt", 'rt') as infile:
    #     raw = infile.readlines()
    #     data = []
    #     for record in raw:
    #         data.append(json.loads(record))
    # print(data[0]['title'])

    # titles = []
    # for record in data:
    #     titles.append(record)

    pred = finbert(data)

    # print(pred)

# try:
#     for i, result in enumerate(results):
#         print(f"Headline: {titles[i]}, Label: {result['label']}, Score: {result['score']:.4f}")
# except:
#     pass

    with open(f"./predictions/predictions_{quote}.txt", 'wt') as outfile:
        outfile.writelines([json.dumps(pred)])

    binary = {
        "positive": 1,
        "negative": -1
    }

    positives = 0
    neutrals = 0
    negatives = 0
    for p in pred:
        if p['label'] == "positive":
            positives += 1
        elif p['label'] == "neutral":
            neutrals += 1
        else:
            negatives += 1

    print(f"Quote: {quote}")
    print(f"Positives: {positives}")
    print(f"Negatives: {negatives}")
    print(f"Neutrals: {neutrals}")
    print()