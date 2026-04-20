from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

url = "https://sg.finance.yahoo.com"

resp = requests.get(url, headers = {'User-agent': 'beep boop bot'})

# print(resp.content)
soup = BeautifulSoup(resp.content, "html.parser")
# print(content)
headlines = soup.find_all(class_="titles")
print(headlines[0])

articles = []

for i, art in enumerate(articles):
    article = {}
    article['title'] = headlines[art]:
    