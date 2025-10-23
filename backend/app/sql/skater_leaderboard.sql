WITH home_games AS (
    SELECT
        "homeTeamID",
        count(id) AS homeGames
    FROM games
    WHERE "gameType" == :gameType AND "season" == :season
    GROUP BY "homeTeamID"
),
away_games AS (
    SELECT
        "awayTeamID",
        count(id) AS awayGames
    FROM games
    WHERE "gameType" == :gameType AND "season" == :season
    GROUP BY "awayTeamID"
),
team_games AS (
    SELECT
        home_games."homeTeamID" AS "teamID",
        coalesce(homeGames, 0) + coalesce(awayGames, 0) AS totalGames
    FROM home_games
    FULL JOIN away_games ON home_games."homeTeamID" == away_games."awayTeamID"
)
SELECT
    skater_appearances."playerID",
    players."firstName" || " " || players."lastName" AS "fullName",
    players."position",
    players."isActive",
    CASE WHEN count("skater_appearances"."gameID") >= 0.3125 * "team_games"."totalGames" THEN 1 ELSE 0 END AS "qualified",
    group_concat(DISTINCT "skater_appearances"."teamID") AS "teams",
    count("skater_appearances"."gameID") AS "gamesPlayed",
    sum("skater_appearances"."goals") AS "goals",
    sum("skater_appearances"."assists") AS "assists",
    sum("skater_appearances"."goals") + sum("skater_appearances"."assists") AS "points",
    sum("skater_appearances"."plusMinus") AS "plusMinus",
    sum("skater_appearances"."pim") AS "penaltyMinutes",
    sum("skater_appearances"."hits") AS "hits",
    sum("skater_appearances"."sog") AS "sog",
    sum("skater_appearances"."blocks") AS "blocks",
    sum("skater_appearances"."toiSeconds") * 1.0 / count("skater_appearances"."gameID") AS "avgTOI"
FROM "skater_appearances"
LEFT JOIN games ON "skater_appearances"."gameID" == "games".id
LEFT JOIN players ON skater_appearances."playerID" == "players".id
LEFT JOIN team_games ON skater_appearances."teamID" == team_games."teamID"
WHERE "games"."gameType" == :gameType AND games.season == :season
GROUP BY skater_appearances."playerID"
ORDER BY "points" DESC;