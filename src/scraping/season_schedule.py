import pandas as pd
import requests

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

if __name__ == "__main__":
    schedule_df = scrape_schedule("2024-12-21")