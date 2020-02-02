import pandas as pd
import re
import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://sofifa.com/players?offset="
columns = ["ID", "Name", "Age", "Nationality", "Overall Rating", "Potential", "Team", "Value", "Wage Value", "Total Stats"]
data = pd.DataFrame(columns = columns)

for offset in range(0, 327):
    url = base_url +str(offset*61)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    tbody = soup.find('tbody')
    for tr in tbody.find_all('tr'):
        td = tr.find_all('td')
        Player_ID = td[0].find('img').get('id')
        name = td[1].find_all('a')[1].text
        age = td[2].text
        Nationality = td[1].find_all('a')[0].get('title')
        Ova =  td[3].text
        Potential = td[4].text
        Team = td[5].find('a').text
        Value = td[6].text
        Wage = td[7].text
        tstats =  td[8].text
        player_data = pd.DataFrame([[Player_ID, name, age, Nationality, Ova, Potential, Team, Value, Wage, tstats]])
        player_data.columns = columns
        data = data.append(player_data, ignore_index = True)


data = data.drop_duplicates()
data.to_csv('../Data/basic_data.csv', encoding = "utf-8")