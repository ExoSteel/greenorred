import cloudscraper, json, os

def getFearAndGreed():
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        
        url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        response = scraper.get(url)
        json_data = response.json()
        
        # print(json_data)
        return json_data # Dictionary
        
    except Exception as e:
        print(f"Error fetching data: {e}")

def saveFearAndGreed(data):
    if not os.path.exists("./others"):
        os.makedirs("./others")

    with open("./others/fear_and_greed.json", "wt", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    data = getFearAndGreed()
    saveFearAndGreed(data)