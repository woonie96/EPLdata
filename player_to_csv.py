from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
from main import cookie_ad, to_csv, to_csv_index
import os
import json

def player_parsing(driver,url):
    response = requests.get(url)
    #time.sleep(6)

    if response.status_code == 200:

        driver.get(url)
        time.sleep(1.5)
        html = driver.page_source
        #html = response.text
        soup = BeautifulSoup(html,'html.parser')
        sum = soup.find_all('span', 'stat')
        stats_index = ["player_id"]
        data_list = []
        player_id = url.split("/")[4]
        data_list.append(player_id)
        for i in sum :
            try:
                data_stat = i.contents[0].replace(' ','')
                data = i.find('span').contents[0].replace(' ','').replace('\n','')
                data_list.append(data)

                stats_index.append(data_stat)

            except:
                pass



        return data_list, stats_index
    else:
        print(response.status_code)

def read_csv(csv_name):
    data = pd.read_csv(csv_name)
    link = data.values

    return link

def session_link(url, session_id, number):
    url = url.replace(url.split("=")[2], str(session_id[number][0]))

    return url


def parse_this_ss(number,players,session_id):
    init_url = players[number][1]
    player_name = players[number][0]
    out_dir = os.path.join(os.getcwd() + "\\player_csv", player_name)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    print("--------- Name is " + player_name + " ---------")
    #print(player_parsing(driver, init_url))
    url = session_link(init_url, session_id, 0)
    print(url)
    current_apperance = player_parsing(driver, url)[0][1]
    print("In " + session_id[0][1])
    print(player_parsing(driver, url))
    file_name = player_name + "_" + str(session_id[1][0]) + ".csv"
    to_csv(player_parsing(driver, url), os.path.join(out_dir, file_name))

def parse_all_player(number,players,session_id):
    session_id_number = len(session_id)
    init_url =players[number][1]
    player_name = players[number][0]

    out_dir = os.path.join(os.getcwd(),"player_csv")
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    print("--------- Name is "+player_name+" ---------")
    total_apperance = player_parsing(driver, init_url)[0][1]
    print("total apperance = "+total_apperance)
    summary_info =[]
    if str(total_apperance) == "0":
        summary_info.append(0)
    for one in range(session_id_number):
        url = session_link(init_url, session_id, one)
        stat_list = player_parsing(driver,url)[0]
        current_apperance = player_parsing(driver, url)[0][1]
        print("Current apperance: "+current_apperance)
        if str(total_apperance) == "0":
            print("--------- Parsing is done ---------")
            break
        elif str(current_apperance) == "0":
            pass
        else:
            stat_list.append(url.split("=")[2])
            summary_info.append(stat_list)

        total_apperance = int(total_apperance) - int(current_apperance)
    file_name = player_name + ".csv"
    to_csv(summary_info,os.path.join(out_dir, file_name))

if __name__ == "__main__":
    players = read_csv("player.csv")
    session_id = read_csv("session.csv")
    test_url = "https://www.premierleague.com/players/19970/Max-Aarons/stats?co=1&se=418"
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    number_of_player = len(players)

    for one in range(number_of_player):
        parse_all_player(one,players,session_id)

    driver.close()

    # csv_file = read_csv("player_csv\\Aaron Ramsey.csv")
    # for line in csv_file:
    #     print(line)

