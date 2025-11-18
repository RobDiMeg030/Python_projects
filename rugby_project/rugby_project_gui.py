

import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry


def wrap_by_words(text, words_per_line=4):
    if pd.isnull(text):
        return ''
    words = str(text).split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

def new_cathegory(competition):
    if pd.isnull(competition):
        return "Test Match"
    turnier=str(competition).lower()
    if "nations" in turnier:
        return "Six Nations"
    elif "Rugby Championship" in turnier:
        return "Rugby Championship"
    elif "world cup" in turnier:
        return "Rugby World Cup"
    else:
        return "Test Match"

# Download latest version
path = kagglehub.dataset_download("lylebegbie/international-rugby-union-results-from-18712022")
#get the downlaoded data
print("Path to dataset files:", path)
new_path=path+"\\results.csv"
#create dataframe
rugby=pd.read_csv(new_path)
rugby['Match Category'] = rugby['competition'].apply(new_cathegory)
rugby=rugby.drop(columns=['competition','neutral','country','world_cup'])
teams = sorted(set(rugby['home_team']).union(set(rugby['away_team'])))

# GUI-Funktion: Match-Stats für ausgewähltes Team
# GUI-Fenster
root = tk.Tk()
root.title("Rugby Team Report")
root.geometry("1200x800")
# Team-Auswahl
team_var = tk.StringVar()
team_dropdown = ttk.Combobox(root, textvariable=team_var, values=teams, state="readonly", width=30)
team_dropdown.set("Team auswählen")
team_dropdown.grid(row=0, column=0, padx=10, pady=10)

# Startdatum
start_label = tk.Label(root, text="Von:")
start_label.grid(row=0, column=1, padx=5, pady=10)
start_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
start_date.grid(row=0, column=2, padx=5, pady=10)

# Enddatum
end_label = tk.Label(root, text="Bis:")
end_label.grid(row=0, column=3, padx=5, pady=10)
end_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
end_date.grid(row=0, column=4, padx=5, pady=10)


# Beenden-Button
exit_button = tk.Button(root, text="Beenden", command=root.destroy)
exit_button.grid(row=0, column=5, padx=10, pady=10, sticky="w")


# Ergebnis-Label
result_label = tk.Label(root, text="", justify="left", font=("Arial", 10), anchor="w")
result_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Canvas für Diagramme
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

def update_report(*args):
    team = team_var.get()

    start = pd.to_datetime(start_date.get_date())
    end = pd.to_datetime(end_date.get_date())

    rugby_team = rugby[
        ((rugby['home_team'] == team) | (rugby['away_team'] == team)) &
        (pd.to_datetime(rugby['date']) >= start) &
        (pd.to_datetime(rugby['date']) <= end)
        ]

    if rugby_team.empty:
        result_label.config(text=f"Keine Spiele für {team} im gewählten Zeitraum ({start.date()} bis {end.date()}).")
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        return

    # Statistiken berechnen
    wins = losses = draws = points = 0
    opponents = []
    for _, i in rugby_team.iterrows():
        team_score = i['home_score'] if i['home_team'] == team else i['away_score']
        opp_score = i['away_score'] if i['home_team'] == team else i['home_score']
        opponent = i['away_team'] if i['home_team'] == team else i['home_team']
        opponents.append(opponent)
        points += team_score
        if team_score > opp_score:
            wins += 1
        elif team_score < opp_score:
            losses += 1
        else:
            draws += 1

    matches = len(rugby_team)
    avg_points = round(points / matches, 2) if matches > 0 else 0
    result_text = (
        f"Team: {team}\n"
        f"Spiele: {matches}\n"
        f"Siege: {wins}\n"
        f"Niederlagen: {losses}\n"
        f"Unentschieden: {draws}\n"
        f"Punkte pro Spiel: {avg_points}"
    )
    result_label.config(text=result_text)

    # Letzte 5 Spiele als Tabelle
    df_last5 = rugby_team.tail(5)

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    axs[0].axis('off')
    table = axs[0].table(cellText=df_last5.values, colLabels=df_last5.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1, 1.2)
    axs[0].set_title("Letzte 5 Spiele")

    # Tortendiagramm der Gegner
    opp_counts = pd.Series(opponents).value_counts()
    axs[1].pie(opp_counts.values, labels=opp_counts.index, autopct='%1.0f%%')
    axs[1].set_title("Gegnerverteilung")

    # Diagramm in GUI einbetten
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)

    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().pack(expand=True, fill='both')

# Eventbindung
team_dropdown.bind("<<ComboboxSelected>>", update_report)




# GUI starten
root.mainloop()