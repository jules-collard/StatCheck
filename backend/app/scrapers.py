import requests
import pandas as pd
from datetime import datetime

def scrape_pbp(gameId: int):
    # Situation Code: *away G* *away skaters* *home skaters* *home G*

    url = f"https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play"
    cols = ['eventId', 'timeInPeriod', 'situationCode', 'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
       'periodDescriptor.number', 'periodDescriptor.periodType', 'periodDescriptor.maxRegulationPeriods', 'details.eventOwnerTeamId',
       'details.losingPlayerId', 'details.winningPlayerId', 'details.xCoord', 'details.yCoord', 'details.zoneCode',
       'details.hittingPlayerId', 'details.hitteePlayerId', 'details.blockingPlayerId', 'details.shootingPlayerId', 'details.reason',
       'details.shotType', 'details.goalieInNetId', 'details.playerId', 'details.duration', 'details.committedByPlayerId',
       'details.drawnByPlayerId', 'details.scoringPlayerId', 'details.assist1PlayerId', 'details.assist2PlayerId']

    response = requests.get(url).json()
    pbp_df = pd.json_normalize(response["plays"])[cols]
    
    pbp_df["gameID"] = gameId
    
    # Parse time in period
    timeInPeriodSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in pbp_df['timeInPeriod']]
    pbp_df['timeInPeriod'] = timeInPeriodSec

    pbp_df.rename(columns = {'eventId':'id',
                                'timeInPeriod':'timeInPeriodSec',
                                'periodDescriptor.number':'period',
                                'periodDescriptor.periodType':'periodType',
                                'periodDescriptor.maxRegulationPeriods':'maxRegulationPeriods'},
                                inplace=True)
    pbp_df.rename(columns = lambda x: x.replace("details.", ""), inplace=True)
    pbp_df.rename(columns = lambda x: x.replace("Id", "ID") if x.endswith("Id") else x, inplace=True)
    pbp_df['awayGoalie'] = pbp_df['situationCode'].apply(lambda x: int(x[0]))
    pbp_df['awaySkaters'] = pbp_df['situationCode'].apply(lambda x: int(x[1]))
    pbp_df['homeSkaters'] = pbp_df['situationCode'].apply(lambda x: int(x[2]))
    pbp_df['homeGoalie'] = pbp_df['situationCode'].apply(lambda x: int(x[3]))

    return pbp_df.to_dict(orient='records')

def scrape_player(playerId: int) -> dict:
    url = f"https://api-web.nhle.com/v1/player/{playerId}/landing"
    cols = ['playerId', 'isActive', 'currentTeamId', 'firstName.default', 'lastName.default',
            'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches', 'heightInCentimeters',
            'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity.default', 'birthCountry',
            'shootsCatches', 'draftDetails.year', 'draftDetails.teamAbbrev', 'draftDetails.round',
            'draftDetails.pickInRound', 'draftDetails.overallPick']

    response = requests.get(url).json()
    player_df = pd.json_normalize(response)
    player_df = player_df[[col for col in cols if col in player_df.columns]]
    player_df.rename(columns = {'playerId':'id',
                                'currentTeamId':'currentTeamID',
                                'firstName.default':'firstName',
                                'lastName.default':'lastName',
                                'birthCity.default':'birthCity',
                                'draftDetails.year':'draftYear',
                                'draftDetails.teamAbbrev':'draftTeamAbbrev',
                                'draftDetails.round':'draftRound',
                                'draftDetails.pickInRound':'draftPickInRound',
                                'draftDetails.overallPick':'draftOverallPick'},
                    inplace=True)

    # Parse birthdate
    player_df['birthDate'] = player_df['birthDate'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())

    return player_df.to_dict(orient='records')[0]

