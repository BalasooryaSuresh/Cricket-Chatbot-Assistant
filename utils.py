# utils.py

import yaml
import glob
import os
import requests
from bs4 import BeautifulSoup

# Load CricSheet YAML data
def parse_cricsheet_data(data_dir):
    matches = []
    for file in glob.glob(os.path.join(data_dir, "*.yaml")):
        with open(file, 'r') as f:
            match = yaml.safe_load(f)
            matches.append(match)
    return matches

# Fantasy Point Calculation + Recommendation
def get_recommendation(matches, query):
    player_points = {}

    for match in matches[-100:]:  # Use recent 100 matches
        for innings in match.get('innings', []):
            for team_innings in innings.values():
                for delivery in team_innings.get('deliveries', []):
                    for ball_num, ball_info in delivery.items():
                        batsman = ball_info.get('batsman')
                        bowler = ball_info.get('bowler')
                        runs = ball_info.get('runs', {})
                        dismissal = ball_info.get('wicket', {})

                        # Batting points
                        if batsman:
                            score = runs.get('batsman', 0)
                            points = score  # 1 point per run
                            if score == 4:
                                points += 1
                            elif score == 6:
                                points += 2
                            player_points[batsman] = player_points.get(batsman, 0) + points

                        # Bowling points
                        if isinstance(dismissal, dict) and bowler:
                            player_points[bowler] = player_points.get(bowler, 0) + 25

                        # Fielding points
                        kind = None
                        fielder = None
                        if isinstance(dismissal, dict):
                            kind = dismissal.get('kind')
                            # Handles both 'fielder' and 'fielders'
                            fielder = dismissal.get('fielder')
                            if not fielder:
                                fielders = dismissal.get('fielders')
                                if isinstance(fielders, list) and fielders:
                                    fielder = fielders[0]

                        if kind and fielder:
                            if kind == 'caught':
                                player_points[fielder] = player_points.get(fielder, 0) + 8
                            elif kind in ['stumped', 'run out']:
                                player_points[fielder] = player_points.get(fielder, 0) + 12

    # Top performers
    top_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)[:5]

    response = "Top Fantasy Performers (last 100 matches):\n"
    for name, pts in top_players:
        response += f"- {name}: {pts} fantasy points\n"

    return response


# Live match score from Cricbuzz
def scrape_live_stats():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        matches = soup.select(".cb-mtch-lst .cb-lv-scrs-col")
        return matches[0].get_text(strip=True) if matches else "No live matches found."
    except Exception as e:
        return f"Error fetching live scores: {e}"
