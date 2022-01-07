import datetime
import time
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import requests
import urllib.request
import re


def player_parse(site):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url=site)
    def doScrollDown(whileSeconds):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=whileSeconds)
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            if datetime.datetime.now() > end:
                break
    # 스크롤 높이 가져옴
    doScrollDown(15)
    players = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody')
    player_name = players.find_elements(By.TAG_NAME, 'a')

    player = []

    for i in player_name:
        link = i.get_attribute('href')
        player.append([i.text,link])

    return player
    #driver.close()

def player(url):
    html = urllib.request.urlopen(url)

    source = html.read()
    soup = BeautifulSoup(source, "html.parser")
    theaters = soup.find(class_="dataContainer indexSection").find_all("a")
    print(theaters[0].get_text())

if __name__ == "__main__":
    url = "https://www.premierleague.com/players"
    print(player_parse(url)[779]) # son heung - min
    #player(url)