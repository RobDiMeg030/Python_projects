'''
The idea of this project is
predict the number tries, conversion goals and penalty goals
based on game performance

'''


from rugbypy.match import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_absolute_error, r2_score
from rugbypy.team import *
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#get all match from Benneton Treviso team_id=25927

ben_df=fetch_team_stats(team_id="25927")
#ben_df.to_csv("benetton.csv", index=False, encoding="utf-8")


target_cols = ["tries", "conversion_goals", "penalty_goals"]

feature_cols = [
    "meters_run", "defenders_beaten", "passes", "possession",
    "territory", "rucks_won", "lineouts_won", "mauls_won", "tackles",
    "missed_tackles","yellow_cards","scrums_won","clean_breaks","red_cards"
]
#comparison pearson & speraman correlation alogrith

results_pear = pd.DataFrame(
    {target: [ben_df[target].corr(ben_df[feature]) for feature in feature_cols]
     for target in target_cols},
    index=feature_cols)

results_spear = pd.DataFrame(
    {target: [ben_df[target].corr(ben_df[feature],method="spearman") for feature in feature_cols]
     for target in target_cols},
    index=feature_cols)


fig, axes = plt.subplots(1, 2, figsize=(16, 6))


sns.heatmap(results_pear, annot=True, cmap="coolwarm", center=0,ax=axes[0])
axes[0].set_title("Pearson-Korrelationen zwischen Features und Targets")
axes[0].set_ylabel("Features")
axes[0].set_xlabel("Targets")

sns.heatmap(results_spear, annot=True, cmap="coolwarm", center=0,ax=axes[1])
axes[1].set_title("Spearman-Korrelationen zwischen Features und Targets")
axes[1].set_ylabel("Features")
axes[1].set_xlabel("Targets")

plt.tight_layout()
plt.show()

#after that i chose my target and values

X= ben_df[["meters_run","defenders_beaten","clean_breaks","passes","possession"]]
X_2= ben_df[["meters_run","defenders_beaten","clean_breaks","passes","possession","tackles"]]
y = ben_df["tries"]

# 3. Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X2_train,X2_test = train_test_split(X_2, test_size=0.2, random_state=42)

# Build models and train
model=LinearRegression()
model.fit(X_train, y_train)

baum =RandomForestRegressor(random_state=42)
baum.fit(X2_train, y_train)

# 5. Vorhersagen treffen
y_pred = model.predict(X_test)
y_baum = baum.predict(X2_test)

# 6. Evaluation
print("Linear Regression")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R² :", r2_score(y_test, y_pred))

print("Random Forrest")
print("MAE:", mean_absolute_error(y_test, y_baum))
print("R² :", r2_score(y_test, y_baum))

#MAE - mean absolute error  smaller than better
#R² < 0 -> bad modell

''' conclusion: the linear regression is a better model than
random forrest
but maybe we should modify the model to get better result 
'''



