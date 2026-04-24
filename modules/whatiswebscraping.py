from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from newspaper import Article
import requests
from pprint import pprint
import json

chrome_options = Options()
chrome_options.add_argument("--headless=new") # The modern headless flag
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu") # Often fixes crashes in Linux
chrome_options.add_argument("--window-size=1920,1080") # Set a virtual resolution


driver = webdriver.Chrome(options=chrome_options)

url = "https://sg.finance.yahoo.com"

resp = requests.get(url, headers = {'User-agent': 'beep boop bot'})

# print(resp.content)
soup = BeautifulSoup(resp.content, "html.parser")
# print(content)
headlines = soup.find_all(class_="titles")
# print(headlines[0].parent)

articles = []

for i, art in enumerate(headlines):
    article = {}
    article['title'] = art.find(['h2','h3']).text
    # article['text'] = art.find(['p'])
    # print(article['title'] if article['title'] else art)
    try:
        article['link'] = art['href']
    except:
        # print(art.parent)
        article['link'] = art.parent['href']
    articles.append(article)

    
    driver.get(article['link'])

    # page = BeautifulSoup(driver.page_source, 'html.parser')

    # print(article['link'])
    # print(page)

    html = driver.page_source
    page = Article(article['link'])
    page.download(input_html=html)
    page.parse()

    # print(page.title)
    # print(page.text)

    article['text'] = page.text
    
    articles.append(article)


pprint(articles)

driver.quit()

with open("test_X.txt", 'w') as infile:
    infile.writelines([json.dumps(d) + "\n" for d in articles])