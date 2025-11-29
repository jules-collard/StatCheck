from typing import List

import requests
import logfire

from src.models.teams import TeamBase
from src.main import BACKEND_URL

def scrape_teams() -> List[TeamBase]:
    url = "https://api.nhle.com/stats/rest/en/team"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    teams = [{k:team.get(k) for k in ["id", "franchiseId", "fullName", "triCode"]} for team in response.get('data')]
    for team in teams:
        team['franchiseID'] = team.pop('franchiseId')
    return [TeamBase(**data) for data in teams]

def post_teams(teams: List[TeamBase]):
    for team in teams:
        r = requests.post(f"{BACKEND_URL}/teams/", json=team.model_dump())
        logfire.info(f"Team {team.triCode} {team.id}: {r.status_code}", table='teams', response_code=r.status_code)

def delete_team(id: int):
    r = requests.delete(f"{BACKEND_URL}/teams/{id}")
    logfire.info(f"DELETE Team {id}: {r.status_code}", table='teams', response_code=r.status_code)
