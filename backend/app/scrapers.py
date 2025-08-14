import requests
import pandas as pd
import numpy as np
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

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    pbp_df = pd.json_normalize(response["plays"])
    pbp_df = pbp_df[pbp_df.columns[pbp_df.columns.isin(cols)]]
    
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
    pbp_df['awayGoalie'] = pbp_df['situationCode'].apply(lambda x: int(str(x)[0]) if pd.notna(x) else np.nan)
    pbp_df['awaySkaters'] = pbp_df['situationCode'].apply(lambda x: int(str(x)[1]) if pd.notna(x) else np.nan)
    pbp_df['homeSkaters'] = pbp_df['situationCode'].apply(lambda x: int(str(x)[2]) if pd.notna(x) else np.nan)
    pbp_df['homeGoalie'] = pbp_df['situationCode'].apply(lambda x: int(str(x)[3]) if pd.notna(x) else np.nan)

    return pbp_df.to_dict(orient='records')

def scrape_pbp_boxscore(gameID: int):
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    teamIDs = {"awayTeam":response["awayTeam"]["id"], "homeTeam":response["homeTeam"]["id"]}
    events = []
    eventID = 99901
    
    for team, teamID in teamIDs.items():
        for player in response["playerByGameStats"][team]["forwards"] + response["playerByGameStats"][team]["defense"]:
            for _ in range(player["goals"]):
                events.append({
                    'id': eventID,
                    'typeCode': 505,
                    'eventOwnerTeamID': teamID,
                    'scoringPlayerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["assists"]):
                events.append({
                    'id': eventID,
                    'typeCode': 505,
                    'eventOwnerTeamID': teamID,
                    'assist1PlayerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["hits"]):
                events.append({
                    'id': eventID,
                    'typeCode': 503,
                    'eventOwnerTeamID': teamID,
                    'hittingPlayerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["sog"]):
                events.append({
                    'id': eventID,
                    'typeCode': 506,
                    'eventOwnerTeamID': teamID,
                    'shootingPlayerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["blockedShots"]):
                events.append({
                    'id': eventID,
                    'typeCode': 508,
                    'eventOwnerTeamID': teamID,
                    'blockingPlayerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["giveaways"]):
                events.append({
                    'id': eventID,
                    'typeCode': 504,
                    'eventOwnerTeamID': teamID,
                    'playerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            for _ in range(player["takeaways"]):
                events.append({
                    'id': eventID,
                    'typeCode': 525,
                    'eventOwnerTeamID': teamID,
                    'playerID': player["playerId"],
                    'gameID': gameID
                })
                eventID += 1
            events.append({
                'id': eventID,
                'typeCode': 509, # Penalty
                'eventOwnerTeamID': teamID,
                'committedByPlayerID': player["playerId"],
                'duration': player["pim"],
                'gameID': gameID
            })

    return events

def scrape_player(playerId: int) -> dict:
    url = f"https://api-web.nhle.com/v1/player/{playerId}/landing"
    cols = ['playerId', 'isActive', 'currentTeamId', 'firstName.default', 'lastName.default',
            'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches', 'heightInCentimeters',
            'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity.default', 'birthCountry',
            'shootsCatches', 'draftDetails.year', 'draftDetails.teamAbbrev', 'draftDetails.round',
            'draftDetails.pickInRound', 'draftDetails.overallPick', 'inHHOF']

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    player_df = pd.json_normalize(response)

    if 'awards' in player_df.columns:
        awards = player_df['awards'][0]
        awards_dict = {award['trophy']['default']:[season['seasonId'] for season in award['seasons']] for award in awards}
    else:
        awards_dict = {}

    player_df = player_df[player_df.columns[player_df.columns.isin(cols)]]
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
    player_dict = player_df.to_dict(orient='records')[0]
    return player_dict, awards_dict

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

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    
    # Empty Gamedays
    if response["gameWeek"][0]["numberOfGames"] == 0:
        return {}
    
    schedule_df = pd.json_normalize(response["gameWeek"][0]["games"])
    schedule_df = schedule_df[schedule_df.columns[schedule_df.columns.isin(cols)]]
    
    schedule_df['gameType'] = schedule_df['gameType'].astype('Int64')
    if len(schedule_df) == 0: return {}

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

    # Only completed games
    schedule_df = schedule_df[(schedule_df['gameState'] == 'OFF') & (schedule_df['gameScheduleState'] == 'OK')]

    return schedule_df.to_dict(orient="records")

def scrape_shifts(gameId: int):
    """
    Scrapes shift data from the NHL website for a given game ID.
    
    :param game_id: The ID of the game you want to scrape the shift data for.
    :type game_id: int
    :return: A DataFrame containing the scraped shift data
    :rtype: pd.DataFrame
    """

    url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameId}"
    cols = ['id', 'durationSec', 'startTimeSec', 'endTimeSec', 'eventNumber', 'gameID', 'period', 'playerID', 'shiftNumber', 'teamID']

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    shifts_df = pd.json_normalize(response["data"])
    
    # Some games do not have shift data
    if len(shifts_df) == 0:
        return {}

    # Remove goal events
    shifts_df = shifts_df[(shifts_df["detailCode"] == 0) & (shifts_df["typeCode"] == 517)]

    # Rename cols
    shifts_df.rename({'gameId':'gameID', 'playerId':'playerID', 'teamId':'teamID'}, axis="columns", inplace=True)

    # Parse MM:SS start/end times
    durationSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['duration']]
    startTimeSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['startTime']]
    endTimeSec = [int(i.split(":")[0]) * 60 + int(i.split(":")[1]) for i in shifts_df['endTime']]
    shifts_df["durationSec"] = durationSec
    shifts_df["startTimeSec"] = startTimeSec
    shifts_df["endTimeSec"] = endTimeSec

    shifts_df = shifts_df[shifts_df.columns[shifts_df.columns.isin(cols)]]

    return shifts_df.to_dict(orient='records')

def scrape_teams():
    """
    Scrapes team data from the NHL website

    :return: A DataFrame containing the scraped team data.
    :rtype: pd.DataFrame
    """

    url = "https://api.nhle.com/stats/rest/en/team"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    teams_df = pd.json_normalize(response["data"])[["id", "franchiseId", "fullName", "triCode"]]
    teams_df.rename(columns = {"franchiseId":"franchiseID"}, inplace=True)

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
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    rosters_df = pd.json_normalize(response['rosterSpots'])
    rosters_df["gameID"] = gameId
    rosters_df.rename(columns={"teamId":"teamID", "playerId":"playerID"}, inplace=True)

    cols = ["gameID", "teamID", "playerID"]
    rosters_df = rosters_df[cols]

    return rosters_df.to_dict(orient="records")

def scrape_rosters_boxscore(gameID: int):
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    homeTeamID = response["homeTeam"]["id"]
    awayTeamID = response["awayTeam"]["id"]
    rosters = []
    for player in response["playerByGameStats"]["awayTeam"]["forwards"] + response["playerByGameStats"]["awayTeam"]["defense"]:
        rosters.append({"gameID": gameID, "teamID": awayTeamID, "playerID": player["playerId"]})

    for player in response["playerByGameStats"]["homeTeam"]["forwards"] + response["playerByGameStats"]["homeTeam"]["defense"]:
        rosters.append({"gameID": gameID, "teamID": homeTeamID, "playerID": player["playerId"]})

    return rosters

def scrape_goalies_boxscore(gameID: int):
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    appearances = []

    for gk in response["playerByGameStats"]["awayTeam"]["goalies"] + response["playerByGameStats"]["homeTeam"]["goalies"]:
        appearances.append({
            'playerID': gk['playerId'],
            'gameID': gameID,
            'evenStrengthSaves': int(gk['evenStrengthShotsAgainst'].split('/')[0]),
            'evenStrengthShotsAgainst': int(gk['evenStrengthShotsAgainst'].split('/')[1]),
            'powerPlaySaves': int(gk['powerPlayShotsAgainst'].split('/')[0]),
            'powerPlayShotsAgainst': int(gk['powerPlayShotsAgainst'].split('/')[1]),
            'shorthandedSaves': int(gk['shorthandedShotsAgainst'].split('/')[0]),
            'shorthandedShotsAgainst': int(gk['shorthandedShotsAgainst'].split('/')[1]),
            'saves': gk['saves'],
            'shotsAgainst': gk['shotsAgainst'],
            'starter': gk['starter'],
            'played': True if gk['starter'] or int(gk['toi'].replace(':','')) > 0 else False,
            'decision': gk['decision'] if 'decision' in gk.keys() else None
        })

    return appearances


if __name__ == "__main__":
    print(scrape_goalies_boxscore(2020020009))
    pass