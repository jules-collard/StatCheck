import requests

from ..schemas.players import PlayerBase, AwardBase
from .. import BACKEND_URL

def scrape_player(playerID: int) -> dict:
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
    r = requests.put(f"{BACKEND_URL}/players/", json=player.model_dump())
    return r.json()


if __name__ == "__main__":
    player: PlayerBase = scrape_player(8455710)
    print(post_player(player))
    # r = requests.put(f"{BACKEND_URL}/healthcheck", json={'id': 2, 'body': 'testing'})
    # print(r.json())