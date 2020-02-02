import pandas as pd
import re
import csv
import requests
from bs4 import BeautifulSoup

months_correlatives = {"Jan": "1", "Feb": "2", "Mar":"3", "Apr":"4", "May":"5",
                          "Jun": "6", "Jul": "7", "Aug": "8", "Sep": "9", "Oct": "10",
                          "Nov": "11", "Dec": "12"}

data_csv = pd.read_csv('../Data/basic_data.csv')
data = pd.DataFrame(data_csv, columns = columns)

player_url = 'https://sofifa.com/player/'
detailed_columns = ["Full Name", "Birth Date", "Height", "Weight", "Position #1", "Position #2", 
                    "Preferred Foot", "International Reputation", "Weak Foot", "Skill Moves","Work Rate", "Body Type", "Real Face", "Release Clause",
                    "Current Team", "Jersey Number", "Joined","Contract Valid Until", 
                    "LS", "ST", "RS", "LW", "LF", "CF", "RF", "RW", "LAM", "CAM", "RAM", "LM", "LCM", "CM", "RCM", 
                    "RM", "LWB", "LDM", "CDM", "RDM", "RWB", "LB", "LCB", "CB", "RCB", "RB",                    
                    "Crossing", "Finishing", "Heading Accuracy", "Short Passing", "Volleys", 
                    "Dribbling", "Curve", "FK Accuracy", "Long Passing", "Ball Control", 
                    "Acceleration", "Sprint Speed", "Agility","Reactions", "Balance", 
                    "Shot Power", "Jumping", "Stamina", "Strength", "Long Shots", 
                    "Aggression", "Interceptions", "Positioning", "Vision",
                    "Penalties", "Composure", "Defensive Awareness", "Standing Tackle","Sliding Tackle", 
                    "GK Diving", "GK Handling", "GK Kicking","GK Positioning", "GK Reflexes", "ID"]
detailed_data = pd.DataFrame(index = range(0, data.count()[0]), columns = detailed_columns)
detailed_data.ID = data.ID

for id in detailed_data.ID:
    print(id)
    full_player_url = player_url + str(id)
    source_code = requests.get(full_player_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    skill_set = {}

    article = soup.find('article')
    meta_data = article.find('div', {'class': 'meta'})
    
    # Basic Data
    
    skill_set["Full Name"] = meta_data.text.split('  ')[0]
    
    # POSITIONS
    positions = meta_data.find_all('span', class_ = "pos")
    skill_set["Position #1"] = positions[0].text
    if(len(positions) > 1):
        skill_set["Position #2"] = positions[1].text
    else:
        skill_set["Position #2"] = None
    
    
    meta_data = meta_data.text.split(' ')
    length = len(meta_data)
    
    # BIRTH DATE
    year = meta_data[length- 3].split(')')[0]
    day = meta_data[length-4].split(',')[0]
    month = meta_data[length -5].split('(')[1]
    skill_set["Birth Date"] = months_correlatives[month] + '/'+ day + '/' + year
     
    # WEIGHT AND HEIGHT
    weight = meta_data[length - 1]
    height = meta_data[length - 2]
    skill_set["Weight"] = weight
    skill_set["Height"] = height
    
    
    
    teams = article.find('div', class_ = "teams")
    lis = teams.find('div', class_ = 'column col-6' ).find_all('li')
    for li in lis:
        label = li.find('label').text
        value = li.text.replace(label, '').strip()
        skill_set[label] = value
    lis = teams.find_all('div', class_ = 'column col-5' )
    
    # Informations about the player at current team
    if(len(lis) == 0): #Player doesn't have current team
        if(len(lis[0].find_all('li')) == 0):
            lis = lis[1].find_all('li')
        else:
            lis = lis[0].find_all('li')


        skill_set["Current Team"] = lis[0].text

        for li in lis[3:]:
            label = li.find('label').text
            value = li.text.replace(label, '').strip()
            if(label == "Joined"):
                value = value.split(' ')
                skill_set[label] = months_correlatives[value[0]] + '/' + value[1].split(',')[0] + '/' +value[2]
            else:
                skill_set[label] = value
    
    # Skill Set
    columns = article.find_all('div', class_ = "columns spacing")
    for column in columns:
        lis = column.find_all('li')
        for li in lis:
            value = re.findall(r'\d+', li.text)
            if(value == []):
                break
            value = int(value[0])
            label = filter(None, re.split('[^a-zA-Z]*', li.text))
            label = ' '.join(label)
            
            skill_set[str(label)] = value
    
    if(skill_set["Position #1"] != "GK"):
        # ASIDE INFORMATION
        aside_information = soup.find('aside').find('div', class_ = "bp3-callout spacing calculated").find_all('div', class_ = "columns")
        for col in aside_information:
            divs = col.find_all('div', class_ = "column")
            for div in divs:
                if(div.find('div') != None):
                    label = div.find('div').text
                    value = div.text.replace(label, '').strip()
                    skill_set[label] = value
    
    for key, value in skill_set.items():
        detailed_data.loc[detailed_data.ID == id, key] = value
    

detailed_data.to_csv('../Data/detailed_data.csv', encoding = "utf-8")

