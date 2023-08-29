#Importar las librerias a usar
import pandas as pd
from string import ascii_uppercase as alfabeto
from bs4 import BeautifulSoup
import requests
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By

# Años de los mundiales a estudiar
years = [1930,1934, 1938, 1950, 1954, 1958, 1962, 1966,
         1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998,
         2002, 2006, 2010, 2014, 2018]

# Se scrappea la lista de los partidos para el mundial 'Qatar 2022'
# Grupos A -> H
# 12 -> 7*8+12 = 68

todas_tablas = pd.read_html('https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
dict_tablas = {}

for letra, i in zip(alfabeto, range(12, 68, 7)):
  df = todas_tablas[i]
  df.rename(columns={df.columns[1]: 'Team'}, inplace = True)
  df.pop('Qualification')
  dict_tablas[f'Grupo {letra}'] = df

with open('dict_table', 'wb') as output:
  pickle.dump(dict_tablas, output)

# La función scrappea los partidos jugados en el mundial enviado como parametro
# y los devuelve como dataframe que contiene home, score, away y year
def get_matches(year):

  web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
  response = requests.get(web)
  content = response.text
  soup = BeautifulSoup(content, 'lxml')

  matches = soup.find_all('div', class_='footballbox')

  home = []
  score = []
  away = []

  for match in matches:
    home.append(match.find('th', class_='fhome').get_text())
    score.append(match.find('th', class_='fscore').get_text())
    away.append(match.find('th', class_='faway').get_text())

  dict_football = {'home': home, 'score': score, 'away': away}
  df_football = pd.DataFrame(dict_football)
  df_football['year'] = year

  return df_football

# Se scrappean los partidos y se guardan en un historico
fifa = [get_matches(year) for year in years]
df_fifa = pd.concat(fifa, ignore_index = True)
df_fifa.to_csv('fifa_worldcup_historical_data.csv', index = False)

# Se scrappean los partidos del mundial de Qatar 2022
df_fixture = get_matches('2022')
df_fixture.to_csv('fifa_worldcup_fixture.csv', index = False)