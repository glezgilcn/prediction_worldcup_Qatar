import pandas as pd

df_data_historica = pd.read_csv('fifa_worldcup_historical_data.csv')
df_fixture = pd.read_csv('fifa_worldcup_fixture.csv')
df_missing_data = pd.read_csv('fifa_worldcup_missing_data.csv')

#Clean df_fixture
df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

#Clean df_missing_data
df_missing_data = df_missing_data.dropna(inplace=True)

#Merge  df_missing_data and df_data_historica
df_data_historica = pd.concat([df_data_historica, df_missing_data], ignore_index=True)
df_data_historica.drop_duplicates(inplace=True)
df_data_historica.sort_values('year', inplace=True)


#Clean df_data_historica
index_eliminar = df_data_historica[df_data_historica['home'].str.contains('Sweden') &
                        df_data_historica['away'].str.contains('Austria')].index
df_data_historica.drop(index = index_eliminar, inplace = True)

df_data_historica['score'] = df_data_historica['score'].str.replace('[^\d–]', '', regex=True)
df_data_historica['score'] = df_data_historica['score'].str.replace('–', '-', regex=True)

df_data_historica['home'] = df_data_historica['home'].str.strip()
df_data_historica['away'] = df_data_historica['away'].str.strip()

df_data_historica[['HomeGoals', 'AwayGoals']] = df_data_historica['score'].str.split('-', expand=True)
df_data_historica.drop('score', axis = 1, inplace = True)
df_data_historica.rename(columns={'home':'HomeTeam', 'away':'AwayTeam', 'year':'Year'}, inplace=True)

df_data_historica = df_data_historica.astype({'HomeGoals':int, 'AwayGoals':int})
df_data_historica['TotalGoals'] = df_data_historica['HomeGoals'] + df_data_historica['AwayGoals']

#Export dataframes
df_data_historica.to_csv('clean_fifa_worldcup_historical_data.csv', index = False)
df_fixture.to_csv('clean_fifa_worldcup_fixture.csv', index = False)