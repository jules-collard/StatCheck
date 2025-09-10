SELECT
    "games"."season",
    "teamID",
    count("skater_appearances"."gameID") AS "gamesPlayed",
    sum("skater_appearances"."goals") AS "goals",
    sum("skater_appearances"."assists") AS "assists",
    sum("skater_appearances"."plusMinus") AS "plusMinus",
    sum("skater_appearances"."pim") AS "penaltyMinutes",
    sum("skater_appearances"."hits") AS "hits",
    sum("skater_appearances"."sog") AS "sog",
    sum("skater_appearances"."blocks") AS "blocks",
    sum("skater_appearances"."toiSeconds") * 1.0 / count("skater_appearances"."gameID") AS "avgTOI"
FROM "skater_appearances"
LEFT JOIN games ON "skater_appearances"."gameID" == "games".id
WHERE "playerID" == :playerID AND "games"."gameType" == :gameType
GROUP BY games.season, "teamID"
ORDER BY games.season, "teamID";