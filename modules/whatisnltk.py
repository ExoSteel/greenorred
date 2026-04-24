import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from spellchecker import SpellChecker
import contractions

# Download stuff
# nltk.download("punkt_tab")
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('wordnet')

# Test text
corpus = [
    "I can't wait for the new season of my favorite show! 😍",
    "The COVID-19 pandemic has affected millions of people worldwide.",
    "U.S. stocks fell on Friday after news of rising inflation.",
    "<html><body>Welcome to the website!</body></html>",
    "Python is a great programming language!!! ??",
    "Check out https://www.example.com for more info!",
    "He won 1st prize in the comp3tition!!!",
    "I luvv this movie sooo much!!!"
]

# Step 1: Text cleaning
import re
import string
from bs4 import BeautifulSoup

def clean(text):
    text = text.lower()
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

corpus = [clean(sentence) for sentence in corpus]

# print(corpus)

# Contractions Expansion
expanded_corpus = [contractions.fix(doc) for doc in corpus]

# Tokenization
# text = "testing one two three. im a bird"

sentences = []
for text in expanded_corpus:
    sentences.append(sent_tokenize(text))

# print(sentences)

tokens = []
for sentence in sentences:
    for word in sentence:
        tokens.append(word_tokenize(word))

print(tokens)

# Stopword Removal
stop_words = set(stopwords.words('english'))
filtered_tokens = [[word for word in doc if word not in stop_words] for doc in tokens]

# print(len(filtered_tokens[0]))

# Stemming

stemmer = PorterStemmer()

stemmed_tokens = [[stemmer.stem(word) for word in doc] for doc in filtered_tokens]

# print(stemmed_tokens[1])

# Lemmatization

lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [[lemmatizer.lemmatize(word) for word in doc] for doc in stemmed_tokens]

# Spell Correction
spell = SpellChecker()
corrected_tokens = [[spell.correction(word) for word in doc] for doc in lemmatized_tokens]

print()
print(corrected_tokens)

# Parts of Speech (POS) Tagging

pos_tagged_tokens = [nltk.pos_tag(doc) for doc in corrected_tokens]

print()
print(pos_tagged_tokens)