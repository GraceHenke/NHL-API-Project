from dotenv import load_dotenv

import os
import requests

# API protection 
load_dotenv()
stats_url = os.getenv("STATS_API_PATH")

# Get Stats for each Team on the Schedule
def get_nhl_team_stats(teams):
    res = []
    for team in teams:
        url = stats_url + team
        
        try: 
          response = requests.get(url, timeout=10)
          response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed with the code: {e}")
        
        try:
            data = response.json()
        
        except ValueError:
            raise Exception("Failed to parse JSON data from API response")
        
    

    return data

def clean_up_data(data):
    pass
