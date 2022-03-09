from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import os
from selenium.webdriver.common.by import By
import time
from main import cookie_ad, to_csv
import os
import json

url = "https://www.premierleague.com/results"

def match_parsing(driver,url):
    response = requests.get(url)
    #time.sleep(6)

    if response.status_code == 200:

        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        #html = response.text
        soup = BeautifulSoup(html,'html.parser')
        match = soup.find_all('ul',class_='matchList')
        print(match)

    else:
        print(response.status_code)

def read_csv(csv):
    data = pd.read_csv(csv)
    return data

if __name__ == "__main__":
    #driver = webdriver.Chrome(executable_path='chromedriver.exe')
    #match_parsing(driver,url)
    files = os.listdir("player_link")

    csv_file = read_csv("player_csv\\Max Aarons\\Max Aarons_274.csv")
    for line in csv_file:
        print(line)
   # print(csv_file)
    test = "https://www.premierleague.com/players/4183/Ahmed-El-Mohamady/stats?co=1&se=363"
    #print(test.split("/")[4])
    #driver.close()