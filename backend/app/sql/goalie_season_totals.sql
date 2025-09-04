SELECT
    "playerID",
    "games"."season",
    "teamID",
    sum("goalie_appearances"."played") AS "gamesPlayed",
    sum("goalie_appearances"."starter") AS "gamesStarted",
    sum(CASE WHEN "goalie_appearances"."decision" == 'W' THEN 1 ELSE 0 END) AS "wins",
    sum(CASE WHEN "goalie_appearances"."decision" == "L" THEN 1 ELSE 0 END) AS "losses",
    sum(goalie_appearances."shotsAgainst") - sum(goalie_appearances."saves") AS "goalsAgainst",
    (sum("goalie_appearances"."shotsAgainst") - sum("goalie_appearances"."saves")) * 3600.0 / sum("goalie_appearances"."toiSeconds") AS "goalsAgainstAvg",
    sum("goalie_appearances"."saves") * 1.0 / sum("goalie_appearances"."shotsAgainst") AS "savePct",
    sum("goalie_appearances"."evenStrengthSaves") * 1.0 / sum("goalie_appearances"."evenStrengthShotsAgainst") AS "evenStrengthSavePct",
    sum("goalie_appearances"."powerPlaySaves") * 1.0 / sum("goalie_appearances"."powerPlayShotsAgainst") AS "powerPlaySavePct"
FROM "goalie_appearances"
LEFT JOIN "games" ON goalie_appearances."gameID" == "games"."id"
WHERE "goalie_appearances"."playerID" == :playerID AND "games"."gameType" == :gameType
GROUP BY "playerID", "games"."season", "teamID";