## Obtains historical weather data from www.wunderground.com
## for the specified airport code, start date and end date
## In addition, downloads corresponding HTML files

from datetime import datetime, timedelta

## --------------- SETTINGS ---------------

AIRPORT_CODE = "CAI"
START_DATE = datetime(2019, 5, 11)
END_DATE = datetime(2019, 5, 11) + timedelta(days=1)

## ----------------------------------------

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
# import requests
# from urllib.request import Request, urlopen

import time
import pandas as pd
import os


lookup_url = "http://www.wunderground.com/history/daily/{}/date/{}-{}-{}"

if not os.path.isdir("./wunder_html"):
    os.mkdir("./wunder_html")
if not os.path.isdir("./wunder_csv"):
    os.mkdir("./wunder_csv")

cur_date = START_DATE
while cur_date != END_DATE:

    ## get starting time
    start_time = time.time()
    ## output current day
    print(str(cur_date) + " " + AIRPORT_CODE)

    ## check if file already exists
    if os.path.exists("./wunder_csv/{}_{}-{}-{}.csv".format(AIRPORT_CODE, cur_date.year, cur_date.month, cur_date.day)):
        print("--- file already exists ---")
        cur_date += timedelta(days=1)
        continue

    url = lookup_url.format(AIRPORT_CODE, cur_date.year,
                            cur_date.month, cur_date.day)

    bi = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=bi)

    ## This starts an instance of Firefox at the specified URL:
    driver.get(url)

    tables = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))

    table = pd.read_html(tables[-1].get_attribute('outerHTML'))
    table = table[0]
    table.to_csv("./wunder_csv/{}_{}-{}-{}.csv".format(AIRPORT_CODE, cur_date.year,
                                                       cur_date.month, cur_date.day))
    # ind =  0
    # for table in tables:
    #     newTable = pd.read_html(table.get_attribute('outerHTML'))
    #     print("TABLE {}:\n".format(ind))
    #     ind += 1
    #     jnd = 0
    #     for haga in newTable:
    #         print(type(haga))
    #         print("HAGA {}:\n".format(jnd))
    #         print(haga)
    #         jnd += 1
    #     if newTable:
    #         print(newTable[0].fillna(''))

    html = driver.page_source
    driver.quit()

    # html = requests.get(url)
    # req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
    # html = urlopen(req).read().decode("utf-8")
    # print(html)

    outfile_name = "wunder_html/{}_{}-{}-{}.html".format(AIRPORT_CODE, cur_date.year,
                                                         cur_date.month, cur_date.day)

    with open(outfile_name, 'w', encoding="utf-8") as out_file:
        out_file.write(html)

    cur_date += timedelta(days=1)
    ## output elapsed seconds
    print("--- %s seconds ---\n" % round(time.time() - start_time, 2))
