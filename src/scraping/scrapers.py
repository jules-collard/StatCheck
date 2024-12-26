import requests
import pandas as pd

def scrape_pbp(gameId: int) -> pd.DataFrame:
    """
    Scrapes play-by-play data from the NHL website for a given game ID.

    :param gameId: The ID of the game to scrape
    :type gameID: int
    :return: Dataframe with play-by-play data
    :rtype: pd.Dataframe
    """

    # Situation Code: *away G* *away skaters* *home skaters* *home G*

    url = f"https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play"
    cols = ['eventId', 'timeInPeriod', 'timeRemaining', 'situationCode', 'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
       'periodDescriptor.number', 'periodDescriptor.periodType', 'periodDescriptor.maxRegulationPeriods', 'details.eventOwnerTeamId',
       'details.losingPlayerId', 'details.winningPlayerId', 'details.xCoord', 'details.yCoord', 'details.zoneCode',
       'details.hittingPlayerId', 'details.hitteePlayerId', 'details.blockingPlayerId', 'details.shootingPlayerId', 'details.reason',
       'details.shotType', 'details.goalieInNetId', 'details.playerId', 'details.typeCode',
       'details.descKey', 'details.duration', 'details.committedByPlayerId', 'details.drawnByPlayerId', 'details.scoringPlayerId',
       'details.assist1PlayerId', 'details.assist2PlayerId']
    

    response = requests.get(url).json()
    pbp_df = pd.json_normalize(response["plays"])[cols]
    pbp_df["gameId"] = gameId
    pbp_df.rename(columns = {'eventId':'id',
                                'periodDescriptor.number':'period',
                                'periodDescriptor.periodType':'periodType',
                                'periodDescriptor.maxRegulationPeriods':'maxRegulationPeriods',
                                },
                                inplace=True)
    categorical_cols = ['homeTeamDefendingSide', 'typeDescKey', 'periodType', 'details.zoneCode', 'details.reason', 'details.shotType', 'details.typeCode', 'details.descKey']
    
    pbp_df[categorical_cols] = pbp_df[categorical_cols].astype('category')

    # Add meta data (datetime of the execution)
    pbp_df["meta_datetime"] = pd.to_datetime("now")

    return pbp_df

def scrape_player(playerId: int) -> dict:
    """
    Scrapes player data from the NHL website for a given player ID.

    :param playerId: The ID of the player to scrape data for
    :type playerId: int
    :return: A dictionary containing the scraped player data.
    """

    url = f"https://api-web.nhle.com/v1/player/{playerId}/landing"

    response = requests.get(url).json()
    keys = ['playerId', 'isActive', 'currentTeamId', 'firstName', 'lastName', 'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches', 'heightInCentimeters', 'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity', 'birthCountry', 'shootsCatches', 'draftDetails', 'inTop100AllTime', 'inHHOF', 'awards']
    
    details = {key:response[key] for key in keys}

    return details

def scrape_schedule(date: str) -> pd.DataFrame:
    """
    Scrapes schedule data from the NHL website for a given date.

    :param date: The date to scrape the schedule (YYYY-MM-DD)
    :type date: str
    :return: Dataframe with schedule data
    :rtype: pd.Dataframe
    """

    # Game Type: 2-REG, 3-POST

    url = f"https://api-web.nhle.com/v1/schedule/{date}"
    response = requests.get(url).json()

    cols = ['id', 'season', 'gameType', 'neutralSite', 'startTimeUTC', 'easternUTCOffset', 'venueUTCOffset', 'venueTimezone', 'gameState',
       'gameScheduleState', 'venue.default', 'awayTeam.id', 'awayTeam.score', 'homeTeam.id', 'homeTeam.score', 'periodDescriptor.maxRegulationPeriods',
       'gameOutcome.lastPeriodType', 'winningGoalie.playerId', 'winningGoalScorer.playerId']
    schedule_df = pd.json_normalize(response["gameWeek"][0]["games"])[cols]
    schedule_df["date"] = date

    return schedule_df

def scrape_shifts(gameId: int) -> pd.DataFrame:
    """
    Scrapes shift data from the NHL website for a given game ID.
    
    :param game_id: The ID of the game you want to scrape the shift data for.
    :type game_id: int
    :return: A DataFrame containing the scraped shift data
    :rtype: pd.DataFrame
    """

    cols = ['id', 'duration', 'startTime', 'endTime', 'eventNumber', 'gameId', 'period', 'playerId', 'shiftNumber', 'teamId', 'meta_datetime']

    url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameId}"
    response = requests.get(url).json()
    shifts_df = pd.json_normalize(response["data"])

    # Add meta data (datetime of the execution)
    shifts_df["meta_datetime"] = pd.to_datetime("now")
    # Remove goal events
    shifts_df = shifts_df[(shifts_df["detailCode"] == 0) & (shifts_df["typeCode"] == 517)]
    shifts_df = shifts_df[cols]

    return shifts_df

def scrape_teams() -> pd.DataFrame:
    """
    Scrapes team data from the NHL website

    Returns :
    :return: A DataFrame containing the scraped team data.
    :rtype: pd.DataFrame
    """

    url = "https://api.nhle.com/stats/rest/en/franchise?sort=fullName"

    response = requests.get(url).json()

    teams_df = pd.json_normalize(response["data"])
    # Add meta data (datetime of the execution)
    teams_df["meta_datetime"] = pd.to_datetime("now")

    return teams_df

if __name__ == "__main__":
    schedule_df = scrape_schedule("2024-12-21")
    shifts_df = scrape_shifts(2024020170)
    pbp_df = scrape_pbp(2024020170)
    player = scrape_player(8478402)
    teams = scrape_teams()
    pass