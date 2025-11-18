import requests

from src.models.teams import TeamBase
from .. import BACKEND_URL

def scrape_teams():
    url = "https://api.nhle.com/stats/rest/en/team"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    teams = [{k:team.get(k) for k in ["id", "franchiseId", "fullName", "triCode"]} for team in response.get('data')]
    for team in teams:
        team['franchiseID'] = team.pop('franchiseId')
    teamObjs = [TeamBase(**data) for data in teams]

    return teamObjs

def post_teams(*teams: TeamBase):
    for team in teams:
        r = requests.post(f"{BACKEND_URL}/teams/", json=team.model_dump())
        print(r.status_code)
        print(r.json())

def delete_team(id: int):
    r = requests.delete(f"{BACKEND_URL}/teams/{id}")
    print(r.status_code)
