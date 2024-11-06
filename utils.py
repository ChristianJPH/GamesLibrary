import os
import json

def read_games(games_path):
    if not os.path.exists(games_path) or not os.path.getsize(games_path):
        return {}
    with(open(games_path, "r")) as games_file:
        return json.load(games_file)