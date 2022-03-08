from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.by import By
import time
from main import cookie_ad, to_csv
import os
import json



def match_parsing(driver,url):
    response = requests.get(url)
    #time.sleep(6)

    if response.status_code == 200:

        driver.get(url)
        cookie_ad(driver)
        html = driver.page_source
        #html = response.text
        soup = BeautifulSoup(html,'html.parser')

        match = soup.find_all('li', class_='matchFixtureContainer')
        matches = []
        for line in match:
            local_time = datetime.fromtimestamp(int(line['data-comp-match-item-ko'])/1000)
            #print(line['data-home']+" VS "+line['data-away']+" at "+str(local_time))
            matches.append([line['data-home'],line['data-away'],local_time])

    else:
        print(response.status_code)

    return matches


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    url_match = "https://www.premierleague.com/results"
    url_player = "https://www.premierleague.com/players"
    now = datetime.now()
    #matches = match_parsing(driver, url_match)
    #print(now.day)
    # for line in matches:
    #     match_time = line[2]
    #     time_gap = now.day - line[2].day
    #     if(time_gap >0 and time_gap <2):
    #         print(line)

    driver.close()