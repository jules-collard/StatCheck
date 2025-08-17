WITH goalie_seasons AS (
    SELECT
        "playerID",
        "games"."season",
        sum("goalie_appearances"."played") AS "gamesPlayed",
        sum("goalie_appearances"."starter") AS "gamesStarted",
        sum(CASE WHEN "goalie_appearances"."decision" == 'W' THEN 1 ELSE 0 END) AS "wins",
        sum(CASE WHEN "goalie_appearances"."decision" == "L" THEN 1 ELSE 0 END) AS "losses",
        (sum("goalie_appearances"."shotsAgainst") - sum("goalie_appearances"."saves")) * 3600.0 / sum("goalie_appearances"."toiSeconds") AS "goalsAgainstAvg",
        sum("goalie_appearances"."saves") * 1.0 / sum("goalie_appearances"."shotsAgainst") AS "savePct",
        sum("goalie_appearances"."evenStrengthSaves") * 1.0 / sum("goalie_appearances"."evenStrengthShotsAgainst") AS "evenStrengthSavePct",
        sum("goalie_appearances"."powerPlaySaves") * 1.0 / sum("goalie_appearances"."powerPlayShotsAgainst") AS "powerPlaySavePct"
    FROM "goalie_appearances"
    LEFT JOIN "games" ON goalie_appearances."gameID" == "games"."id"
    WHERE "games"."gameType" == :gameType
    GROUP BY "playerID", "games"."season"
) SELECT
    season,
    max("gamesPlayed") AS maxGamesPlayed,
    max("gamesStarted") AS maxGamesStarted,
    max("wins") AS maxWins,
    max("losses") AS maxLosses,
    min("goalsAgainstAvg") AS minGAA,
    max("savePct") AS maxSavePct,
    max("evenStrengthSavePct") AS maxEVSavePct,
    max("powerPlaySavePct") AS maxPPSavePct
FROM goalie_seasons
WHERE gamesPlayed >= 0.3125 * 82
GROUP BY season
ORDER BY season ASC;