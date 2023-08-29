from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

c = webdriver.ChromeOptions()
c.add_argument("--incognito")

service = Service(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service,options=c)

web = f'https://en.wikipedia.org/wiki/1990_FIFA_World_Cup'
driver.get(web)
matches = pd.DataFrame()
partidos = []
for i in range(7, 5*2+7, 2):
  tables = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[{i}]')
  matches = tables[0].text.split('\n')
  for m in matches:
    try:
      int(m[0])
    except:
      partidos.append(m)

matches = [p.split('Stadio')[0][:-1] for p in partidos]

home = []
score = []
away = []

for m in matches:
  auxi = m.split('–')
  home.append(auxi[0][:-3])
  away.append(auxi[1][3:])
  score.append(auxi[0][-1] + '-' + auxi[1][0])

dict_football = {'home': home, 'score': score, 'away': away}
df_football = pd.DataFrame(dict_football)
df_football['year'] = '1990'

fifa = [df_football]
driver.quit()

df_fifa = pd.concat(fifa, ignore_index = True)
df_fifa.to_csv('fifa_worldcup_missing_data.csv', index=False)

driver.close()