import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, username):
        self.username = username
        self.rankings = []
        self.total_points = 0

    def set_rankings(self, rankings):
        self.rankings = rankings

    def update_points(self, points):
        self.total_points += points

def initialize_teams():
    return ["GT", "LSG", "SRH", "MI", "RCB", "KKR", "PBKS", "DC", "RR", "CSK"]

def load_schedule():
    return [
        {"match_no": 1, "team1": "MI", "team2": "CSK", "date": "2025-03-23"},
        {"match_no": 2, "team1": "RCB", "team2": "KKR", "date": "2025-03-24"},
        {"match_no": 3, "team1": "GT", "team2": "LSG", "date": "2025-03-25"},
        {"match_no": 4, "team1": "SRH", "team2": "PBKS", "date": "2025-03-26"},
        {"match_no": 5, "team1": "DC", "team2": "RR", "date": "2025-03-27"},
    ]

def get_team_points(rank_index):
    points_distribution = [10, 9, 8, 7, 6, 5, 4, 3, 2, -4]
    return points_distribution[rank_index]

def submit_rankings():
    username = entry_username.get().strip()
    rankings = entry_rankings.get().strip().split(',')

    if len(rankings) != 10:
        messagebox.showerror("Error", "Please enter exactly 10 teams.")
        return

    rankings = [team.strip() for team in rankings]

    for team in rankings:
        if team not in teams:
            messagebox.showerror("Error", f"Invalid team: {team}")
            return

    user = User(username)
    user.set_rankings(rankings)
    users.append(user)

    listbox_users.insert(tk.END, f"User: {username} | Rankings: {', '.join(rankings)}")

    entry_username.delete(0, tk.END)
    entry_rankings.delete(0, tk.END)

def submit_match_result():
    team1 = entry_team1.get().strip()
    team2 = entry_team2.get().strip()
    winner = entry_winner.get().strip().upper()

    if team1 not in teams or team2 not in teams:
        messagebox.showerror("Error", "Invalid team names.")
        return

    if winner not in [team1, team2, "TIE", "CANCELED"]:
        messagebox.showerror("Error", "Winner must be Team 1, Team 2, 'TIE', or 'CANCELED'.")
        return

    for user in users:
        if winner == "TIE":
            if team1 in user.rankings:
                user.update_points(get_team_points(user.rankings.index(team1)) // 2)
            if team2 in user.rankings:
                user.update_points(get_team_points(user.rankings.index(team2)) // 2)
        elif winner == "CANCELED":
            min_points = min(get_team_points(user.rankings.index(team1)), get_team_points(user.rankings.index(team2)))
            user.update_points(min_points)
        else:
            if winner in user.rankings:
                user.update_points(get_team_points(user.rankings.index(winner)))
            elif winner == user.rankings[-1]:
                user.update_points(1)

    label_match_winner.config(text=f"Latest Match: {team1} vs {team2} - Result: {winner}")
    print_standings()

    entry_team1.delete(0, tk.END)
    entry_team2.delete(0, tk.END)
    entry_winner.delete(0, tk.END)

def print_standings():
    standings_text.delete(1.0, tk.END)
    standings_text.insert(tk.END, "Current Standings:\n")
    sorted_users = sorted(users, key=lambda u: u.total_points, reverse=True)
    for user in sorted_users:
        standings_text.insert(tk.END, f"{user.username}: {user.total_points} points\n")

def display_upcoming_matches():
    upcoming_matches_text.delete(1.0, tk.END)
    upcoming_matches_text.insert(tk.END, "Upcoming Matches:\n")
    for match in schedule:
        match_info = f"Match {match['match_no']}: {match['team1']} vs {match['team2']} on {match['date']}\n"
        upcoming_matches_text.insert(tk.END, match_info)

teams = initialize_teams()
users = []
schedule = load_schedule()

root = tk.Tk()
root.title("IPL Fantasy League")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

label_username = tk.Label(frame_top, text="Username:")
label_username.grid(row=0, column=0, padx=5, pady=5)

entry_username = tk.Entry(frame_top)
entry_username.grid(row=0, column=1, padx=5, pady=5)

label_rankings = tk.Label(frame_top, text="Team Rankings (comma separated):")
label_rankings.grid(row=1, column=0, padx=5, pady=5)

entry_rankings = tk.Entry(frame_top, width=50)
entry_rankings.grid(row=1, column=1, padx=5, pady=5)

button_submit = tk.Button(frame_top, text="Submit Rankings", command=submit_rankings)
button_submit.grid(row=2, columnspan=2, pady=10)

frame_users = tk.Frame(root)
frame_users.pack(pady=10)

listbox_users = tk.Listbox(frame_users, width=80, height=6)
listbox_users.pack()

frame_match_result = tk.Frame(root)
frame_match_result.pack(pady=10)

label_team1 = tk.Label(frame_match_result, text="Team 1:")
label_team1.grid(row=0, column=0, padx=5, pady=5)
entry_team1 = tk.Entry(frame_match_result)
entry_team1.grid(row=0, column=1, padx=5, pady=5)

label_team2 = tk.Label(frame_match_result, text="Team 2:")
label_team2.grid(row=1, column=0, padx=5, pady=5)
entry_team2 = tk.Entry(frame_match_result)
entry_team2.grid(row=1, column=1, padx=5, pady=5)

label_winner = tk.Label(frame_match_result, text="Winner (or 'TIE'/'CANCELED'):")
label_winner.grid(row=2, column=0, padx=5, pady=5)
entry_winner = tk.Entry(frame_match_result)
entry_winner.grid(row=2, column=1, padx=5, pady=5)

button_submit_result = tk.Button(frame_match_result, text="Submit Match Result", command=submit_match_result)
button_submit_result.grid(row=3, columnspan=2, pady=10)

label_match_winner = tk.Label(root, text="Latest Match: None", font=("Arial", 12))
label_match_winner.pack(pady=5)

standings_text = tk.Text(root, width=50, height=10)
standings_text.pack(pady=10)

frame_upcoming_matches = tk.Frame(root)
frame_upcoming_matches.pack(pady=10)

upcoming_matches_text = tk.Text(frame_upcoming_matches, width=50, height=10)
upcoming_matches_text.pack()

display_upcoming_matches()

root.mainloop()
