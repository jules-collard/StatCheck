from typing import List, Tuple

import requests

from .. import BACKEND_URL
from src.models.appearances import GoalieAppearanceBase, SkaterAppearanceBase
from src.scrapers.players import scrape_player, post_player

def scrape_appearances(gameID: int) -> Tuple[List[SkaterAppearanceBase], List[GoalieAppearanceBase]]:
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    teamIDs = {"awayTeam":response["awayTeam"]["id"], "homeTeam":response["homeTeam"]["id"]}
    skater_appearances = []
    goalie_appearances = []

    for team, teamID in teamIDs.items():
        for player in response["playerByGameStats"][team]["forwards"] + response["playerByGameStats"][team]["defense"]:
            skater_appearances.append(SkaterAppearanceBase(
                playerID=player['playerId'],
                teamID=teamID,
                gameID=gameID,
                position=player['position'],
                goals=player['goals'],
                powerPlayGoals=player['powerPlayGoals'],
                assists=player['assists'],
                plusMinus=player['plusMinus'],
                pim=player['pim'],
                hits=player['hits'],
                sog=player['sog'],
                blocks=player['blockedShots'],
                giveaways=player['giveaways'],
                takeaways=player['takeaways'],
                toiSeconds=int(player['toi'].split(':')[0]) * 60 + int(player['toi'].split(':')[1])
            ))
        for gk in response["playerByGameStats"][team]["goalies"]:
            goalie_appearances.append(GoalieAppearanceBase(
                appearanceID=int(str(gk['playerId']) + str(teamID) + str(gameID)),
                playerID=gk['playerId'],
                teamID=teamID,
                gameID=gameID,
                evenStrengthSaves=int(gk['evenStrengthShotsAgainst'].split('/')[0]),
                evenStrengthShotsAgainst=int(gk['evenStrengthShotsAgainst'].split('/')[1]),
                powerPlaySaves=int(gk['powerPlayShotsAgainst'].split('/')[0]),
                powerPlayShotsAgainst=int(gk['powerPlayShotsAgainst'].split('/')[1]),
                shorthandedSaves=int(gk['shorthandedShotsAgainst'].split('/')[0]),
                shorthandedShotsAgainst=int(gk['shorthandedShotsAgainst'].split('/')[1]),
                saves=gk['saves'],
                shotsAgainst=gk['shotsAgainst'],
                toiSeconds=int(gk['toi'].split(':')[0]) * 60 + int(gk['toi'].split(':')[1]),
                starter=gk['starter'],
                played=True if gk['starter'] or int(gk['toi'].replace(':','')) > 0 else False,
                decision=gk['decision'] if 'decision' in gk.keys() else None
            ))
    return skater_appearances, goalie_appearances

def post_appearances(gameID: int, skaters: List[SkaterAppearanceBase], goalies: List[GoalieAppearanceBase]):
    ids = set(app.playerID for app in goalies + skaters)
    db_ids = set(requests.get(f"{BACKEND_URL}/players/all/ids").json())
    new_ids = ids - db_ids
    
    for id in new_ids:
        player = scrape_player(id)
        post_player(player)

    skater_r = requests.post(f"{BACKEND_URL}/games/{gameID}/skater-apps", json=[skater.model_dump() for skater in skaters])
    goalie_r = requests.post(f"{BACKEND_URL}/games/{gameID}/goalie-apps", json=[goalie.model_dump() for goalie in goalies])
    print(f"Skaters: {skater_r.status_code}")
    print(f"Goalies: {goalie_r.status_code}")

if __name__ == "__main__":
    skaters, goalies = scrape_appearances(2025020253)
    post_appearances(2025020253, skaters, goalies)