import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


class Crawler:

    months_correlatives = {"Jan": "1", "Feb": "2", "Mar":"3", "Apr":"4", "May":"5",
                          "Jun": "6", "Jul": "7", "Aug": "8", "Sep": "9", "Oct": "10",
                          "Nov": "11", "Dec": "12"}

    basic_url = "https://sofifa.com/players?offset="

    detailed_url = "https://sofifa.com/player/"


    basic_columns = ["ID", "Name", "Age", "Nationality", "Overall Rating", "Potential", "Team", "Value", "Wage Value", "Total Stats"]
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
                    "Penalties", "Composure", "Defensive Awareness", "Marking", "Standing Tackle","Sliding Tackle", 
                    "GK Diving", "GK Handling", "GK Kicking","GK Positioning", "GK Reflexes", "ID"]

    def Basic_Crawler(self, basic_data_filename):
        self.basic_data = pd.DataFrame(columns = self.basic_columns)

        for offset in range(0, 327):
            url = self.basic_url +str(offset*61)
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
                player_data.columns = self.basic_columns
                self.basic_data = self.basic_data.append(player_data, ignore_index = True)


        self.basic_data = self.basic_data.drop_duplicates()
        self.basic_data.to_csv("../Data/"+str(basic_data_filename), encoding = "utf-8")

    def Create_Detailed_DataFrame(self, basic_data_filename):
        self.detailed_data = pd.DataFrame(index = range(0, self.basic_data.count()[0]), columns = self.detailed_columns)
        self.detailed_data.ID = self.basic_data.ID

    def Detailed_Crawler(self, detailed_data_filename):
        for id in self.detailed_data.ID:
            full_player_url = self.detailed_url + str(id)
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
            skill_set["Birth Date"] = self.months_correlatives[month] + '/'+ day + '/' + year
            
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
            if(len(lis) != 0): #Player have current team
                if(len(lis) > 1):
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
                        skill_set[label] = self.months_correlatives[value[0]] + '/' + value[1].split(',')[0] + '/' +value[2]
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
                self.detailed_data.loc[self.detailed_data.ID == id, key] = value

        self.detailed_data.to_csv("../Data/" + str(detailed_data_filename), encoding = "utf-8")

    
    def Merge_Data(self, full_data_filename):
        self.full_data = pd.merge(self.basic_data, self.detailed_data, how = "inner", on = "ID")
        self.full_data.to_csv("../Data/" + str(full_data_filename), encoding = "utf-8")


    def Update_Data(self, basic_data_filename, detailed_data_filename, full_data_filename):
        print(basic_data_filename)
        self.Basic_Crawler(basic_data_filename)
        self.Create_Detailed_DataFrame(basic_data_filename)
        print(detailed_data_filename)
        self.Detailed_Crawler(detailed_data_filename)
        print(full_data_filename)
        self.Merge_Data(full_data_filename)


