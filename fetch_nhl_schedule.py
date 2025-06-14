from datetime import datetime
from dotenv import load_dotenv

import os
import pandas as pd
import requests

today = datetime.today().strftime('%Y-%m-%d')

# API protection 
load_dotenv()
sched_url = os.getenv("TEAM_API_PATH")

# Get Weeks Worth of NHL Games
def get_nhl_schedule(): 
    url =  sched_url
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed with the code: {e}")

# Data Validation
    try:
        res = response.json()
    except ValueError:
        raise Exception("Failed to parse JSON data from API response")
    
    games = [game for day in res["gameWeek"] for game in day["games"]]
    normalize = pd.json_normalize(games)

    # Parse Data into a more user friendly version
    data = fix_cols_name(normalize)


    return res
        


def fix_cols_name(data):
    data.columns = data.columns.str.replace(r"\.", "_", regex=True)

    # Drop cols not needed
    drop_cols = [
        'tvBroadcasts', 'alternateBroadcasts', 'seriesUrl',
        'ticketsLink', 'ticketsLinkFr', 'gameCenterLink',
        'awayTeam_logo', 'awayTeam_darkLogo', 'awayTeam_radioLink',
        'homeTeam_logo', 'homeTeam_darkLogo', 'homeTeam_radioLink',
        'awayTeam_placeName_fr', 'awayTeam_placeNameWithPreposition_fr',
        'homeTeam_placeName_fr', 'homeTeam_placeNameWithPreposition_fr',
        'seriesStatus_bottomSeedWins', 'gameType', 'seriesStatus_topSeedWins', 'neutralSite',
        'awayTeam_placeNameWithPreposition_default','homeTeam_placeNameWithPreposition_default'
    ]

    data = data.drop(columns=[col for col in drop_cols if col in data.columns])


    # Rename important columns
    data = data.rename(columns={
        'id': 'game_id',
        'startTimeUTC': 'start_time_utc',
        'venue_default': 'venue',
        'awayTeam_commonName_default': 'away_name',
        'awayTeam_abbrev': 'away_team',
        'homeTeam_commonName_default': 'home_name',
        'homeTeam_abbrev': 'home_team',
        'awayTeam_odds' : 'away_odds',
        'homeTeam_odds' : 'home_odds',
        'seriesStatus_gameNumberOfSeries': 'num_of_series',
        'awayTeam_placeName_default' : 'away_team_proper_name',
        'homeTeam_placeName_default' : 'home_team_proper_name'
    })
    
    return data





