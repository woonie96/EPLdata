import requests

s = requests.Session()
s.get("https://www.premierleague.com/players")
print(s.cookies)