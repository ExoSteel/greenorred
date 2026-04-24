import torch, json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

model_name = "ProsusAI/finbert" 
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

with open("test_X.txt", 'rt') as infile:
    raw = infile.readlines()
    data = []
    for record in raw:
        data.append(json.loads(record))
# print(data[0]['title'])

titles = []
for record in data:
    titles.append(record['title'])

results = []
for record in data:
    pred = finbert(titles)
    results.append(pred)

print(results)

# try:
#     for i, result in enumerate(results):
#         print(f"Headline: {titles[i]}, Label: {result['label']}, Score: {result['score']:.4f}")
# except:
#     pass

with open("predictions.txt", 'wt') as outfile:
    outfile.writelines([json.dumps(results)])