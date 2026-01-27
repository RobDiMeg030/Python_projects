from rugbypy.team import *
from rugbypy.match import *
import pandas as pd
from rugbypy.player import *



# 1. Zeitraum festlegen (z. B. ganze Saison 2023)
dates = pd.date_range(start="2022-01-01", end="2024-01-31", freq="D")

# 2. get matches
all_matches = pd.DataFrame()
for d in dates:
    date_str = d.strftime("%Y%m%d")  # rugbypy erwartet YYYYMMDD
    matches = fetch_matches(date_str)
    all_matches = all_matches._append(matches)

#convert matches to csv
all_matches.to_csv("all_matches.csv",index=False)

# create a team-match-bridge
team1 = all_matches[["match_id", "home_team_id"]].rename(columns={"home_team_id": "team_id"})
team1["home_away"] = "home"

team2 = all_matches[["match_id", "away_team_id"]].rename(columns={"away_team_id": "team_id"})
team2["home_away"] = "away"

tmb = pd.concat([team1, team2], ignore_index=True)

tmb.to_csv("team_match_bridge.csv",index=False)

#make the matche_id as a parameter
matchid=all_matches["match_id"]
#get the team_id and name as a dataframe and csv
team=all_matches[["home_team_id","home_team"]].drop_duplicates()
team.to_csv("team.csv",index=False)

#generate team team_stats
team_stats = pd.DataFrame()
for t in team["home_team_id"]:
    team_str=str(t)
    stats=fetch_team_stats(team_str)
    team_stats=team_stats._append(stats)
    
for col in team_stats.columns:
    if team_stats[col].dtype == object:
        if team_stats[col].str.contains(",", regex=False).any():
            team_stats[col] = (
                team_stats[col]
                .str.replace(",", ".", regex=False)
                .astype(float)
            )

team_stats.to_csv("team_stats.csv",index=False)

#generate matche_stats
all_matches_stats = pd.DataFrame()
for a in matchid:
    match_str =str(a)
    temp=fetch_match_details(match_str)
    all_matches_stats = all_matches_stats._append(temp)

all_matches_stats.to_csv("all_matches_stats.csv",index=False)

players_table=team_stats[["game_date","team_id","match_id","players"]]
df_players_table=players_table.explode("players")
df_players_table.to_csv("players_match.csv",index=False)

#get competiton data
competition=all_matches_stats[["competition_id","competition"]].drop_duplicates()
competition.to_csv("competition.csv",index=False)

#get player data
player_manifest = fetch_all_players()
player_manifest.to_csv("players.csv",index=False)

player_stats=pd.DataFrame()

for p in player_manifest["player_id"]:
    play_str=str(p)
    temp=fetch_player_stats(play_str)
    player_stats=player_stats._append(temp)

player_stats.to_csv("player_stats.csv",index=False)


