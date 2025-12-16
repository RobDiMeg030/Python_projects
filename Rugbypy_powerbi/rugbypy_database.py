from rugbypy.team import *
from rugbypy.match import *
import pandas as pd
from rugbypy.player import *



# 1. Zeitraum festlegen (z. B. ganze Saison 2023)
dates = pd.date_range(start="2023-01-01", end="2023-01-31", freq="D")

# 2. get matches
all_matches = pd.DataFrame()
for d in dates:
    date_str = d.strftime("%Y%m%d")  # rugbypy erwartet YYYYMMDD
    matches = fetch_matches(date_str)
    all_matches = all_matches._append(matches)

#convert matches to csv
all_matches.to_csv("all_matches.csv",index=False)

#make the matche_id as a parameter
matchid=all_matches["match_id"]
#get the team_id and name as a dataframe and csv
team=all_matches[["home_team_id","home_team"]].drop_duplicates()
team.to_csv("team.csv",index=False)

#generate team team_stats
team_stats = pd.DataFrame()
for t in team["home_team"]:
    stats=fetch_team_stats(t)
    team_stats=team_stats._append(stats)

team_stats.to_csv("team_stats.csv",index=False)

#generate matche_stats
all_matches_stats = pd.DataFrame()
for a in matchid:
    match_str =str(a)
    temp=fetch_match_details(a)
    all_matches_stats = all_matches_stats._append(temp)

all_matches_stats.to_csv("all_matches_stats.csv",index=False)

#get competiton data
competition=all_matches_stats[["competition_id","competition"]].drop_duplicates()
competition.to_csv("competition.csv",index=False)

#get player data
player_manifest = fetch_all_players()
player_manifest.to_csv("players.csv",index=False)


