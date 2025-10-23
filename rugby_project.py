

import kagglehub
import pandas as pd
import matplotlib.pyplot as plt


# Download latest version
path = kagglehub.dataset_download("lylebegbie/international-rugby-union-results-from-18712022")
#get the downlaoded data
print("Path to dataset files:", path)
new_path=path+"\\results.csv"
#create dataframe
rugby=pd.read_csv(new_path)

# spezifie the team
team='New Zealand'
rugby_team = rugby[(rugby['home_team'] == team) | (rugby['away_team'] == team)]

def get_match_stats_per_team(team):

    matches=len(rugby_team)
    wins=0
    losses=0
    draws=0
    points=0
    for _, i in rugby_team.iterrows():
        if team == i['home_team']:
            team_point=i['home_score']

            opponent_point=i['away_score']
        else:
            team_point = i['away_score']
            opponent_point = i['home_score']

        points+=team_point
        if team_point > opponent_point:
            wins+=1
        elif team_point < opponent_point:
            losses+=1
        else:
            draws+=1

    point_per_match=points/matches
    print("Stats of", team, " :  Matches:", matches, " Wins:", wins, " Losses:", losses, " Draws:", draws,
          "Average of Points per Match:", point_per_match)
    return 1


def last_5_matches(team):
    df=rugby_team.tail(5)
    fig, ax = plt.subplots()
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    plt.title(f"Last 5 Matches of {team}")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.show()

    return 1

def opp_stats(team):
    opponents = rugby_team.apply(
        lambda row: row['away_team'] if row['home_team'] == team else row['home_team'],
        axis=1)
    opp_counts = opponents.value_counts()

    labels = opp_counts.index.tolist()
    values = opp_counts.values.tolist()

    def show_absolute_values(pct):
        total = sum(values)
        absolute = int(round(pct * total / 100.0))
        return f"{absolute}"

    plt.pie(values, labels=labels, autopct=show_absolute_values)
    plt.title("Number of matches against which Team")
    plt.axis('equal')
    plt.show()
    return 1


ende=''


while ende.lower() !='n':
    option=""
    option=input("""What Information do you want to see?
            Options:
            a - Match Stats
            b - Last 5 Matches
            c - List Up how many Matches your team had against which Opponent
            Please Enter: """)
    if option == "a":
        get_match_stats_per_team(team)
    elif option == "b":
        last_5_matches(team)
    elif option ==  "c":
        opp_stats(team)
    else:
        print("Please enter a valid option.")
    ende=input("Do you want to continue? (y/n):")