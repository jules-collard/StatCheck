import requests
import logfire

from src.main import BACKEND_URL
from src.models.games import GameBase

def scrape_schedule(date: str):
    # date: YYYY-MM-DD
    url = f"https://api-web.nhle.com/v1/schedule/{date}"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    
    # Empty Gamedays
    if response["gameWeek"][0]["numberOfGames"] == 0:
        return []
    
    games = response.get('gameWeek', [{}])[0].get('games', None)

    for game in games:
        game['defaultVenue'] = game.pop('venue', {}).pop('default', None)
        game['awayTeamID'] = game.get('awayTeam', {}).pop('id', None)
        game['homeTeamID'] = game.get('homeTeam', {}).pop('id', None)
        game['awayTeamScore'] = game.pop('awayTeam', {}).pop('score', None)
        game['homeTeamScore'] = game.pop('homeTeam', {}).pop('score', None)
        game['lastPeriodType'] = game.pop('gameOutcome', {}).pop('lastPeriodType', None)
        game['gameDate'] = date

    games = [game for game in games if game.get('gameState', None) == 'OFF' and game.get('gameScheduleState', None) == 'OK']
    
    return [GameBase(**game) for game in games]

def post_game(game: GameBase):
    r = requests.post(f"{BACKEND_URL}/games/", json=game.model_dump())
    logfire.info(f"Game {game.id}: {r.status_code}", table='games', response_code=r.status_code)

def delete_game(id: int):
    r = requests.delete(f"{BACKEND_URL}/games/{id}")
    logfire.info(f"DELETING Game {id}", table='games', response_code=r.status_code)
