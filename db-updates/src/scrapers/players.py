import requests
import logfire

from src.models.players import PlayerBase, AwardBase
from src.main import BACKEND_URL, get_log_level

def scrape_player(playerID: int) -> PlayerBase:
    url = f"https://api-web.nhle.com/v1/player/{playerID}/landing"

    response: dict = requests.get(url)
    response.raise_for_status()
    response = response.json()

    response['id'] = response.pop('playerId', None)
    response['currentTeamID'] = response.pop('currentTeamId', None)
    response['firstName'] = response.pop('firstName', {}).pop('default', None)
    response['lastName'] = response.pop('lastName', {}).pop('default', None)
    response['birthCity'] = response.pop('birthCity', {}).pop('default', None)
    
    draft_details = response.pop('draftDetails', {})
    response['draftYear'] = draft_details.get('year', None)
    response['draftTeamAbbrev'] = draft_details.get('teamAbbrev', None)
    response['draftRound'] = draft_details.get('round', None)
    response['draftPickInRound'] = draft_details.get('pickInRound', None)
    response['draftOverallPick'] = draft_details.get('overallPick', None)
    
    awards = response.pop('awards', [])
    award_list = []
    for award in awards:
        for season in award.get('seasons'):
            award_obj = AwardBase(awardName=award.get('trophy').get('default'), season=season.get('seasonId'), winningPlayerID=playerID)
            award_list.append(award_obj)
    
    response['awards'] = award_list

    player = PlayerBase(**response)
    return player

def post_player(player: PlayerBase):
    r = requests.post(f"{BACKEND_URL}/players/", json=player.model_dump())
    logfire.log(get_log_level(r.status_code), f"POST Player {player.firstName} {player.lastName} {player.id}: {r.status_code}",
                attributes=dict(table='players', response_code=r.status_code))

def put_player(player: PlayerBase):
    r = requests.put(f"{BACKEND_URL}/players/", json=player.model_dump())
    logfire.log(get_log_level(r.status_code), f"PUT Player {player.firstName} {player.lastName} {player.id}: {r.status_code}",
                attributes=dict(table='players', response_code=r.status_code))

def delete_player(id: int):
    r = requests.delete(f"{BACKEND_URL}/players/{id}")
    logfire.log(get_log_level(r.status_code), f"DELETE Player {id}: {r.status_code}",
                table='players', response_code=r.status_code)
