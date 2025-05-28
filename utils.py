# === utils.py ===

import yaml
import glob
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import pickle

class PlayerFeatureHistory:
    def __init__(self, history):
        self.history = history

    def to_vector(self):
        scores = [pt for _, pt in self.history[-10:]]
        avg = np.mean(scores) if scores else 0
        std = np.std(scores) if scores else 0
        return np.array([avg, std])

def parse_cricsheet_data(data_dir):
    matches = []
    for file in glob.glob(os.path.join(data_dir, "*.yaml")):
        with open(file, 'r') as f:
            match = yaml.safe_load(f)
            matches.append(match)
    return matches

def _ball_points(ball):
    runs = ball.get("runs", {})
    score = runs.get("batsman", 0)
    points = score
    if score == 4:
        points += 1
    elif score == 6:
        points += 2

    dismissal = ball.get("wicket")
    if isinstance(dismissal, list):
        dismissal = dismissal[0] if dismissal else None
    kind = dismissal.get("kind") if isinstance(dismissal, dict) else None
    bowler = ball.get("bowler")
    fielder = dismissal.get("fielder") if kind else None
    if kind and bowler:
        points += 25
    if kind and fielder:
        if kind == 'caught':
            points += 8
        elif kind in ['stumped', 'run out']:
            points += 12
    return points

def build_dataset(data_dir):
    matches = parse_cricsheet_data(data_dir)
    player_histories = defaultdict(list)
    player_roles = {}
    for match in matches:
        for innings in match.get("innings", []):
            for team, details in innings.items():
                for delivery in details.get("deliveries", []):
                    for _, ball in delivery.items():
                        batter = ball.get("batsman")
                        bowler = ball.get("bowler")
                        if batter:
                            pts = _ball_points(ball)
                            player_histories[batter].append((match['info'], pts))
                            player_roles[batter] = "batsman"
                        if bowler:
                            player_roles.setdefault(bowler, "bowler")

    rows = []
    avg_points = defaultdict(list)
    for player, logs in player_histories.items():
        for info, pts in logs:
            rows.append({"player": player, "pts": pts})
            avg_points[player].append(pts)
    df = pd.DataFrame(rows)

    leaderboard = sorted(
        [(player, np.mean(pts)) for player, pts in avg_points.items() if len(pts) > 5],
        key=lambda x: x[1], reverse=True
    )[:10]
    df_leaderboard = pd.DataFrame(leaderboard, columns=["Player", "Avg Points"])
    df_leaderboard.to_json("leaderboard.json", orient="records")

    return df, player_histories, player_roles

def load_or_train_model(data_dir, model_path):
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model, lookup, roles = pickle.load(f)
            return model, lookup, roles
    df, histories, roles = build_dataset(data_dir)
    feats = []
    labels = []
    lookup = {}
    for name, logs in histories.items():
        feature = PlayerFeatureHistory(logs)
        x = feature.to_vector()
        y = np.mean([pt for _, pt in logs])
        feats.append(x)
        labels.append(y)
        lookup[name] = feature
    X = np.vstack(feats)
    y = np.array(labels)
    model = GradientBoostingRegressor().fit(X, y)

    # Save a performance chart
    try:
        import matplotlib.pyplot as plt
        y_pred = model.predict(X)
        plt.figure(figsize=(8, 5))
        plt.scatter(y, y_pred, alpha=0.6)
        plt.xlabel("Actual Avg Points")
        plt.ylabel("Predicted Avg Points")
        plt.title("Model Prediction Performance")
        plt.grid(True)
        plt.savefig("performance_plot.png")
    except Exception as e:
        print(f"Could not generate chart: {e}")

    with open(model_path, "wb") as f:
        pickle.dump((model, lookup, roles), f)
    return model, lookup, roles

def live_scores():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        matches = soup.select(".cb-mtch-lst .cb-lv-scrs-col")
        return matches[0].get_text(strip=True) if matches else "No live matches found."
    except Exception as e:
        return f"Error fetching live scores: {e}"

def answer_faq(text):
    faqs = {
        "scoring": "Batting: 1 pt per run, +1 for 4s, +2 for 6s. Bowling: 25 pts per wicket. Fielding: 8-12 pts depending on type.",
        "how does scoring work": "Batting: 1 pt per run, +1 for 4s, +2 for 6s. Bowling: 25 pts per wicket. Fielding: 8-12 pts.",
        "who made this": "This bot was made using FastAPI, ML regression, and CricSheet YAML data.",
        "help": "Try asking things like 'Recommend a batsman', 'Live scores', or 'How does scoring work'."
    }
    for k, v in faqs.items():
        if k in text:
            return v
    return None

def get_role_stats(histories, roles):
    role_points = defaultdict(list)
    for player, logs in histories.items():
        role = roles.get(player, "unknown")
        pts_list = [pt for _, pt in logs]
        if pts_list:
            role_points[role].extend(pts_list)

    role_avg = {r: np.mean(pts) for r, pts in role_points.items() if pts}
    return role_avg
