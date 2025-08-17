WITH skater_seasons AS (
    SELECT
        "playerID",
        "games"."season",
        "teamID",
        count("skater_appearances"."gameID") AS "gamesPlayed",
        sum("skater_appearances"."goals") AS "goals",
        sum("skater_appearances"."assists") AS "assists",
        sum("skater_appearances"."goals") + sum("skater_appearances"."assists") AS "points",
        sum("skater_appearances"."powerPlayGoals") AS "powerPlayGoals",
        sum("skater_appearances"."plusMinus") AS "plusMinus",
        sum("skater_appearances"."pim") AS "penaltyMinutes",
        sum("skater_appearances"."hits") AS "hits",
        sum("skater_appearances"."sog") AS "sog",
        sum("skater_appearances"."blocks") AS "blocks"
    FROM "skater_appearances"
    LEFT JOIN games ON "skater_appearances"."gameID" == "games".id
    WHERE "games"."gameType" == :gameType
    GROUP BY "playerID", games.season, "teamID")
SELECT
    "season",
    max("gamesPlayed") AS maxGamesPlayed,
    max("goals") AS maxGoals,
    max("assists") AS maxAssists,
    max("points") AS maxPoints,
    max("powerPlayGoals") AS maxPowerPlayGoals,
    max("plusMinus") AS maxPlusMinus,
    max("penaltyMinutes") AS maxPenaltyMinutes,
    max("hits") AS maxHits,
    max("sog") AS maxShotsOnGoal,
    max("blocks") AS maxBlocks
FROM skater_seasons
GROUP BY "season"
ORDER BY "season" ASC;
