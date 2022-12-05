# -*- coding: utf-8 -*-
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from lxml.html import fromstring
import requests
from itertools import cycle

chrome_options = webdriver.ChromeOptions()
proxy = "145.239.121.218:3129"
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--proxy-server=%s' % proxy)

base_url = "https://translate.google.com/#view=home&op=translate&sl=auto&tl=en&text="
spacy_langs = ["DA", "NL", "EN", "FR", "DE", "EL", "IT", "LT", "PL", "PT","RO", "ES"]

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def foreign2en(sdescr):
    final_url = base_url + sdescr
    driver.get(final_url)

    xpath_from = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]/span[1]'

    #https://riptutorial.com/selenium/example/23375/explicit-wait-in-python
    element = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath_from)))
    print("{}\n:\n{}".format(sdescr, element.text))
    return element.text

def create_webdriver(proxy_pool, change_proxy=False):
    if change_proxy:
        proxy = next(proxy_pool)
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    return webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)

if __name__ == "__main__":
    df = pd.read_csv("datasets/descriptions/descriptions_w_trans_multi_translated.csv")

    length = df.shape[0]

    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    print(proxies)

    driver = create_webdriver(proxy_pool)

    count = 0
    for idx, row in df.iterrows():
        # Translate all rows which their tranlations are in "translation" or their tranlations are Nan
        if (str(row["TRANSLATION"]).lower() == "translation") or (type(row["TRANSLATION"]) == float):
            # No need to translate if there is not any description nor description's language not in spacy lang models
            if (type(row["SHORT_DESCR"]) != float) or (row["SELECTED_ORIG_x"] not in spacy_langs):
                count += 1
                try:
                    df.loc[idx, "TRANSLATION"] = foreign2en(row["SHORT_DESCR"])
                except:
                    driver.close()
                    driver.quit()
                    driver = create_webdriver(proxy_pool)

                # Control
                empties_s = df.TRANSLATION.isna().sum()
                print("{} out of {} in translations {} out of {} in total".format(count, empties_s, idx, length))

        # Take flash at each 1000th sample
        if (idx != 0) and (idx % 1000 == 0):
            df.to_csv("datasets/descriptions/descriptions_w_trans_multi_translated.csv")






