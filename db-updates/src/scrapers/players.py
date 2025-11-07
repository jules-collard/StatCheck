from datetime import datetime

import requests

from ..schemas import PlayerBase, AwardBase

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

    response['birthDate'] = datetime.strptime(response.get('birthDate', None), '%Y-%m-%d').date()

    player = PlayerBase(**response)
    
    return player.model_dump_json()


if __name__ == "__main__":
    print(scrape_player(8448208))