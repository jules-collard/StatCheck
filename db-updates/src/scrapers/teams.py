import requests

from src.models.teams import TeamBase
from .. import BACKEND_URL

def scrape_teams():
    url = "https://api.nhle.com/stats/rest/en/team"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    teams = [{k:team.get(k) for k in ["id", "franchiseId", "fullName", "triCode"]} for team in response.get('data')]
    teamObjs = [TeamBase(**data) for data in teams]

    return teamObjs

def post_team(team: TeamBase):
    r = requests.post(f"{BACKEND_URL}/teams/", json=team.model_dump())
    print(r.status_code)

if __name__ == "__main__":
    teams = scrape_teams()
    print(post_team(teams[0]))