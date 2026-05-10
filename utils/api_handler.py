import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CricbuzzAPI:
    def __init__(self):
        self.api_key = os.getenv('CRICBUZZ_API_KEY')
        self.api_host = os.getenv('CRICBUZZ_API_HOST', 'cricbuzz-cricket.p.rapidapi.com')
        self.base_url = 'https://cricbuzz-cricket.p.rapidapi.com'
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host
        }
    
    def get_live_matches(self):
        """Fetch live matches from Cricbuzz API"""
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching live matches: {e}")
            return None
    
    def get_match_details(self, match_id):
        """Fetch detailed match information"""
        try:
            url = f"{self.base_url}/matches/v1/{match_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching match details: {e}")
            return None
    
    def get_player_stats(self, player_id):
        """Fetch player statistics"""
        try:
            url = f"{self.base_url}/stats/v1/player/{player_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return None
    
    def get_series_matches(self, series_id):
        """Fetch matches from a specific series"""
        try:
            url = f"{self.base_url}/series/v1/{series_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching series matches: {e}")
            return None