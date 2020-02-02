import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Getting basic information from players

basic_columns = ["ID", "Name", "Age", "Nationality", "Overall Rating", "Potential", "Team", "Value", "Wage Value", "Total Stats"]
data_csv = pd.read_csv('../Data/basic_data.csv')
basic_data = pd.DataFrame(data_csv,columns = basic_columns)

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

data_csv = pd.read_csv('../Data/detailed_data.csv')

detailed_data = pd.DataFrame(data_csv, columns = detailed_columns)

full_data = pd.merge(basic_data, detailed_data, how = 'inner', on = 'ID')
full_data.to_csv('../Data/full_data.csv', encoding = "utf-8")
