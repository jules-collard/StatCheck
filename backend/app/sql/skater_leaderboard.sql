SELECT
    skater_appearances."playerID",
    players."firstName",
    players."lastName",
    group_concat(DISTINCT "teamID") AS "teams",
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
LEFT JOIN players ON skater_appearances."playerID" == "players".id
WHERE "games"."gameType" == :gameType AND games.season == :season
GROUP BY skater_appearances."playerID"
ORDER BY "goals" DESC;