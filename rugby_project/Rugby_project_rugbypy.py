from rugbypy.match import *
import csv
import matplotlib.pyplot as plt
import pandas as pd


from datetime import datetime, timedelta

'''
start_date = datetime(2025, 1, 1)
end_date=datetime(2025, 1, 31)
#end_date = datetime.now()
df=pd.DataFrame()
for i in range((end_date - start_date).days + 1):
    current_date = start_date + timedelta(days=i)
    date_str = current_date.strftime("%Y%m%d")
    match = fetch_matches(date_str)
    df = pd.concat([df, match], ignore_index=True)

    #all_matches.append(match)



df.to_csv("rugbymatches.csv", index=False, encoding="utf-8")
'''
ben_df=fetch_match_details(team_id="25927")
ben_df.to_csv("benetton.csv", index=False, encoding="utf-8")


