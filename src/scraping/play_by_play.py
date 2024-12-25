import pandas as pd
import requests
import json

def scrape_pbp(gameId: int) -> pd.DataFrame:
    """
    Scrapes play-by-play data from the NHL website for a given game ID.

    :param gameId: The ID of the game to scrape
    :type gameID: int
    :return: Dataframe with play-by-play data
    :rtype: pd.Dataframe
    """

    url = f"https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play"
    cols = ['eventId', 'timeInPeriod', 'timeRemaining', 'situationCode', 'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
       'periodDescriptor.number', 'periodDescriptor.periodType', 'periodDescriptor.maxRegulationPeriods', 'details.eventOwnerTeamId',
       'details.losingPlayerId', 'details.winningPlayerId', 'details.xCoord', 'details.yCoord', 'details.zoneCode',
       'details.hittingPlayerId', 'details.hitteePlayerId', 'details.blockingPlayerId', 'details.shootingPlayerId', 'details.reason',
       'details.shotType', 'details.goalieInNetId', 'details.awaySOG', 'details.homeSOG', 'details.playerId', 'details.typeCode',
       'details.descKey', 'details.duration', 'details.committedByPlayerId', 'details.drawnByPlayerId', 'details.scoringPlayerId',
       'details.scoringPlayerTotal', 'details.assist1PlayerId', 'details.assist1PlayerTotal', 'details.assist2PlayerId',
       'details.assist2PlayerTotal', 'details.awayScore', 'details.homeScore', 'details.secondaryReason']
    

    response = requests.get(url).json()
    with open("pbp.json", "w") as f:
        json.dump(response, f)
    pbp_df = pd.json_normalize(response["plays"])[cols]
    pbp_df["gameId"] = gameId

    # Add meta data (datetime of the execution)
    pbp_df["meta_datetime"] = pd.to_datetime("now")

    return pbp_df


if __name__ == "__main__":
    pbp_df = scrape_pbp(2024020170)