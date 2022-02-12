from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
from main import cookie_ad



def player_parsing(url):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        sum = soup.find_all('span', 'stat')

        summary_info = []
        for i in sum :
            try:
                data_stat = i.contents[0].replace(' ','')
                data = i.find('span').contents[0].replace(' ','').replace('\n','')
                summary_info.append([data_stat, data])
            except:
                pass

        return summary_info
    else:
        print(response.status_code)

def read_csv():
    data = pd.read_csv('player.csv')
    link = data.values

    return link[1][1]

def choose_seaseon(url):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1920, 1024)
    driver.get(url)
    cookie_ad(driver)

    driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div/div/div[2]/div/div/section/div[2]/div[2]').click()

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    drop_down = soup.find_all('ul',class_='dropdownList')[1]
    season_id =[]
    for line in drop_down:
        try:
            season_id.append([line['data-option-id'],line['data-option-name']])
        except:
            pass
    return season_id

if __name__ == "__main__":
    player_link = read_csv()

    for line in player_parsing(player_link):
        print(line)

