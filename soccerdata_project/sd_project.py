'''
import soccerdata as sd
import pandas as pd

# Scraper für Bundesliga und gewünschte Saisons erstellen
fbref = sd.FBref(leagues=['GER-Bundesliga'], seasons=['1920', '2021', '2122', '2223'])

stats=pd.DataFrame(fbref)
hertha_stats = stats[stats['team'] == 'Hertha BSC']

# Team-Statistiken abrufen (z. B. Schussstatistiken)
season_stats = fbref.read_team_season_stats(stat_type='standard')

season_stats.columns = ['_'.join(col) if isinstance(col, tuple) else col for col in season_stats.columns]
#print(season_stats.columns)

# Nur Hertha BSC herausfiltern
#


# Ergebnis anzeigen
print(season_stats.head())
'''

import soccerdata as sd

# Bundesliga-Saison 2022/23
fbref = sd.FBref(leagues="GER-Bundesliga", seasons="2223")

# Alle Teamstatistiken laden
team_stats = fbref.read_team_match_stats()

# Hertha BSC herausfiltern
hertha_stats = team_stats.loc[team_stats.index.get_level_values("team") == "Hertha BSC"]

# Ausgabe
print(hertha_stats.head())
