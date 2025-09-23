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
),
max_games AS (
    SELECT season, max(totalGames) AS games
    FROM all_games
    GROUP BY season
),
goalie_seasons AS (
    SELECT
        "playerID",
        "games"."season",
        sum("goalie_appearances"."played") AS "gamesPlayed",
        sum("goalie_appearances"."starter") AS "gamesStarted",
        sum(CASE WHEN "goalie_appearances"."decision" == 'W' THEN 1 ELSE 0 END) AS "wins",
        sum(CASE WHEN "goalie_appearances"."decision" == "L" THEN 1 ELSE 0 END) AS "losses",
        (sum("goalie_appearances"."shotsAgainst") - sum("goalie_appearances"."saves")) * 3600.0 / sum("goalie_appearances"."toiSeconds") AS "goalsAgainstAvg",
        sum("goalie_appearances"."saves") * 1.0 / sum("goalie_appearances"."shotsAgainst") AS "savePct"
    FROM "goalie_appearances"
    LEFT JOIN "games" ON goalie_appearances."gameID" == "games"."id"
    WHERE "games"."gameType" == :gameType
    GROUP BY "playerID", "games"."season"
) SELECT
    goalie_seasons."season",
    max("gamesPlayed") AS maxGamesPlayed,
    max("gamesStarted") AS maxGamesStarted,
    max("wins") AS maxWins,
    max("losses") AS maxLosses,
    min("goalsAgainstAvg") AS minGAA,
    max("savePct") AS maxSavePct
FROM goalie_seasons LEFT JOIN max_games ON goalie_seasons."season" == max_games.season
WHERE gamesPlayed >= 0.3125 * max_games."games"
GROUP BY goalie_seasons."season"
ORDER BY goalie_seasons."season" ASC;