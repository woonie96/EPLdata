from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
from main import cookie_ad, to_csv
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
        #stats_index = []
        summary_info = []
        for i in sum :
            try:
                data_stat = i.contents[0].replace(' ','')
                data = i.find('span').contents[0].replace(' ','').replace('\n','')
                summary_info.append(data)
                #stats_index.append(data_stat)
            except:
                pass
        player_id = url.split("/")[4]
        summary_info.append(player_id)
        #stats_index.append()
        return summary_info, #stats_index
    else:
        print(response.status_code)

def read_csv(csv_name):
    data = pd.read_csv(csv_name)
    link = data.values

    return link

def session_link(url, session_id, number):
    url = url.replace(url.split("=")[2], str(session_id[number][0]))

    return url

def parse_all_player(number,players,session_id):
    session_id_number = len(session_id)
    init_url = players[number][1]
    player_name = players[number][0]

    out_dir = os.path.join(os.getcwd()+"\\player_csv",player_name)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    print("--------- Name is "+player_name+" ---------")
    print(player_parsing(driver, init_url))
    total_apperance = player_parsing(driver, init_url)[0]
    for one in range(session_id_number):

        url = session_link(init_url, session_id, one)
        current_apperance = player_parsing(driver, url)[0]
        if str(total_apperance) == "0":
            print("--------- Parsing is done ---------")
            break
        elif str(current_apperance) == "0":
            pass
        else:
            print("In "+session_id[one][1])
            print(player_parsing(driver, url))
            file_name = player_name+"_"+str(session_id[one][0])+".csv"
            to_csv(player_parsing(driver, url), os.path.join(out_dir, file_name))
        total_apperance = int(total_apperance) - int(current_apperance)

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

def parse_all_player_test(session_id):
    session_id_number = len(session_id)
    init_url =" https://www.premierleague.com/players/19970/Max-Aarons/stats?co=1&se=-1"
    player_name = "Max Aarons_test"

    out_dir = os.path.join(os.getcwd()+"\\player_csv",player_name)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    print("--------- Name is "+player_name+" ---------")
    print(player_parsing(driver, init_url))
    total_apperance = player_parsing(driver, init_url)[0][0]
    print(total_apperance)
    for one in range(session_id_number):

        url = session_link(init_url, session_id, one)
        current_apperance = player_parsing(driver, url)[0][0]
        print(current_apperance)
        if str(total_apperance) == "0":
            print("--------- Parsing is done ---------")
            break
        elif str(current_apperance) == "0":
            pass
        else:
            print("In "+session_id[one][1])
            print(player_parsing(driver, url))
            file_name = player_name+"_"+str(session_id[one][0])+".csv"
            to_csv(player_parsing(driver, url), os.path.join(out_dir, file_name))
        total_apperance = int(total_apperance) - int(current_apperance)

if __name__ == "__main__":
    players = read_csv("player_test.csv")
    session_id = read_csv("session.csv")
    #test_url = "https://www.premierleague.com/players/19970/Max-Aarons/stats?co=1&se=418"
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    number_of_player = len(players)

    # for one in range(number_of_player):
    #     parse_all_player(one,players,session_id)
    parse_all_player_test(session_id)

    #print(session_id[0][0])
    # for one in range(number_of_player):
    #     parse_this_ss(one,players,session_id)

    driver.close()