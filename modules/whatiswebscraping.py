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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

with open("tickers.txt", "rt") as infile:
    data = infile.readlines()
    quotes = [d.strip("\n") for d in data]

driver = webdriver.Chrome(options=chrome_options)

url = "https://sg.finance.yahoo.com/quote/"

# https://www.cnbc.com/finance/
# https://www.reuters.com/business/finance/
# https://news.google.com/search?q=

for quote in quotes:
    print(f"Quote {quote} Started.")
    url = url + quote + "/news/"
    resp = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(resp.content, "html.parser")

    with open(".txt", 'wt') as infile:
        infile.write(resp.content.decode('utf-8'))
    break
    # headlines = soup.find_all(class_="titles")
    # # print(headlines[0].parent)

    # articles = []

    # for i, art in enumerate(headlines):
    #     article = {}
    #     article['title'] = art.find(['h2','h3']).text
    #     # article['text'] = art.find(['p'])
    #     # print(article['title'] if article['title'] else art)
    #     try:
    #         article['link'] = art['href']
    #     except:
    #         # print(art.parent)
    #         article['link'] = art.parent['href']
    #     articles.append(article)

        
    #     driver.get(article['link'])

    #     # page = BeautifulSoup(driver.page_source, 'html.parser')

    #     # print(article['link'])
    #     # print(page)

    #     html = driver.page_source
    #     page = Article(article['link'])
    #     page.download(input_html=html)
    #     page.parse()

    #     # print(page.title)
    #     # print(page.text)

    #     article['text'] = page.text
        
    #     articles.append(article)



    # pprint(articles)

    # driver.quit()

    # with open(f"news_{quote}.txt", 'w') as infile:
    #     infile.writelines([json.dumps(d) + "\n" for d in articles])

    # print(f"Quote {quote} Finished.")
    # print()