import pandas as pd
from scrapers import scrape_teams
import requests

teams: pd.DataFrame = scrape_teams()
team = teams.loc[0].to_json()

requests.post("http://127.0.0.1:5000/api/teams", json=team)