def scrape_schedule(date: str):
    """
    Scrapes schedule data from the NHL website for a given date.

    :param date: The date to scrape the schedule (YYYY-MM-DD)
    :type date: str
    :return: Dataframe with schedule data
    :rtype: pd.Dataframe
    """

    # Game Type: 2-REG, 3-POST

    url = f"https://api-web.nhle.com/v1/schedule/{date}"
    cols = ['id', 'season', 'gameType', 'neutralSite', 'startTimeUTC', 'venueUTCOffset', 'gameState', 'gameScheduleState',
            'venue.default', 'awayTeam.id', 'awayTeam.score', 'homeTeam.id', 'homeTeam.score', 'periodDescriptor.maxRegulationPeriods',
            'gameOutcome.lastPeriodType']

    response = requests.get(url).json()
    schedule_df = pd.json_normalize(response["gameWeek"][0]["games"])[cols]

    schedule_df.rename(columns = {'venue.default':'defaultVenue',
                                    'awayTeam.id':'awayTeamID', 'awayTeam.score':'awayTeamScore',
                                    'homeTeam.id':'homeTeamID', 'homeTeam.score':'homeTeamScore',
                                    'periodDescriptor.maxRegulationPeriods':'maxRegulationPeriods',
                                    'gameOutcome.lastPeriodType':'lastPeriodType'},
                                    inplace=True)
    
    # Type cleaning
    schedule_df['season'] = schedule_df['season'].astype(str)
    schedule_df['startTimeUTC'] = schedule_df['startTimeUTC'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    schedule_df['venueUTCOffset'] = schedule_df['venueUTCOffset'].apply(lambda x: int(x.split(":")[0]))
    schedule_df[['awayTeamScore', 'homeTeamScore']] = schedule_df[['awayTeamScore', 'homeTeamScore']].astype('Int64')
    schedule_df["date"] = schedule_df['startTimeUTC'].apply(lambda x: x.date())

    return schedule_df.to_dict(orient="records")

def scrape_shifts(gameId: int) -> pd.DataFrame:
    """
    Scrapes shift data from the NHL website for a given game ID.
    
    :param game_id: The ID of the game you want to scrape the shift data for.
    :type game_id: int
    :return: A DataFrame containing the scraped shift data
    :rtype: pd.DataFrame
    """

    url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameId}"
    cols = ['id', 'durationSec', 'startTimeSec', 'endTimeSec', 'eventNumber', 'gameId', 'period', 'playerId', 'shiftNumber', 'teamId']

    response = requests.get(url).json()
    shifts_df = pd.json_normalize(response["data"])

    # Remove goal events
    shifts_df = shifts_df[(shifts_df["detailCode"] == 0) & (shifts_df["typeCode"] == 517)]

    # Parse MM:SS start/end times
    durationSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['duration']]
    startTimeSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['startTime']]
    endTimeSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['endTime']]
    shifts_df["durationSec"] = durationSec
    shifts_df["startTimeSec"] = startTimeSec
    shifts_df["endTimeSec"] = endTimeSec

    shifts_df = shifts_df[cols]

    return shifts_df

def scrape_teams() -> list[dict]:
    """
    Scrapes team data from the NHL website

    :return: A DataFrame containing the scraped team data.
    :rtype: pd.DataFrame
    """

    url = "https://api.nhle.com/stats/rest/en/franchise?sort=fullName"

    response = requests.get(url).json()
    teams_df = pd.json_normalize(response["data"])
    teams_df.rename(columns = {"teamCommonName":"commonName", "teamPlaceName":"placeName"}, inplace=True)

    return teams_df.to_dict(orient='records')

def scrape_rosters(gameId: int):
    """
    Scrapes roster data from the NHL website for a given game ID.

    Parameters :
      - game_id (int) : The ID of the game you want to scrape the roster data for.

      Returns :
    :return: A DataFrame containing the scraped roster data.
    :rtype: pd.Dataframe

    """
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play"
    response = requests.get(url).json()

    rosters_df = pd.json_normalize(response['rosterSpots'])
    rosters_df["gameID"] = gameId
    rosters_df.rename(columns={"teamId":"teamID", "playerId":"playerID"}, inplace=True)

    cols = ["gameID", "teamID", "playerID"]
    rosters_df = rosters_df[cols]

    return rosters_df.to_dict(orient="records")


if __name__ == "__main__":
    schedule_df = scrape_schedule("2025-01-15")
    shifts_df = scrape_shifts(2024020170)
    pbp_df = scrape_pbp(2024020170)
    player = scrape_player(8478402)
    teams = scrape_teams()
    rosters_df = scrape_rosters(2024020170)
    pass