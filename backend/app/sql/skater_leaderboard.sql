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
),
advanced AS (
    SELECT
        skater_appearances."playerID",
        coalesce(SUM(xg), 0) AS xg,
        sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS xgGoals,
        count(*) AS fenwick
    FROM events
    LEFT JOIN games ON events."gameID" == games.id
    LEFT JOIN skater_appearances ON coalesce(events."shootingPlayerID", events."scoringPlayerID") == skater_appearances."playerID" AND events."gameID" == skater_appearances."gameID"
    WHERE
        games."season" == :season
        AND events.xg NOT NULL
        AND games."gameType" == :gameType
    GROUP BY skater_appearances."playerID"
),
onice AS (
    SELECT
        "playerID",
        1.0 * sum("goalsFor") / sum("sogFor") AS onIceShootingPct,
        sum("fenwickFor") AS fenwickFor,
        sum("fenwickAgainst") AS fenwickAgainst,
        sum("corsiFor") AS corsiFor,
        sum("corsiAgainst") AS corsiAgainst,
        sum("xgFor") AS xgFor,
        sum("xgAgainst") AS xgAgainst,
        sum("oZoneStarts") AS oZoneStarts,
        sum("nZoneStarts") AS nZoneStarts,
        sum("dZoneStarts") AS dZoneStarts
    FROM split_shifts
    LEFT JOIN games on split_shifts."gameID" == games.id
    WHERE
        games."gameType" == :gameType
        AND games.season == :season
        AND "attackingSkaters" == "defendingSkaters"
    GROUP BY "playerID"
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
    sum("skater_appearances"."toiSeconds") * 1.0 / count("skater_appearances"."gameID") AS "avgTOI",
    coalesce(advanced.xg, 0) AS xg,
    coalesce(advanced.xgGoals, 0) AS xgGoals,
    coalesce(advanced.fenwick, 0) AS fenwick,
    coalesce(onice.onIceShootingPct, 0) AS onIceShootingPct,
    coalesce(onice.fenwickFor, 0) AS fenwickFor,
    coalesce(onice.fenwickAgainst, 0) AS fenwickAgainst,
    coalesce(onice.corsiFor, 0) AS corsiFor,
    coalesce(onice.corsiAgainst, 0) AS corsiAgainst,
    coalesce(onice.xgFor, 0) AS xgFor,
    coalesce(onice.xgAgainst, 0) AS xgAgainst,
    coalesce(onice.oZoneStarts, 0) AS oZoneStarts,
    coalesce(onice.nZoneStarts, 0) AS nZoneStarts,
    coalesce(onice.dZoneStarts, 0) AS dZoneStarts
FROM "skater_appearances"
LEFT JOIN games ON "skater_appearances"."gameID" == "games".id
LEFT JOIN players ON skater_appearances."playerID" == "players".id
LEFT JOIN team_games ON skater_appearances."teamID" == team_games."teamID"
LEFT JOIN advanced ON advanced."playerID" == skater_appearances."playerID"
LEFT JOIN onice ON skater_appearances."playerID" == onice."playerID"
WHERE "games"."gameType" == :gameType AND games.season == :season
GROUP BY skater_appearances."playerID"
ORDER BY "points" DESC;