import pandas as pd
import requests

def scrape_shifts(gameId: int):
    """
    Scrapes shift data from the NHL website for a given game ID.
    
    :param game_id: The ID of the game you want to scrape the shift data for.
    :type game_id: int
    :return: A DataFrame containing the scraped shift data
    :rtype: pd.DataFrame
    """

    url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameId}"
    response = requests.get(url).json()
    shifts_df = pd.json_normalize(response["data"])

    # Add meta data (datetime of the execution)
    shifts_df["meta_datetime"] = pd.to_datetime("now")

    return shifts_df

if __name__ == "__main__":
    shifts_df = scrape_shifts(2024020170)