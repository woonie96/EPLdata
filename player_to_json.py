from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
from main import cookie_ad



def player_parsing(url,session):
    response = requests.get(url)
    print(url)
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

def read_csv(csv_name):
    data = pd.read_csv(csv_name)
    link = data.values

    return link[1][1]



if __name__ == "__main__":
    player = read_csv("player.csv")
    for line in player_parsing(player,1):
        print(line)

