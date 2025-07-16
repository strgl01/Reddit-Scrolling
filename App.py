from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import time
import random
import pandas as pd

headline=[]
source=[]

proxies=[
     "92.113.242.158:6742",
     "216.10.27.159:6837"]

proxy=random.choice(proxies)

custom_headers = {
        "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
        }

seleniumwire_options = {
        # 'request_storage_base_dir': 'requests',  # Optional: to store requests
        'custom_headers': custom_headers,
        'proxy': {
                'http': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'https': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'no_proxy': 'localhost,127.0.0.1'  # Exclude localhost
                }
        }

service = Service(geckodriver_path = r"C:/Users/dell/Downloads/geckodriver.exe")
options = Options()
        
driver = webdriver.Firefox(service=service, options=options, seleniumwire_options=seleniumwire_options)
print(proxy)
driver.get('https://www.reddit.com/t/business/')
time.sleep(10)

total_height = 0
distance = 15000
scroll_pause_time = 30
count=0

while True:
    count=count+1
    print(count)
    
    # Scroll down by the distance
    driver.execute_script("window.scrollBy(0, arguments[0]);", distance)

    soup = bs(driver.page_source, 'lxml')
    articles = soup.select('article[class="w-full m-0"]')
    for i in articles:
        if str(i['aria-label']).strip() in headline:
            continue
        headline.append(str(i['aria-label']).strip())
        try:
            source.append(i.find('video')['src'])
        except:
            if i.find('img', attrs={'class' : 'preview-img'}):
                source.append(i.find('img', attrs={'class' : 'preview-img'})['src'])
            else:
                source.append(None) 


    
    time.sleep(scroll_pause_time)  # Wait to load new content
        
    # Calculate the new scroll height and check if more content is loaded
    new_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if new_scroll_height == total_height:
        print('scrolling complete')
        break
    total_height = new_scroll_height


for i in articles:
    headline.append(str(i['aria-label']).strip())
    try:
        source.append(i.find('video')['src'])
    except:
        if i.find('img', attrs={'class' : 'preview-img'}):
            source.append(i.find('img', attrs={'class' : 'preview-img'})['src'])
        else:
            source.append(None) 

    

data= {'headline' : headline, 'source': source}
df = pd.DataFrame(data)
df.to_csv('output.csv')

driver.close()
