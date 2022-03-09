import pandas as pd
import time
import os
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
        #driver.implicitly_wait(10)
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

def player_parse(driver,url,team_id,team_name):

    driver.get(url)
    out_dir = os.path.join(os.getcwd() , "player_link")
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    #cookie_ad(driver)
    scroll(driver,2)
    #time.sleep(3)
    players = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody')
    player_name = players.find_elements(By.TAG_NAME, 'a')
    player = []
    now = time.localtime()
    print(team_name+" Parsing done"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    for i in player_name:
        link = str(i.get_attribute('href'))
        link = link.replace("/overview","/stats?co=1&se=-1")
        player_id = link.split("/")[4]
        player.append([player_id,i.text,link,team_id])
    now = time.localtime()
    print(team_name+" List complete"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    file_name = team_name+".csv"

    to_csv(player,os.path.join(out_dir, file_name))


def to_csv(list_name,csv_name):
    #file = open(csv_name, 'w', newline='', encoding='utf-16')
    dataframe = pd.DataFrame(list_name)
    dataframe.to_csv(csv_name, index=False)


def choose_seaseon(driver,url):
    #driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.set_window_size(1920, 1024)

    driver.get(url)
    cookie_ad(driver)

    driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[2]/div[1]/div/section/div[1]/div[2]').click()

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    drop_down = soup.find_all('ul',class_='dropdownList')[0] # 0 for season id 1 for club id
    season_id =[]
    for line in drop_down:
        try:
            season_id.append([line['data-option-id'],line['data-option-name']])
        except:
            pass
    return season_id

def team(driver,url):
    driver.get(url)
    driver.set_window_size(1920, 1024)
    time.sleep(5)
    cookie_ad(driver)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/div/section/div[2]/div[2]').click()
    html = driver.page_source
    # html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    drop_down = soup.find_all('ul', class_='dropdownList')[1]
    team_id = []
    for line in drop_down:
        try:
            if(int(line['data-option-id']) > 0):
                team_id.append([line['data-option-id'], line['data-option-name']])
            else:
                pass
        except:
            pass

    return team_id
def parse_player_by_team(driver, url, teams):
    for line in teams:

        team_url = url+"?&cl="+line[0]
        #print(url)
        player_parse(driver,team_url,line[0],line[1])
def player_parse_test(driver,site):

    driver.get(url=site)

    #cookie_ad(driver)
    scroll(driver,1)
    players = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody')
    player_name = players.find_elements(By.TAG_NAME, 'a')
    player = []
    now = time.localtime()
    print("Parsing done"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    for i in player_name:
        link = str(i.get_attribute('href'))
        link = link.replace("/overview","/stats?co=1&se=-1")
        player_id = link.split("/")[4]
        player.append([player_id,i.text,link])
    now = time.localtime()
    print("List complete"+" "+"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))



    return player
if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.set_window_size(1920, 1024)
    url = "https://www.premierleague.com/players"
    #cookie_ad(driver)
    # session_id = choose_seaseon(driver, url)
    #teams = team(driver,url)
    #parse_player_by_team(driver,url,teams)
    # test_url = "https://www.premierleague.com/players?cl=1"
    # player_parse(driver,test_url,1,"Arsenal")

    driver.close()

    # to_csv(session_id,"session.csv")
    #to_csv(teams, "teams.csv")
