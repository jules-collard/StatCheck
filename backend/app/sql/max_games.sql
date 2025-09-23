WITH home_games AS (
    SELECT
        season,
        "homeTeamID",
        count(id) AS homeGames
    FROM games
    WHERE "gameType" == 2
    GROUP BY season, "homeTeamID"
),
away_games AS (
    SELECT
        season,
        "awayTeamID",
        count(id) AS awayGames
    FROM games
    WHERE "gameType" == 2
    GROUP BY season, "awayTeamID"
),
all_games AS (
    SELECT
        home_games.season,
        homeGames + awayGames AS totalGames
    FROM home_games
    FULL JOIN away_games ON home_games.season == away_games.season AND home_games."homeTeamID" == away_games."awayTeamID"
)
SELECT season, max(totalGames) AS max_games FROM all_games GROUP BY season;