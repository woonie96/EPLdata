import pandas as pd
import time
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import requests
import urllib.request
import re



def scroll(driver,timeout):
    scroll_pause_time = timeout

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def cookie_ad(driver):

    try:
        driver.implicitly_wait(10)
        now = time.localtime()
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[5]/button[1]').click() #cookie button
        print("cookies accepted"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    except:
        print("no cookies")
    try:
        driver.find_element(By.XPATH, '//*[@id="advertClose"]').click() #popup button
    except:
        now = time.localtime()
        print("No ad"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

def player_parse(driver,site):

    driver.get(url=site)

    cookie_ad(driver)
    scroll(driver,5)
    players = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody')
    player_name = players.find_elements(By.TAG_NAME, 'a')
    player = []
    now = time.localtime()
    print("Parsing done"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    for i in player_name:
        link = str(i.get_attribute('href'))
        link = link.replace("/overview","/stats")
        player.append([i.text,link])
    now = time.localtime()
    print("List complete"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    driver.close()


    return player

def to_csv(player_name):
    #file = open('player.csv', 'w', newline='', encoding='utf-16')
    dataframe = pd.DataFrame(player_name)
    dataframe.to_csv("player.csv", header=False, index=False)

def read_csv():
    data = pd.read_csv('player.csv')
    link = data.values
    print(link[1][1])



if __name__ == "__main__":
    #driver = webdriver.Chrome(executable_path='chromedriver.exe')
    url = "https://www.premierleague.com/players"
    #print(player_parse(url)[794]) # son heung - min 779
    #print(player_parse(url)[794])
    #print(player_parse(driver,url))
    #player_list = player_parse(driver,url)
    #to_csv(player_list)
    read_csv()
