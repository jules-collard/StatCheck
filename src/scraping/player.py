import requests

def scrape_player(playerId: int):
    """
    Scrapes player data from the NHL website for a given player ID.

    :param playerId: The ID of the player to scrape data for
    :type playerId: int
    :return: A dictionary containing the scraped player data.
    """

    url = f"https://api-web.nhle.com/v1/player/{playerId}/landing"

    response = requests.get(url).json()
    keys = ['playerId', 'isActive', 'currentTeamId', 'firstName', 'lastName', 'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches', 'heightInCentimeters', 'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity', 'birthStateProvince', 'birthCountry', 'shootsCatches', 'draftDetails', 'playerSlug', 'inTop100AllTime', 'inHHOF', 'featuredStats', 'careerTotals', 'awards']
    
    details = {key:response[key] for key in keys}

    return details

if __name__ == "__main__":
    scrape_player(8478402)